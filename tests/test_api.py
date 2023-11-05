import requests
from pathlib import Path

def test_decomposition_endpoint() -> None:
    # Define the URL
    url = 'https://chriscarrollsmith--image-decompisition-api-v2-fastapi-app.modal.run/api/decompose'
    
    # Path to the image you want to upload
    image_path = 'C:/Users/chris/Downloads/image.png'

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

    # Define expected response
    expected_response = [
        dict(
            uuid="1",
            img="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z/C/HgAGgwJ/lK3Q6wAAAABJRU5ErkJggg==",
            keyword="pixel",
            linklist=["https://www.google.com/"],
            description="Here's a description of the image"
        )
    ]

    # Assert that the response is as expected
    assert response.json() == expected_response

    # Close the file after uploading
    files['image'][1].close()
