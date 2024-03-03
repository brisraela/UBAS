import torch
import numpy as np
import cv2
from ultralytics import YOLO

model = YOLO('yolov8m.pt')

global people
global baggage
global matches

matches = {}

# saves the 2 types of coordinates in 2 lists (ppl + bags)
def take_coordinate(result):
    global people
    global baggage

    list = result
    print("Class: ", result[1])
    if result[1] == 0:
        # [coordinates, class, confidence, id]
        people.append(result)
    elif result[1] == 24 or result[1] == 26 or result[1] == 28:
        list += [-1, -1]
        # [x1, y1,x2, y2] , class, confidence, box id, owner id, Max overlap
        baggage.append(list)


def filterResults(results):
    filteredResults = []
    # only save ppl & baggage
    for r in results:
        if int(r[1]) == 0 or int(r[1]) == 24 or int(r[1]) == 26 or int(r[1]) == 28:
            filteredResults.append(r)
    return filteredResults


def resultsToList(results):
    rList = []
    # get the lists of
    boxes = results[0].boxes.xyxy.tolist()
    classes = results[0].boxes.cls.tolist()
    confidence = results[0].boxes.conf.tolist()
    track_ids = results[0].boxes.id
    if track_ids != None:
        track_ids.tolist()
        print("Track IDs: ", track_ids)

        result = []

        for i in range(len(classes)):
            result.append(boxes[i])
            result.append(classes[i])
            result.append(confidence[i])
            result.append(track_ids[i])

            rList.append(result)
            result = []

    return rList


# returns area of intersection between person and bag
def find_intersection(bag, person):
    # Calculate intersection coordinates
    x1_intersect = max(bag[0], person[0])
    y1_intersect = max(bag[1], person[1])
    x2_intersect = min(bag[2], person[2])
    y2_intersect = min(bag[3], person[3])

    area = (x2_intersect - x1_intersect) * (y2_intersect - y1_intersect)
    print(area)
    if area < 0:
        return -1
    else:
        return area


# updates which bags belong to which people
def match_by_maxOverlap(baggage, people):
    global matches
    # find overlap between all bags and ppl
    for i in baggage:
        for j in people:
            overlap = find_intersection(i[0], j[0])
            print(overlap)
            # if current overlap is bigger than saved overlap
            if i[5] < overlap:
                # save this as new overlap
                i[5] = overlap
                # save owner id
                i[4] = j[3]
            matches[i[3]] = [j[3], i[3]]


# Draw on image the bounding boxes around items
def drawBoxes(resultList, image):
    # Dictionary of class labels
    label = {0: "person", 24: "backpack", 26: "handbag", 28: "suitcase"}

    # Draw bounding boxes on the copy of the image
    for r in resultList:
        objType = (int(r[1]))
        print("Object info: ", r)
        confidence = "{:.2f}".format(r[2])
        class_label = label.get(objType, "Unknown")

        color = (0, 0, 0)  # black
        print("Color type: ", type(color))
        if objType != 0: # if it's baggage
            if r[5] == -1:  # with no overlap
                color = (0, 0, 255)  # red


        # Get text size
        text_size, baseline = cv2.getTextSize(f"{class_label}: {confidence}", cv2.FONT_HERSHEY_SIMPLEX, 1.25, 3)

        # Draw filled rectangle as background
        cv2.rectangle(image, (int(r[0][0]), int(r[0][1]) - text_size[1] - 5),
                      (int(r[0][0]) + text_size[0], int(r[0][1]) - 5), color, -1)

        cv2.rectangle(image, (int(r[0][0]), int(r[0][1])), (int(r[0][2]), int(r[0][3])), color, 5)
        cv2.putText(image, f"{class_label}: {confidence}", (int(r[0][0]), int(r[0][1]) - 5),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)


def analysis(frame):
    global baggage
    global people
    global matches

    baggage = []
    people = []

    '''
    In each frame, we will reset the people, baggage lists to zero, as they hold the coordinates of each item
    In the matches list, we will place the id's of bags & owners, but we won't reset it at each frame
    Only remove the bags & owners who aren't in the frame anymore (both aren't in frame anymore)
    '''

    # Create 2 copies of the original image to draw bounding boxes on (all objects and selected objects)
    fullDetect = frame.copy()
    selectedDetect = frame.copy()

    # Find all objects in image using model
    results = model.track(source=fullDetect, show=False, tracker="bytetrack.yaml")

    # turn into a list of results instead of tensor
    resLists = resultsToList(results)

    # Filter results for people, backpacks, suitcases, handbags
    # (class indices: 0 - person, 24 - backpack, 26 - handbag, 28 - suitcase)
    filtered_results = filterResults(resLists)

    for r in filtered_results:
        take_coordinate(r)

    match_by_maxOverlap(baggage, people)

    drawBoxes(baggage, selectedDetect)
    drawBoxes(people, selectedDetect)

    # Display the image with filtered bounding boxes
    #cv2.imshow('Selected Detection', selectedDetect)

    print(baggage)
    if any(bag[5] == -1 for bag in baggage):
        return (False,selectedDetect)
    else:
        return (True,selectedDetect)