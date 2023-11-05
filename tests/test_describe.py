import os
from PIL import Image
from img_decomposition.describe import get_text_description, IMG2TEXT_PROCESSOR, IMG2TEXT_MODEL

def test_get_text_description():
    # Load the image
    img_path = os.path.join(os.path.dirname(__file__), '..', 'sofa.png')
    img = Image.open(img_path)

    # Call the function with the image and 'chair' as arguments
    description = get_text_description(IMG2TEXT_PROCESSOR, IMG2TEXT_MODEL, img, 'chair')

    # Assert that the returned description is a string and contains the word 'chair'
    assert isinstance(description, str)
    assert 'chair' in description
