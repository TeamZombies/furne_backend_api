# ---
# lambda-test: false
# ---

from typing import Optional

from fastapi import FastAPI, Header
from modal import Image, Stub, asgi_app, web_endpoint
from pydantic import BaseModel

web_app = FastAPI()
app_image = (
        Image.debian_slim(python_version="3.10")
        .pip_install(
            "fastapi",
            "pydantic>=2.2.1",
        )
    )
stub = Stub(
        name="example-fastapi-app",
        image=app_image,
    )

class TranscriptionRequest(BaseModel):
    src_url: str
    unique_id: int
    session_title: Optional[str] = None
    presenters: Optional[str] = None
    is_video: Optional[bool] = False
    password: Optional[str] = None

@web_app.post(path="/api/decompose")
async def decompose(user_agent: Optional[str] = Header(None)):
    print(f"GET /     - received user_agent={user_agent}")
    return "Hello World"


@web_app.post("/foo")
async def handle_foo(item: Item, user_agent: Optional[str] = Header(None)):
    print(
        f"POST /foo - received user_agent={user_agent}, item.name={item.name}"
    )
    return item


@stub.function()
@asgi_app()
def fastapi_app():
    return web_app


@stub.function()
@web_endpoint(method="POST")
def f(item: Item):
    return "Hello " + item.name


if __name__ == "__main__":
    stub.deploy("webapp")
