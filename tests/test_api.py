import requests
from pathlib import Path
from img_decomposition.main import DecompositionResponse

def test_decomposition_endpoint() -> None:
    # Define the URL
    url = 'https://chriscarrollsmith--image-decompisition-api-v2-fastapi-app.modal.run/api/decompose'
    
    # Path to the image you want to upload
    image_path = 'room.png'

    # Assert that the image exists
    assert Path(image_path).exists()

    # Prepare the files dictionary
    files = {
        'image': ('image.png', open(file=image_path, mode='rb'), 'image/png')
    }
    
    # Make the POST request
    response = requests.post(url=url, files=files)
    
    # Assert that the response code is 200
    assert response.status_code == 200

    # Validate that response can be parsed as a pydantic DecompositionResponse
    DecompositionResponse(**response.json())

    # Close the file after uploading
    files['image'][1].close()
