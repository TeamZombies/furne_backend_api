"""
API endpoint that takes an image file and returns a promise that resolves to a
list of objects that have a 'uuid', 'img', and 'keyword', 'linklist',
(optional) image 'description'.
"""
from fastapi import FastAPI
from modal import Dict, Image, NetworkFileSystem, Stub, asgi_app #, Secret
from .search import search
from .logger import get_logger
from pydantic import BaseModel

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
        "uuid"
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
        #Secret.from_name(app_name="my-googlecloud-secret")   // Provide secrets to Modal and access here
    ]
)
def decompose_image(image) -> list[DecompositionResponse]:
    # Detect objects in the image and return a list of bounding boxes and
    # keyword labels
    logger.info(msg="Detecting objects in the image.")

    # Based on the bounding boxes, crop the original image into smaller images
    # and generate a uuid for each cropped image

    # For each cropped image search for matching products and return a list of
    # links to the matching products
    
    # Return a list of DecompositionResponse objects that have a 'uuid', 'img',
    # and 'keyword', 'linklist', (optional) image 'description'.
    return [
        DecompositionResponse(
            uuid="1",
            img="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z/C/HgAGgwJ/lK3Q6wAAAABJRU5ErkJggg==",
            keyword="pixel",
            linklist=["https://www.google.com/"],
            description="Here's a description of the image"
        )
    ]

# Register the transcribe_segment function with the stub
@stub.function(
    image=app_image,
    network_file_systems={CACHE_DIR: volume},
    cpu=2
)
def async_search(*args, **kwargs):
    return search(*args, **kwargs)
