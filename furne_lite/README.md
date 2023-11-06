# FURN-E Lite

FURN-E Lite based on FURN-E, the "Open Source" category winner of the 2023 AEC Hackathon in NYC.

## How to use FURN-E Lite

1. Download this GitHub repo as a ZIP file to your local hard drive.
2. Upload the file `FURN-E_Lite.ipynb` to your Google Drive.
3. In Google Drive, open `FURN-E_Lite.ipynb` with Google Colaboratory. Specifically, right click `FURN-E_Lite.ipynb` in Google Drive, go to "Open With">"Google Colaboratory"
4. Once you open `FURN-E_Lite.ipynb` within Google Colab, follow Steps 0 through 2 and you should be good to go!
5. Feel free to use `img_00.png` as a starter example.

## But I don't know how to code...

That's OK! As long as you have Google Drive, you can use Google Colaboratory ("Colab" for short), which will allow you to run machine learning code from just your browser! `ipynb` files are Python notebook files where an author can explain how code works in plain ol' text as they add more chunks or "cells" of code to run.

So, once you can open `FURN-E_Lite.ipynb` within Google Colab, the step-by-step instructions will tell you how to run all the code inside. The only modification you need to do is change a file path specifying where in Google Drive you've uploaded your generative AI image for identifying furniture within it.

You may need to visit this link first: https://colab.research.google.com so that you can open `ipynb` files directly from Google Drive and never leave the browser. But after that, you should be off to the races!

## What's the difference between FURN-E and FURN-E Lite?

The original FURN-E project made for the hackathon tried to make a web app that went from a DALL-E image generation prompt all the way to displaying images of furniture objects within the generated image paired with links to actual furniture products found online. The full implementation consists of a web-based front-end made with Vue.js and a backend with Flask API. 

The idea behind FURN-E Lite is to do pretty much the same thing with a single Python notebook running on Google Colab. In the spirit of Open Source, this project uses a single notebook to explain the components of FURN-E step by step so that:

 - absolute beginners can just use the notebook on their own Midjourney/DALL-E images.

 - programmers can repurpose this code for their own use cases for object identification within AI generated images.

Besides the fact that this project is basically a single Python notebook, the final results you get are also slightly different from the original FURN-E. FURN-E Lite gives you product links from a specific set of retail/furniture seller websites, using only a text-based Google search. 
