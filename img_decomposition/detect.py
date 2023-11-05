import torch
from PIL import Image
import os
import uuid

# Define constants and load models once to avoid reloading them every time a function is called
CLASS_DICT = {
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

# Load models
OBJ_DET_MODEL = torch.hub.load('ultralytics/yolov5', 'yolov5s')
OBJ_DET_MODEL.classes = [key for key in CLASS_DICT.keys()]

def get_cropped_images(obj_det_model, img: Image, img_results_dir: str) -> tuple[list, list, list]:
    # Convert PIL Image to a format suitable for the model if required
    img_for_detection = img
    if isinstance(img, Image.Image):
        # Convert PIL Image to CV2 (if your model requires that)
        # In most cases, YOLOv5 from torch.hub can handle PIL images directly.
        pass

    # Detect objects in the image data
    results = obj_det_model(img_for_detection)

    # Process the results
    croppings_df = results.pandas().xyxy[0]
    class_list = list(croppings_df['name'])
    uuids = [str(uuid.uuid4()) for _ in range(len(class_list))]
    cropped_image_files = []

    for index, row in croppings_df.iterrows():
        # Coordinates for cropping
        left, upper, right, lower = row['xmin'], row['ymin'], row['xmax'], row['ymax']
        cropped_image = img.crop((left, upper, right, lower))
        # Create a filename for the cropped image
        cropped_file_name = os.path.join(img_results_dir, f'{uuids[index]}.png')
        # Save the cropped image to the results directory
        cropped_image.save(cropped_file_name)
        cropped_image_files.append(cropped_file_name)

    return uuids, cropped_image_files, class_list
