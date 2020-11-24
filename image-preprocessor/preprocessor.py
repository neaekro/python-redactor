import cv2
import numpy as np
import pytesseract

# pytesseract.pytesseract.tesseract_cmd = "/bin/tesseract"

"""
Steps:
1. Use OpenCV to preprocess the image
    1.1 Convert the image to grayscale
    1.2 Use the grayscaled image and threshold it (step removed)
2. Pass the preprocessed image to tesseract and have it return text bounding box data
3. Use OpenCV to draw text and redact the bounding box data

TODO next sprint:
1. Manually crop out the text from image
2. Feed into tesseract
3. See if the info is accurate
"""

# load image file and get info
# uncomment the line for the type of image you want to try with
# image = cv2.imread('xray.jpg')
# image = cv2.imread('xray_upscaled_2x.jpg')
# image = cv2.imread('xray_upscaled_4x.jpg')
# height, width = image.shape[0], image.shape[1]

# print('Image Height: ', height)
# print('Image Width: ', width)
# print(type(image))

def preprocess_image(image):
    assert type(image) is np.ndarray, "pass in an image pls"

    # convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # threshold image
    # thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)[1]

    # By default OpenCV stores images in BGR format and since pytesseract assumes RGB format,
    # we need to convert from BGR to RGB format/mode:
    
    # this is actually unnecessary for grayscaled images i think but not sure
    img_rgb = cv2.cvtColor(gray, cv2.COLOR_BGR2RGB)
    
    # print("Image preprocess successfully finished.")

    return img_rgb

def redact_character(image, top_left, bottom_right, color):
    redacted_image = cv2.rectangle(image, top_left, bottom_right, color, thickness=1)
    return redacted_image

"""
preprocessed = preprocess_image(image)
preprocessed_text = pytesseract.image_to_string(preprocessed)
# print(preprocessed_text)

# convert the data read by pytesseract into dictionary format
data = pytesseract.image_to_data(preprocessed, output_type=pytesseract.Output.DICT)
# print(data['conf'])
# print(data['text'])

bounds = len(data['level'])
# print(bounds)

for i in range(bounds):
    # arbitrarily chosen confidence for testing purposes
    if int(data['conf'][i]) >= 90:
        top_left = (data['left'][i], data['top'][i])
        bottom_right = (data['width'][i], data['height'][i])
        # print("text: ", data['text'][i])
        # print("top_left: ", top_left)
        # print("bottom_right: ", bottom_right)
        redact_character(preprocessed, top_left, bottom_right, (255))

# cv2.imshow("redacted (CLOSE WINDOW BY HITTING ANY KEY)", preprocessed)
# cv2.waitKey(0)
"""