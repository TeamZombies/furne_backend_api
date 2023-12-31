from .logger import get_logger
import requests
import os
from dotenv import load_dotenv

# Initialize logger
logger = get_logger(name=__name__)

# Load environment variables
load_dotenv()

# Define constants
base_uri = 'https://api.bing.microsoft.com/v7.0/images/visualsearch'
subscription_key = os.environ.get('BING_API_KEY')
headers = {
    'Ocp-Apim-Subscription-Key': subscription_key,
}

# Search for matching products given a list of image file paths
def search_for_products(image_file_paths: list[str]) -> list[dict]:
    # Return None if no image file paths are provided
    if len(image_file_paths) == 0:
        return None
    
    # Search for matching products for each image using the Bing Visual Search API
    linklists = []
    for image_path in image_file_paths:
        with open(file=image_path, mode='rb') as image_file:
            file = {'image': (image_path, image_file, 'image/png')}
            response = requests.post(url=base_uri, headers=headers, files=file)

        if response.status_code == 200:
            # Compile the first five results into a list of dictionaries
            for item in response.json()['tags'][0]['actions']:
                if item['actionType'] == 'VisualSearch':
                    results = item['data']['value']
                    pagelinks = []
            
            pagelinks = []
            for result in results[0:3]:
                pagelinks.append({
                    'thumbnailUrl': result['thumbnailUrl'],
                    'hostPageUrl': result['hostPageUrl']
                })
            linklists.append(pagelinks)
        else:
            raise requests.exceptions.HTTPError((f"Request failed with status code {response.status_code}: {response.text}"))
        
    # Return the link list (for now, return the responses)
    return linklists
