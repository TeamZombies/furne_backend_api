import torch
import os
from PIL import Image
import json

from transformers import ViltProcessor, ViltForQuestionAnswering

class ImageProcessor(object):
    def __init__(self, img_dir = 'Images', results_dir = 'Results'):
        self.class_dict = {
        56: "chair",
        57: "couch",
        58: "potted plant",
        59: "bed",
        60: "dining table",
        61: "toilet",
        62: "tv",
        68: "microwave",
        69: "oven",
        71: "sink",
        72: "refrigerator",
        74: "clock"
        }

        self.classes = [key for key in self.class_dict.keys()]
        
        # Object Detection Model
        self.obj_det_model = torch.hub.load('ultralytics/yolov5', 'yolov5s')  # or yolov5m, yolov5x, custom
        self.obj_det_model.classes = self.classes

        
        self.img2text_processor = ViltProcessor.from_pretrained("dandelin/vilt-b32-finetuned-vqa")
        self.img2text_model = ViltForQuestionAnswering.from_pretrained("dandelin/vilt-b32-finetuned-vqa")

        # Image Directory
        self.img_dir = img_dir

        self.results_dir = results_dir

    def detect_obj(self,img_file_path):
        # Inference
        results = self.obj_det_model(img_file_path)
        return results

    def get_cropped_imgs(self, img, img_file_path, img_results_dir):
        obj_results = self.detect_obj(img_file_path)

        croppings_df = obj_results.pandas().xyxy[0]

        class_list = list(croppings_df['name'])
        # cropped_images = []
        cropped_images_files = []

        for index, row in croppings_df.iterrows():
            # Define the coordinates for the crop (left, upper, right, lower)
            left, upper, right, lower = row['xmin'], row['ymin'], row['xmax'], row['ymax']

            # Crop the image using slices
            cropped_image = img.crop((left, upper, right, lower))

            # Display or save the cropped image
            # display(cropped_image)
            class_name = row['name']
            cropped_file_name = os.path.join(img_results_dir, f'{index}_{class_name}.png')

            cropped_image.save(cropped_file_name)
            # cropped_images.append(cropped_image)
            cropped_images_files.append(cropped_file_name)
        
        return class_list, cropped_images_files
    
    def get_text_description(self, img, class_name):
        attributes = ['style', 'color', 'material']
        description = []
        for attr in attributes:
            # prepare image + question
            text = f"Describe the {class_name} {attr}"

            # prepare inputs
            encoding = self.img2text_processor(img, text, return_tensors="pt")

            # forward pass
            outputs = self.img2text_model(**encoding)
            logits = outputs.logits
            idx = logits.argmax(-1).item()
            description.append(self.img2text_model.config.id2label[idx])
            # print("Predicted answer:", self.img2text_model.config.id2label[idx])

        description.append(class_name)

        description = " ".join(description)
        return description
    
    def generate_img_text_prompts(self,img_file):

        img_file_path = os.path.join(self.img_dir,img_file)

        # Results Directory
        results_folder_name = img_file.split('.')[0]
        img_results_dir = os.path.join(self.results_dir, results_folder_name)

        # Check if the folder exists
        if not os.path.exists(img_results_dir):
            # If it doesn't exist, create the folder
            os.mkdir(img_results_dir)

        image = Image.open(img_file_path)

        class_list, cropped_images_files = self.get_cropped_imgs(img=image,img_file_path=img_file_path,img_results_dir=img_results_dir)
        
        prompts = []
        for i, crop_img_file in enumerate(cropped_images_files):
            crop_img = Image.open(crop_img_file)
            prompt_obj = {
                "image_file": "",
                "obj_class": "",
                "text_description": ""
            }
            prompt_obj["image_file"] = cropped_images_files[i]
            prompt_obj["obj_class"] = class_list[i]
            prompt_obj["text_description"] = self.get_text_description(img=crop_img, class_name=class_list[i])
            prompts.append(prompt_obj)

        prompt_dict = {
            'prompts': prompts
        }

        file_path = os.path.join(img_results_dir,'prompts.json')
        # Write the dictionary to a JSON file
        with open(file_path, 'w') as json_file:
            json.dump(prompt_dict, json_file)

        return prompts


if __name__ == "__main__":
    # Image Directory
    img_dir = os.path.join('Images')

    results_dir = os.path.join('Results')

    processor = ImageProcessor(img_dir=img_dir, results_dir=results_dir)
    
    img_file = 'img_00.png'

    processor.generate_img_text_prompts(img_file=img_file)


