import os
from PIL import Image
from img_decomposition.detect import get_cropped_images, OBJ_DET_MODEL

def test_get_cropped_images() -> None:
    # Load the test image
    img = Image.open(fp=os.path.join(os.path.dirname(p=__file__), '..', 'room.png'))

    # Define the results directory and ensure it exists
    img_results_dir = os.path.join(os.path.dirname(p=__file__), '..', 'results')
    os.makedirs(img_results_dir, exist_ok=True)

    # Call the function with the test image
    cropped_image_files, class_list = get_cropped_images(obj_det_model=OBJ_DET_MODEL, img=img, img_results_dir=img_results_dir)

    # Assert that the function returns a list of cropped image files and a list of classes
    assert isinstance(cropped_image_files, list)
    assert isinstance(class_list, list)

    # Assert that the length of the lists is the same
    assert len(cropped_image_files) == len(class_list)

    # Assert that each item in the list of cropped image files is a string representing a file path
    for cropped_image_file in cropped_image_files:
        assert isinstance(cropped_image_file, str)
        assert os.path.isfile(cropped_image_file)

    # Assert that each item in the list of classes is a string
    for class_item in class_list:
        assert isinstance(class_item, str)
