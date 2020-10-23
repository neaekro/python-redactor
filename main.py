import cv2
import time
import numpy as np
from imutils.object_detection import non_max_suppression


def round_nearest(x, base):
    return base * round(x / base)


image = cv2.imread('test_image.jpg')
height, width = image.shape[:2]
# EAST only takes images with dimensions of multiples of 32
height, width = round_nearest(height, 32), round_nearest(width, 32)
image = cv2.resize(image, (width, height))
net = cv2.dnn.readNet("frozen_east_text_detection.pb")

# The first layer is our output sigmoid activation which gives us the probability of a region containing text or not.
# The second layer is the output feature map that represents the “geometry” of the image — we’ll be able to use this
# geometry to derive the bounding box coordinates of the text in the input image
layerNames = [
    "feature_fusion/Conv_7/Sigmoid",
    "feature_fusion/concat_3"]
# Specifies the mean to be subtracted from the image that was used to train the model
blob = cv2.dnn.blobFromImage(image, 1.0, (width, height),
                             (123.68, 116.78, 103.94), swapRB=True, crop=False)
start = time.time()
net.setInput(blob)
scores, geometry = net.forward(layerNames)
end = time.time()
print("[INFO] text detection took {:.6f} seconds".format(end - start))

(numRows, numCols) = scores.shape[2:4]
rects = []
confidences = []
minimum_confidence = 0.5

for y in range(0, numRows):
    # extract the scores (probabilities), followed by the geometrical
    # data used to derive potential bounding box coordinates that
    # surround text
    scoresData = scores[0, 0, y]
    xData0 = geometry[0, 0, y]
    xData1 = geometry[0, 1, y]
    xData2 = geometry[0, 2, y]
    xData3 = geometry[0, 3, y]
    anglesData = geometry[0, 4, y]

    # loop over the number of columns
    for x in range(0, numCols):
        # if our score does not have sufficient probability, ignore it
        if scoresData[x] < minimum_confidence:
            continue

        # compute the offset factor as our resulting feature maps will
        # be 4x smaller than the input image
        (offsetX, offsetY) = (x * 4.0, y * 4.0)

        # extract the rotation angle for the prediction and then
        # compute the sin and cosine
        angle = anglesData[x]
        cos = np.cos(angle)
        sin = np.sin(angle)

        # use the geometry volume to derive the width and height of
        # the bounding box
        h = xData0[x] + xData2[x]
        w = xData1[x] + xData3[x]

        # compute both the starting and ending (x, y)-coordinates for
        # the text prediction bounding box
        endX = int(offsetX + (cos * xData1[x]) + (sin * xData2[x]))
        endY = int(offsetY - (sin * xData1[x]) + (cos * xData2[x]))
        startX = int(endX - w)
        startY = int(endY - h)

        # add the bounding box coordinates and probability score to
        # our respective lists
        rects.append((startX, startY, endX, endY))
        confidences.append(scoresData[x])

boxes = non_max_suppression(np.array(rects), probs=confidences)

for (startX, startY, endX, endY) in boxes:
    cv2.rectangle(image, (startX, startY), (endX, endY), (0, 0, 255), -1)

cv2.imwrite('test_result.jpg', image)
cv2.imshow('test_result.jpg', image)
cv2.waitKey(0)