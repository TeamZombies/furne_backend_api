"""
API endpoint that takes an image file and returns a promise that resolves to a
list of objects that have a 'uuid', 'img', and 'keyword', 'linklist',
(optional) image 'description'.
"""
from fastapi import FastAPI
from modal import Dict, Image, NetworkFileSystem, Stub, asgi_app, Secret
from .search import search_for_products
from .logger import get_logger
from pydantic import BaseModel
from .describe import generate_descriptions, IMG2TEXT_PROCESSOR, IMG2TEXT_MODEL
from .detect import get_cropped_images, OBJ_DET_MODEL
from .search import search_for_products
import os

logger = get_logger(name=__name__)

# Define a Pydantic model for request response - 
# 'uuid', img, and keyword, linklist, (optional) image description.  
class DecompositionResponse(BaseModel):
    uuid: str
    img: str # base64 encoded image
    keyword: str
    linklist: list[str]
    description: str

# Define paths to cache directories
CACHE_DIR = "/cache"

# Create a persistent cache for storing logs across application runs
volume = NetworkFileSystem.persisted(label="dataset-cache-vol")

app_image = (
    Image.debian_slim(python_version="3.11")
    .pip_install(
        "fastapi",
        "pydantic",
        "uuid",
        "gitpython>=3.1.30",
        "matplotlib>=3.3",
        "numpy>=1.22.2",
        "opencv-python>=4.1.1",
        "Pillow>=10.0.1",
        "psutil",
        "PyYAML>=5.3.1",
        "requests>=2.23.0",
        "scipy>=1.4.1",
        "thop>=0.1.1",
        "torch>=1.8.0",
        "torchvision>=0.9.0",
        "tqdm>=4.64.0",
        "ultralytics>=8.0.147",
        "transformers",
        "python-dotenv"
    )
)

# Create a modal.Stub instance for managing the application
stub = Stub(
    name="image-decompisition-api-v2",
    image=app_image,
)

# Define a dictionary object for tracking progress within the Stub
stub.in_progress = Dict.new()


# Import api.py and register it with the stub as an asynchronous ASGI app,
# including setting shared volumes and a keep-warm strategy
@stub.function(
    network_file_systems={CACHE_DIR: volume},
    keep_warm=1
)
@asgi_app()
def fastapi_app() -> FastAPI:
    from .api import web_app
    return web_app


# Register the decompose_image function with the stub, along with specific
# configurations like image, shared volumes, secrets, etc.
# This function controls the overall flow of the application.
@stub.function(
    image=app_image,
    network_file_systems={CACHE_DIR: volume},
    timeout=900,
    secrets=[
        Secret.from_name(app_name="bing_api_key")
    ]
)
def decompose_image(image) -> list[DecompositionResponse]:    
    # Create a directory for the results only if it doesn't exist
    img_results_dir = os.path('results')
    if not os.path.exists(path=img_results_dir):
        os.makedirs(name=img_results_dir)
    
    # Get cropped images and classifications using an object detection model
    uuids, cropped_images, image_classifications = crop_image(
            obj_det_model=OBJ_DET_MODEL,
            img=image,
            img_results_dir=img_results_dir
        )

    # Detect objects in the image and return a list of prompt dictionaries
    descriptions = generate_descriptions(
            img_file=cropped_images,
            image_classifications=image_classifications,
            img2text_processor=IMG2TEXT_PROCESSOR,
            img2text_model=IMG2TEXT_MODEL
        )

    # For each cropped image, search for matching products and return a list of
    # links to the matching products
    linklists = search(
            cropped_images=cropped_images
        )

    # For each cropped image, convert the image to base64 and return a list of
    # base64 encoded images
    base64_images = []
    for image in cropped_images:
        with open(image, "rb") as image_file:
            base64_images.append(image_file.read())

    # Clean up the results directory
    os.remove(img_results_dir)
    
    # Create a list of DecompositionResponse objects that have a 'uuid', 'img',
    # and 'keyword', 'linklist', and image 'description'
    decomposition_responses = []
    for index, uuid in enumerate(uuids):
        decomposition_responses.append(
            DecompositionResponse(
                uuid=uuid,
                img=base64_images[index],
                keyword=image_classifications[index],
                linklist=linklists[index],
                description=descriptions[index]
            )
        )
    
    # Return the list of DecompositionResponse objects
    return decomposition_responses


# Register the search function with the stub
@stub.function(
    image=app_image,
    network_file_systems={CACHE_DIR: volume},
    cpu=2
)
def search(*args, **kwargs):
    return search_for_products(*args, **kwargs)

# Register the generate_img_text_prompts function with the stub
@stub.function(
    image=app_image,
    network_file_systems={CACHE_DIR: volume},
    cpu=2
)
def crop_image(*args, **kwargs):
    return get_cropped_images(*args, **kwargs)
