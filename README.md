# Fast Audio/Video transcribe using Openai's Whisper and Modal

## Powered by Modal.com for parallel processing on-demand, an hour audio file can be transcribed in ~1 minute.

"Modal’s dead-simple parallelism primitives are the key to doing the transcription so quickly. Even with a GPU, transcribing a full episode serially was taking around 10 minutes. But by pulling in ffmpeg with a simple .pip_install("ffmpeg-python") addition to our Modal Image, we could exploit the natural silences of the podcast medium to partition episodes into hundreds of short segments. Each segment is transcribed by Whisper in its own container task with 2 physical CPU cores, and when all are done we stitch the segments back together with only a minimal loss in transcription quality. This approach actually accords quite well with Whisper’s model architecture." The model uses 30-second chunking.

## How to develop

1. Create a Modal account and get your API key.

   - Run this command to install modal client and generate token.

     ```bash
     pip install modal-client
     modal token new
     ```

     - The first command will install the Modal client library on your computer, along with its dependencies.

     - The second command creates an API token by authenticating through your web browser. It will open a new tab, but you can close it when you are done.

2. Deploy your modal project with the following command.

   ```bash
   modal deploy img_decomposition.main
   ```

## How to use

1. Transcribe your audio file using the following curl command. The 'transcribe' endpoint wants a JSON formatted request:

  ```curl
  curl -X POST "https://chriscarrollsmith--image-decompisition-api-v2-fastapi-app.modal.run/api/decompose" \
     -H "accept: application/json" \
     -H "Content-Type: multipart/form-data" \
     -F "image=@/path_to_your_image/image.jpg"
  ```

   Sample response:

   ```json
   {
     "job_id": "your-job-id"
   }
   ```
