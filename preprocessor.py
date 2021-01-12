import cv2
import numpy as np
import pytesseract

# pytesseract.pytesseract.tesseract_cmd = "/bin/tesseract"

filename = './utilities/random.jpeg'
image = cv2.imread(filename)

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
    resized = cv2.resize(image, dimensions, interpolation = cv2.INTER_CUBIC)

    return resized

def preprocess_image(image):
    assert type(image) is np.ndarray, "pass in an image pls"
    result = resize_image(image, 200)
    result = convert_to_gray(result)

    # threshold image and inverse b/w
    result = cv2.threshold(result, 137, 255, cv2.THRESH_BINARY_INV)[1]

    # Otsu's method adaptive threshold
    blur = cv2.GaussianBlur(result, (5,5), 0)
    result = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1]

    return result

def adjust_gamma(image, gamma=0.1):
    # build a lookup table mapping the pixel values [0, 255] to their adjusted gamma values
    invGamma = 1.0 / gamma
    table = np.array([((i / 255.0) ** invGamma) * 255
        for i in np.arange(0, 256)]).astype("uint8")
    
    # apply gamma correction using the lookup table
    return cv2.LUT(image, table)

def get_average_color(image):
    avg_color_per_row = np.average(image, axis=0)
    avg_color = np.average(avg_color_per_row, axis=0)
    
    return sum(avg_color)/3

def process(image):
    if (get_average_color(image) > 125):
        preprocessed = adjust_gamma(image)
    else: 
        preprocessed = preprocess_image(image)
    preprocessed_text = pytesseract.image_to_string(preprocessed)

    return preprocessed_text