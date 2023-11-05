from fastapi import FastAPI, HTTPException, File, UploadFile
from PIL import Image
from io import BytesIO
from .main import decompose_image, DecompositionResponse
from .logger import get_logger

logger = get_logger(name=__name__)
web_app = FastAPI()

# API endpoint to decompose an image and return a promise that resolves to a
# list of objects that have a 'uuid', 'img', and 'keyword', 'linklist',
# (optional) image 'description'.
@web_app.post(path="/api/decompose", response_model=list[DecompositionResponse])
async def decompose_and_return_response(
    image: UploadFile = File(...)
) -> list[DecompositionResponse]:
    try:
        # Read image file as Image
        image_data = await image.read()
        image_object = Image.open(fp=BytesIO(initial_bytes=image_data))

        # Decompose the image
        response: list[DecompositionResponse] = decompose_image.local(image_object)

        # Return a list of objects that have a 'uuid', 'img', and 'keyword',
        # 'linklist', (optional) image 'description'.
        return response
    except Exception as e:
        # An unexpected error occurred, return a 500 error
        logger.error(msg=f"An unexpected error occurred while processing your request: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"An unexpected error occurred while processing your request: {str(e)}"
        )
