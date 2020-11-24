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
# to access an image in the UTILITIES folder, do './utilities/image_name'
filename = './utilities/xray_snip_2.png'
image = cv2.imread(filename)
# height, width = image.shape[0], image.shape[1]

# print('Image Height: ', height)
# print('Image Width: ', width)
# print(type(image))

def preprocess_image(image):
    assert type(image) is np.ndarray, "pass in an image pls"
    kernel = np.ones((1,1), np.uint8)

    # convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # threshold image
    thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)[1]

    # adaptive threshold (this is a work in progres don't use)
    # thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 2)

    # OpenCV's opening and erosion methods to try and increase the fidelity of the thresholded image. does not seem to have noticable impact, explore.
    # opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
    # erosion = cv2.erode(thresh, kernel, iterations = 1)

    # By default OpenCV stores images in BGR format and since pytesseract assumes RGB format,
    # we need to convert from BGR to RGB format/mode:
    
    # this is actually unnecessary for grayscaled images i think but not sure
    # img_rgb = cv2.cvtColor(thresh, cv2.COLOR_BGR2RGB)
    
    print("Image preprocess successfully finished.\n")

    return thresh

def redact_character(image, top_left, bottom_right, color):
    redacted_image = cv2.rectangle(image, top_left, bottom_right, color, thickness=1)
    return redacted_image


preprocessed = preprocess_image(image)
preprocessed_text = pytesseract.image_to_string(preprocessed)

print(preprocessed_text)
cv2.imshow("preprocessed {image} (PRESS ANY KEY TO CLOSE)".format(image = filename), preprocessed)
# cv2.imwrite('test_result.png', preprocessed)
cv2.waitKey(0)