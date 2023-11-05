# Fast Image decomposition API

## Powered by Modal.com for parallel processing on-demand

1. To spin up a Modal instance, create a Modal account and get your API key.

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

## How to use the API

1. Here's how you would upload your image file to the API using CURL.

  ```curl
  curl -X POST "https://chriscarrollsmith--image-decompisition-api-v2-fastapi-app.modal.run/api/decompose" \
     -H "accept: application/json" \
     -H "Content-Type: multipart/form-data" \
     -F "image=@/path_to_your_image/image.jpg"
  ```

Alternatively, use the Javascript requests library:

   ```javascript
   // Select your input type=file and the image for upload
   const fileInput = document.querySelector('input[type="file"]');
   const imageData = fileInput.files[0]; // get the file

   // Create a FormData instance and append the file
   const formData = new FormData();
   formData.append('image', imageData); // 'image' is the key expected by the backend

   // Define the URL to your endpoint
   const url = 'https://chriscarrollsmith--image-decomposition-api-v2-fastapi-app.modal.run/api/decompose';

   // Make the POST request
   fetch(url, {
   method: 'POST',
   body: formData // FormData will be sent as 'multipart/form-data'
   })
   .then(response => {
   if (response.ok) {
      return response.json(); // if the response is good, get the JSON from the response
   }
   throw new Error('Network response was not ok.'); // if the response is not good, throw an error
   })
   .then(data => {
   console.log(data); // Handle the data from the response
   })
   .catch(error => {
   console.error('There has been a problem with your fetch operation:', error);
   });
   ```

Sample response:

   ```json
   [
      {
         "uuid" : "1",
         "img" : "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z/C/HgAGgwJ/lK3Q6wAAAABJRU5ErkJggg==",
         "keyword" : "pixel",
         "linklist" : [
               {
                  "thumbnailURL" : "https://www.google.com/",
                  "hostPageUrl" : "https://www.google.com/"
               }
            ],
         "description" : "Image of a single transparent pixel"
      }
   ]
   ```

## Testing

Unit tests are built on the pytest framework. To run the tests, run the following command from the root directory of the project.

```bash
pytest tests
```