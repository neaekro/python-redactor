import requests
import cv2
import numpy as np
import random
import textwrap

# select random dimensions between 512 and 2048 pixels, inclusive
width, height = random.randint(512, 2048), random.randint(512, 2048)
# print("Width:", width)
# print("Height:", height)

image = np.random.randint(255, size=(height, width, 3), dtype=np.uint8)
wrapped_text = textwrap.wrap("Hello World!", width=35)

font = cv2.FONT_HERSHEY_SIMPLEX
# coordinate = (random.randint(0, width), random.randint(150, height))
fontScale = 3
fontColor = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
lineType = 2

for i, line in enumerate(wrapped_text):
    textsize = cv2.getTextSize(line, font, fontScale, lineType)[0]

    gap = textsize[1] + 10

    y = int((image.shape[0] + textsize[1]) / 2) + i * gap
    x = int((image.shape[1] - textsize[0]) / 2)

    cv2.putText(image, "Hello World!", (x, y), font, fontScale, fontColor, lineType)

cv2.imwrite("random.jpg".format(width = width, height = height), image)
files = {'file': open('random.jpg', 'rb')}
r = requests.post('http://localhost:5000', files=files)
print(r.status_code)
print(r.text)