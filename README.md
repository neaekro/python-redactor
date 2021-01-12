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
If you choose to build an image with Docker, then this step is unnecessary as they will be built together.

## Usage With Docker
Tested using the Postman Desktop App

1. Make sure Docker is installed on your machine
2. Run
```
docker pull jwn8175/xray-redactor
```
3. After the image is done pulling, run
```
docker run -p 5000:5000 jwn8175/xray-redactor
```
which should show the IP the server is hosted on

#### Postman Method

4. In the Postman Desktop App, setup a new request to the IP above
5. Change the request type to POST
6. Click body in the navigation bar of that request, and click "form-data". 
7. Include a file with the key "file" that is a picture with text of the form jpg, jpeg, or png. It should look something like the picture below
![example request](https://i.imgur.com/T0iCBLI.png)
8. Send the request and you should receive a JSON of the aforementioned format described in the description. An example is below
```json
{
  "boxes": [
    [
      364,
      15,
      505,
      46
    ],
    [
      1,
      16,
      183,
      62
    ],
    [
      358,
      462,
      519,
      496
    ],
    [
      2,
      415,
      107,
      495
    ]
  ],
  "text": [
    "NAME NAME\nNAME MEDICAL SYSTEMS.\n\f",
    "NAME, M, 129838\n927, 721389\nFr: 4, WL: 40, WW: 400\n\f",
    "1091 ms\nOFOV: 360.000000 mm\n\f",
    "LightSpeedUltra,\nkv: 120\n\nmA: 40\n\n5.000000 mm\nTilt: 0.000000\n\f"
  ]
}
```

#### curl Method
4. CD to the directory that holds the file you wish to send to the program
5. Send a command in the form
```
curl -X POST -F "file=@<filename>" localhost:5000
```

## Without Docker
If you choose not to use Docker, install the required packages manually, pull from the repository, run server.py, and continue from Step 3 above.

## Building Docker Container
After pulling from the repository, cd to the directory and run
```
docker build -t python-redactor .
```
To use the container when it is done building, follow from step 3 in the usage steps above.