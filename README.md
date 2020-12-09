# python-redactor

## Description
Running server.py will start a Flask server that accepts POST requests containing a file in jpg, jpeg, png formats at localhost:5000. 

It will return a JSON containing "boxes", an array of multiple arrays each of which contains a starting X coordinate, starting Y coordinate, ending X, and ending Y that corresponds to a bounding box around any text the EAST detection model sees. 

The JSON also contains a "text" array that contains strings corresponding to the same index as the box it describes in the "boxes" array.

## Usage
Tested using the Postman Desktop App

1. Setup a new request to localhost:5000 or whatever IP is hosted by server.py
2. Change the request type to POST
3. Click body in the navigation bar of that request, and click "form-data". 
4. Include a file with the key "file" that is a picture with text of the form jpg, jpeg, or png. It should look something like the picture below
![example request](https://i.imgur.com/T0iCBLI.png)
5. Send the request and you should receive a JSON of the aforementioned format described in the description
