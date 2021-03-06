import cv2
import numpy as np

cap = cv2.VideoCapture(0)
accumulator_frame = None
img_counter = 0

while True:
    ret, frame = cap.read()
    fs = frame.shape
    flipped = cv2.flip(frame, 1)
    mask = cv2.inRange(flipped, (0, 0, 0), (47, 49, 51))
    masked_input = cv2.bitwise_and(flipped, flipped, mask=mask)
    if accumulator_frame is None:
        accumulator_frame = np.ones(fs, dtype=np.uint8) * 255

    # BLOB DETECTION
    p = cv2.SimpleBlobDetector_Params()
    p.filterByColor = False
    p.filterByConvexity = False
    p.filterByArea = True
    p.minArea = 500
    detector = cv2.SimpleBlobDetector_create(p)
    key_points = detector.detect(mask)

    if key_points:
        pt = key_points[0].pt
        # Clear out accumulator_frame
        if pt[0] < 140 and pt[1] < 30:
            accumulator_frame[:, :, :] = 0
        # Takes and saves pictures from accumulator_frame           PUT IN A DELAY?
        if pt[0] > 540 and pt[1] < 30:
            img_name = "opencv_frame_{}.png".format(img_counter)
            cv2.imwrite(img_name, accumulator_frame)
            print("{} saved!".format(img_name))
            img_counter += 1

        # COLOR COORDINATION
        if pt[0] < 325 and pt[1] < 250:
            cv2.circle(accumulator_frame, (round(pt[0]), round(pt[1])), 10, (0, 0, 255), -1)  # BLUE
        if pt[0] > 325 and pt[1] < 250:
            cv2.circle(accumulator_frame, (round(pt[0]), round(pt[1])), 10, (255, 0, 0), -1)  # RED
        if pt[0] < 325 and pt[1] > 250:
            cv2.circle(accumulator_frame, (round(pt[0]), round(pt[1])), 10, (255, 255, 0), -1)  # YELLOW
        if pt[0] > 325 and pt[1] > 250:
            cv2.circle(accumulator_frame, (round(pt[0]), round(pt[1])), 10, (0, 255, 0), -1)  # GREEN

    # BUTTONS
    accumulator_frame = cv2.rectangle(accumulator_frame, (0, 0), (140, 30), (122, 122, 122), -1)
    accumulator_frame = cv2.rectangle(accumulator_frame, (540, 0), (650, 30), (122, 122, 122), -1)

    # TEXT
    cv2.putText(accumulator_frame, "Clear painting", (10, 20), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255))
    cv2.putText(accumulator_frame, "Save me!", (552, 20), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255))
    cv2.putText(flipped, "Find something black and try to paint!", (5, 22), cv2.FONT_HERSHEY_PLAIN, 1.7, (0, 0, 0))

    # FRAMES
    cv2.imshow('Webcam', flipped)
    cv2.imshow('Detect', mask)
    cv2.imshow('Paint', accumulator_frame)

    # KEYPRESS
    if cv2.waitKey(1) % 256 == 27:  # Esc key
        break
    elif cv2.waitKey(1) == ord('s'):  # S key
        img_name = "opencv_frame_{}.png".format(img_counter)
        cv2.imwrite(img_name, accumulator_frame)
        print("{} saved!".format(img_name))
        img_counter += 1

cap.release()
cv2.destroyAllWindows()
