from .logger import get_logger
import requests
import os
from dotenv import load_dotenv

# Initialize logger
logger = get_logger(name=__name__)

# Load environment variables
load_dotenv()

# Define constants
base_uri = 'https://api.cognitive.microsoft.com/bing/v7.0/images/visualsearch'
subscription_key = os.environ.get('BING_API_KEY')
headers = {
    'Ocp-Apim-Subscription-Key': subscription_key,
}

# Search for matching products given a list of image file paths
def search_for_products(image_file_paths):
    # Return None if no image file paths are provided
    if len(image_file_paths) == 0:
        return None
    
    # Search for matching products for each image using the Bing Visual Search API
    responses = []
    for image_path in image_file_paths:
        with open(file=image_path, mode='rb') as image_file:
            file = {'image': (image_path, image_file, 'image/png')}
        response = requests.post(base_uri, headers=headers, files=file)

        if response.status_code == 200:
            # Add the response to the list of responses
            responses.append(response)
        else:
            raise requests.exceptions.HTTPError((f"Request failed with status code {response.status_code}: {response.text}"))

    # TODO: Process the responses and return a list of links to matching products

    # Return the link list (for now, return the responses)
    return responses
