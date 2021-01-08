from math import hypot
import cv2
# import time
import numpy as np


def round_nearest(x, base):
    return base * round(x / base)


# Source: https://github.com/jrosebr1/imutils/blob/master/imutils/object_detection.py
def non_max_suppression(boxes, probs=None, overlapThresh=0.3):
    # if there are no boxes, return an empty list
    if len(boxes) == 0:
        return []

    # if the bounding boxes are integers, convert them to floats -- this
    # is important since we'll be doing a bunch of divisions
    if boxes.dtype.kind == "i":
        boxes = boxes.astype("float")

    # initialize the list of picked indexes
    pick = []

    # grab the coordinates of the bounding boxes
    x1 = boxes[:, 0]
    y1 = boxes[:, 1]
    x2 = boxes[:, 2]
    y2 = boxes[:, 3]

    # compute the area of the bounding boxes and grab the indexes to sort
    # (in the case that no probabilities are provided, simply sort on the
    # bottom-left y-coordinate)
    area = (x2 - x1 + 1) * (y2 - y1 + 1)
    idxs = y2

    # if probabilities are provided, sort on them instead
    if probs is not None:
        idxs = probs

    # sort the indexes
    idxs = np.argsort(idxs)

    # keep looping while some indexes still remain in the indexes list
    while len(idxs) > 0:
        # grab the last index in the indexes list and add the index value
        # to the list of picked indexes
        last = len(idxs) - 1
        i = idxs[last]
        pick.append(i)

        # find the largest (x, y) coordinates for the start of the bounding
        # box and the smallest (x, y) coordinates for the end of the bounding
        # box
        xx1 = np.maximum(x1[i], x1[idxs[:last]])
        yy1 = np.maximum(y1[i], y1[idxs[:last]])
        xx2 = np.minimum(x2[i], x2[idxs[:last]])
        yy2 = np.minimum(y2[i], y2[idxs[:last]])

        # compute the width and height of the bounding box
        w = np.maximum(0, xx2 - xx1 + 1)
        h = np.maximum(0, yy2 - yy1 + 1)

        # compute the ratio of overlap
        overlap = (w * h) / area[idxs[:last]]

        # delete all indexes from the index list that have overlap greater
        # than the provided overlap threshold
        idxs = np.delete(idxs, np.concatenate(([last],
                                               np.where(overlap > overlapThresh)[0])))

    # return only the bounding boxes that were picked
    return boxes[pick].astype("int")


net = cv2.dnn.readNet("frozen_east_text_detection.pb")
layerNames = [
    "feature_fusion/Conv_7/Sigmoid",
    "feature_fusion/concat_3"]
"""
# to access an image in the UTILITIES folder, do './utilities/image_name'
timeStart = time.time()
image = cv2.imread('./utilities/test_image.jpg')
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

boxes = non_max_suppression(np.array(rects), probs=confidences).tolist()

distance_limit = 40

"""


def merge_boxes(box1, box2):
    return [min(box1[0], box2[0]),
            min(box1[1], box2[1]),
            max(box1[2], box2[2]),
            max(box1[3], box2[3])]


def calc_dist(box1, box2):
    return hypot(min(abs(box1[0] - box2[0]), abs(box1[0] - box2[2]), abs(box1[2] - box2[0]), abs(box1[2] - box2[2])),
                 min(abs(box1[1] - box2[1]), abs(box1[1] - box2[3]), abs(box1[3] - box2[1]), abs(box1[3] - box2[3])))


def merge(bounding_boxes, distance_limit):
    for i, box1 in enumerate(bounding_boxes):
        for j, box2 in enumerate(bounding_boxes):
            if j <= i: continue
            if calc_dist(box1, box2) < distance_limit:
                new_box = merge_boxes(box1, box2)
                bounding_boxes[i] = new_box
                del bounding_boxes[j]
                return True, bounding_boxes
    return False, bounding_boxes


def get_bounding_boxes(image):
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    height, width = image.shape[:2]
    # EAST only takes images with dimensions of multiples of 32
    height, width = round_nearest(height, 32), round_nearest(width, 32)
    image = cv2.resize(image, (width, height))
    blob = cv2.dnn.blobFromImage(image, 1.0, (width, height), (123.68, 116.78, 103.94), swapRB=True, crop=False)
    net.setInput(blob)
    scores, geometry = net.forward(layerNames)
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
            endX = max(int(offsetX + (cos * xData1[x]) + (sin * xData2[x])), 0)
            endY = max(int(offsetY - (sin * xData1[x]) + (cos * xData2[x])), 0)
            startX = max(int(endX - w), 0)
            startY = max(int(endY - h), 0)

            # add the bounding box coordinates and probability score to
            # our respective lists
            rects.append((startX, startY, endX, endY))
            confidences.append(scoresData[x])

    boxes = non_max_suppression(np.array(rects), probs=confidences).tolist()

    distance_limit = 40
    merging = True
    while merging:
        merging, boxes = merge(boxes, distance_limit)

    return boxes


def crop_image(image, startX, startY, endX, endY):
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    buffer_pixels_x = int(image.shape[1] / 100)
    buffer_pixels_y = int(image.shape[0] / 100)
    bounds_check = list(
        map(lambda x: max(x, 0), [startX - buffer_pixels_x, startY - buffer_pixels_y, endX + buffer_pixels_x,
                                  endY + buffer_pixels_y]))
    bounds_check = [min(bounds_check[0], image.shape[1]), min(bounds_check[1], image.shape[0]),
                    min(bounds_check[2], image.shape[1]), min(bounds_check[3], image.shape[0])]
    return image[bounds_check[1]:bounds_check[3],
           bounds_check[0]:bounds_check[2]]

# merging = True
# while merging:
#     merging, boxes = merge(boxes)

# for (startX, startY, endX, endY) in boxes:
#     cv2.rectangle(image, (startX, startY), (endX, endY), (0, 0, 255), -1)

# timeEnd = time.time()
# cv2.imwrite('./utilities/after.png', image)
# print("[INFO] detection and drawing took {:.6f} seconds".format(timeEnd - timeStart))
