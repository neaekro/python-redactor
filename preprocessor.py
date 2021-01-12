import cv2
import numpy as np
import pytesseract

# pytesseract.pytesseract.tesseract_cmd = "/bin/tesseract"

# load image file and get info
# to access an image in the UTILITIES folder, do './utilities/image_name'
# or input the path to the image for FILENAME
filename = './utilities/levine_joshua_2.jpg'
# filename = './utilities/xray.jpg'
image = cv2.imread(filename)

"""
height, width = image.shape[0], image.shape[1]
print('Image Height: ', height)
print('Image Width: ', width)
print(type(image))
"""

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

    # Gaussian adaptive threshold (this is a work in progres)
    # result = cv2.adaptiveThreshold(result, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

    # threshold image and inverse b/w (this works okay if you use it by itself after the grayscale and return it)
    result = cv2.threshold(result, 137, 255, cv2.THRESH_BINARY_INV)[1]

    # Otsu's method adaptive threshold (another work in progress)
    blur = cv2.GaussianBlur(result, (5,5), 0)
    result = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1]

    # print("Image preprocess successfully completed.\n")

    return result

def adjust_gamma(image, gamma=0.1):
    # i want this to activiate only with white on white images
    # build a lookup table mapping the pixel values [0, 255] to
    # their adjusted gamma values
    invGamma = 1.0 / gamma
    table = np.array([((i / 255.0) ** invGamma) * 255
        for i in np.arange(0, 256)]).astype("uint8")
    # apply gamma correction using the lookup table
    return cv2.LUT(image, table)

"""
def lab(image):
    lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    # cv2.imshow("lab", lab)

    l, a, b = cv2.split(lab)
    # cv2.imshow('l_channel', l)
    #cv2.imshow('a_channel', a)
    # cv2.imshow('b_channel', b)

    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
    cl = clahe.apply(l)
    # cv2.imshow('CLAHE output', cl)

    limg = cv2.merge((cl,a,b))
    # cv2.imshow('limg', limg)

    final = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)
    # cv2.imshow('final', final)
    return final
"""

def get_average_color(image):
    avg_color_per_row = np.average(image, axis=0)
    avg_color = np.average(avg_color_per_row, axis=0)
    return sum(avg_color)/3 # Averages the average B, G, R values of an image

def process(image):
    if (get_average_color(image) > 125):
        preprocessed = adjust_gamma(image)
    else: 
        preprocessed = preprocess_image(image)
    preprocessed_text = pytesseract.image_to_string(preprocessed)
    return preprocessed_text

"""
preprocessed_image = preprocess_image(image)
preprocessed_text = pytesseract.image_to_string(preprocessed_image)

print("Running Tesseract version:", pytesseract.get_tesseract_version())
print("--Start of Image Text--")
print(preprocessed_text)
print("--End of Image Text--")
print("Average Color [B, G, R]: ", get_average_color(image))

# cv2.imwrite('test_result.png', preprocessed)

# keeps the results open until the ESC key is pressed
while((cv2.waitKey() & 0xEFFFFF) != 27):
    cv2.imshow("(PRESS ESC TO CLOSE) preprocessed {image}".format(image = filename), preprocessed_image)
"""