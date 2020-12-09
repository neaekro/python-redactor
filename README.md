# python-redactor

## Description
Running server.py will start a Flask server that accepts POST requests containing a file in jpg, jpeg, png formats at localhost:5000. 

It will return a JSON containing "boxes", an array of multiple arrays each of which contains a starting X coordinate, starting Y coordinate, ending X, and ending Y that corresponds to a bounding box around any text the EAST detection model sees. 

The JSON also contains a "text" array that contains strings corresponding to the same index as the box it describes in the "boxes" array.

## Requirements
* [Tesseract](https://github.com/tesseract-ocr/tesseract)
* Python Packages
  * pytesseract
  * opencv-python
  * Flask
  * numpy
  
To install the python packages, run 
```python
pip install <package name>
```

## Usage
Tested using the Postman Desktop App

1. Run server.py
2. Setup a new request to localhost:5000 or whichever IP is hosted by server.py
3. Change the request type to POST
4. Click body in the navigation bar of that request, and click "form-data". 
5. Include a file with the key "file" that is a picture with text of the form jpg, jpeg, or png. It should look something like the picture below
![example request](https://i.imgur.com/T0iCBLI.png)
6. Send the request and you should receive a JSON of the aforementioned format described in the description
