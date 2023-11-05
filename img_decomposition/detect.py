import torch
import os
from PIL import Image
import json
from transformers import ViltProcessor, ViltForQuestionAnswering

# Define constants and load models once to avoid reloading them every time a function is called
CLASSES = ["chair","couch","potted plant","bed","dining table","toilet",
              "tv","microwave","oven","sink","refrigerator","clock"]

# Load models
OBJ_DET_MODEL = torch.hub.load('ultralytics/yolov5', 'yolov5s')
OBJ_DET_MODEL.classes = CLASSES
IMG2TEXT_PROCESSOR = ViltProcessor.from_pretrained("dandelin/vilt-b32-finetuned-vqa")
IMG2TEXT_MODEL = ViltForQuestionAnswering.from_pretrained("dandelin/vilt-b32-finetuned-vqa")

def detect_obj(obj_det_model, img_file_path):
    # Detect objects in the image
    results = obj_det_model(img_file_path)
    return results

def get_cropped_imgs(obj_det_model, img, img_file_path, img_results_dir):
    obj_results = detect_obj(obj_det_model, img_file_path)
    croppings_df = obj_results.pandas().xyxy[0]
    class_list = list(croppings_df['name'])
    cropped_images_files = []

    for index, row in croppings_df.iterrows():
        left, upper, right, lower = row['xmin'], row['ymin'], row['xmax'], row['ymax']
        cropped_image = img.crop((left, upper, right, lower))
        class_name = row['name']
        cropped_file_name = os.path.join(img_results_dir, f'{index}_{class_name}.png')
        cropped_image.save(cropped_file_name)
        cropped_images_files.append(cropped_file_name)
    
    return class_list, cropped_images_files

def get_text_description(img2text_processor, img2text_model, img, class_name):
    attributes = ['style', 'color', 'material']
    description = []
    for attr in attributes:
        text = f"Describe the {class_name} {attr}"
        encoding = img2text_processor(img, text, return_tensors="pt")
        outputs = img2text_model(**encoding)
        logits = outputs.logits
        idx = logits.argmax(-1).item()
        description.append(img2text_model.config.id2label[idx])

    description.append(class_name)
    return " ".join(description)

def generate_img_text_prompts(img_dir, results_dir, obj_det_model, img2text_processor, img2text_model, img_file):
    img_file_path = os.path.join(img_dir, img_file)
    results_folder_name = img_file.split('.')[0]
    img_results_dir = os.path.join(results_dir, results_folder_name)
    if not os.path.exists(img_results_dir):
        os.mkdir(img_results_dir)

    image = Image.open(img_file_path)
    class_list, cropped_images_files = get_cropped_imgs(obj_det_model, image, img_file_path, img_results_dir)
    prompts = []
    for i, crop_img_file in enumerate(cropped_images_files):
        crop_img = Image.open(crop_img_file)
        prompt_obj = {
            "image_file": crop_img_file,
            "obj_class": class_list[i],
            "text_description": get_text_description(img2text_processor, img2text_model, crop_img, class_list[i])
        }
        prompts.append(prompt_obj)

    file_path = os.path.join(img_results_dir, 'prompts.json')
    with open(file_path, 'w') as json_file:
        json.dump({'prompts': prompts}, json_file)

    return prompts
