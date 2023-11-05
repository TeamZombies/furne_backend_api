from PIL import Image
from typing import Literal
from transformers import ViltProcessor, ViltForQuestionAnswering

IMG2TEXT_PROCESSOR = ViltProcessor.from_pretrained("dandelin/vilt-b32-finetuned-vqa")
IMG2TEXT_MODEL = ViltForQuestionAnswering.from_pretrained("dandelin/vilt-b32-finetuned-vqa")


def get_text_description(
            img2text_processor,
            img2text_model,
            img: Image,
            class_name: Literal["chair", "couch", "potted plant", "bed", 
                                "dining table", "toilet", "tv", "microwave",
                                "oven", "sink", "refrigerator", "clock"]
        ):
    # Make sure that the image is in RGB format
    if img.mode != "RGB":
        img = img.convert(mode="RGB")
    
    # Get a text description of the style, color, and material of the object
    # in the image and return it as a string joined by spaces
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


def generate_descriptions(cropped_images, image_classifications, results_dir, img2text_processor, img2text_model):  
    # Generate a description for each cropped image
    descriptions = []
    for image, classification in zip(cropped_images, image_classifications):
        image_object = Image.open(image)
        description = get_text_description(img2text_processor, img2text_model, image_object, classification)
        descriptions.append(description)

    # Return a list of descriptions
    return descriptions
