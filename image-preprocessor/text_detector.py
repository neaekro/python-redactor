import cv2
import numpy as np
import pytesseract

# load image file and get info
# image = cv2.imread('xray.jpg')
# image = cv2.imread('xray_upscaled_2x.jpg')
image = cv2.imread('xray_upscaled_4x.jpg')
height, width = image.shape[0], image.shape[1] # 1600 x 1600 for 2x, 3000 x 3000 for 4x

print('Image Height: ', height)
print('Image Width: ', width)
# print(type(image))

"""
TODO:
1. Manually crop out the text from image
2. Feed into tesseract
3. See if the info is accurate
"""

