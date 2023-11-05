import os
from PIL import Image
from img_decomposition.describe import get_text_description, generate_descriptions, IMG2TEXT_PROCESSOR, IMG2TEXT_MODEL

def test_get_text_description():
    # Load the image
    img_path = os.path.join(os.path.dirname(__file__), '..', 'sofa.png')
    img = Image.open(fp=img_path)

    # Call the function with the image and 'chair' as arguments
    description = get_text_description(
            img2text_processor=IMG2TEXT_PROCESSOR,
            img2text_model=IMG2TEXT_MODEL,
            img=img,
            class_name='chair'
        )

    # Assert that the returned description is a string and contains the word 'chair'
    assert isinstance(description, str)
    assert 'chair' in description

def test_generate_descriptions():
    # Define a list of cropped image paths and a list of classifications
    cropped_images = [os.path.join(os.path.dirname(__file__), '..', 'sofa.png')]
    image_classifications = ['chair']

    # Call the function with the lists as arguments
    descriptions = generate_descriptions(
            cropped_images=cropped_images,
            image_classifications=image_classifications,
            img2text_processor=IMG2TEXT_PROCESSOR,
            img2text_model=IMG2TEXT_MODEL
        )

    # Assert that the returned descriptions are a list of strings and each description contains the corresponding classification
    assert isinstance(descriptions, list)
    assert all(isinstance(description, str) for description in descriptions)
    assert all(classification in description for classification, description in zip(image_classifications, descriptions))
