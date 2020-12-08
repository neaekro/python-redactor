import cv2
import numpy as np
import pytesseract

# pytesseract.pytesseract.tesseract_cmd = "/bin/tesseract"

# load image file and get info
# to access an image in the UTILITIES folder, do './utilities/image_name'
# or input the path to the image for FILENAME
filename = './utilities/xray_snip_1.png'
image = cv2.imread(filename)
# height, width = image.shape[0], image.shape[1]
# print('Image Height: ', height)
# print('Image Width: ', width)
# print(type(image))

def convert_to_gray(image):
    # convert from bgr to rgb
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # convert to grayscale
    gray = cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY)

    return gray

def resize_image(image, factor):
    width = int(image.shape[1] * factor / 100)
    height = int(image.shape[0] * factor / 100)
    dimensions = (width, height)

    resized = cv2.resize(image, dimensions, interpolation = cv2.INTER_AREA)
    return resized

def preprocess_image(image):
    assert type(image) is np.ndarray, "pass in an image pls"
    result = resize_image(image, 220)
    result = convert_to_gray(result)

    # Gaussian adaptive threshold (this is a work in progres)
    # result = cv2.adaptiveThreshold(result, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

    # threshold image and inverse b/w (this works okay if you use it by itself after the grayscale and return it)
    result = cv2.threshold(result, 137, 255, cv2.THRESH_BINARY_INV)[1]

    # Otsu's method adaptive threshold (another work in progress)
    blur = cv2.GaussianBlur(result, (5,5), 0)
    result = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1]

    print("Image preprocess successfully completed.\n")

    return result

def process(image):
    preprocessed = preprocess_image(image)
    preprocessed_text = pytesseract.image_to_string(preprocessed)
    return preprocessed_text

"""
print("Running Tesseract version: ", pytesseract.get_tesseract_version())
print("--Start of Image Text--")
print(preprocessed_text)
print("--End of Image Text--")

# cv2.imwrite('test_result.png', preprocessed)

# keeps the results open until the ESC key is pressed
while((cv2.waitKey() & 0xEFFFFF) != 27):
    cv2.imshow("(PRESS ESC TO CLOSE) preprocessed {image}".format(image = filename), preprocessed)
"""
