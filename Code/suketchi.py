import cv2
import numpy as np
import time
import os
import hand_tracking_module as htm

header_path = './UI/Header Selection'
header_list = os.listdir(header_path)
# print(header_list)

stroke_size_path = './UI/Stroke Size Selection'
stroke_size_list = os.listdir(stroke_size_path)
# # print(stroke_size_list)

header_overlay_list = []

stroke_size_overlay_list = []

for im_path in header_list:
    image = cv2.imread(f'{header_path}/{im_path}')
    header_overlay_list.append(image)
# print(len(header_overlay_list))

for im_path in stroke_size_list:
    image = cv2.imread(f'{stroke_size_path}/{im_path}')
    stroke_size_overlay_list.append(image)
# print(len(stroke_size_overlay_list))

header = header_overlay_list[0]
stroke_side = stroke_size_overlay_list[2]

# print(header.shape)

# BGR Values for the colors
red = (9, 9, 240)
dark_red = (44, 5, 173)
brown = (37, 67, 101)
orange = (5, 138, 247)
yellow = (10, 247, 247)
flu_green = (2, 254, 120)
green = (35, 189, 15)
dark_green = (8, 120, 57)
blue = (245, 197, 5)
dark_blue = (196, 69, 19)
pink = (195, 33, 235)
violet = (158, 19, 135)
white = (240, 246, 250)
color = red

brush_thickness = 18
eraser_thickness = 54


x_prev, y_prev = 0, 0

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

img_canvas = np.zeros((720, 1280, 3), np.uint8)
img_white_screen = 255 * np.ones((720, 1280, 3), np.uint8)

detector = htm.handDetector(detection_confidence=0.85)

while True:
    # 1. Import Image
    success, webcam_img = cap.read()
    webcam_img  = cv2.flip(webcam_img , 1) # To avoid the mirror effect

    # 2. Tracking hand Landmarks
    webcam_img  = detector.findHands(webcam_img )
    landmark_list = detector.findLandmarkPosition(webcam_img , draw=False)

    if len(landmark_list) != 0:
        # print(landmark_list)
       
        # Tip of the index finger
        x1, y1 = landmark_list[8][0:]

         # Tip of the middle finger
        x2, y2 = landmark_list[12][0:]

        # 3. Check Finger count
        fingers = detector.fingersUp()
        print(fingers)
        # 4. Selection Mode - Two fingers
        if fingers[1] and fingers[2]:
            x_prev, y_prev = 0, 0
            # Checking for the click
            if y1 < 100:
                if 149 < x1 < 213:
                    header = header_overlay_list[0]
                    color = red
                elif 237 < x1 < 299:
                    header = header_overlay_list[1]
                    color = dark_red
                elif 317 < x1 < 377:
                    header = header_overlay_list[2]
                    color = brown
                elif 394 < x1 <458:
                    header = header_overlay_list[3]
                    color = orange
                elif 475 < x1 < 528:
                    header = header_overlay_list[4]
                    color = yellow
                elif 553 < x1 < 614:
                    header = header_overlay_list[5]
                    color = flu_green
                elif 633 < x1 < 694:
                    header = header_overlay_list[6]
                    color = green
                elif 710 < x1 < 773:
                    header = header_overlay_list[7]
                    color = dark_green
                elif 791 < x1 < 852:
                    header = header_overlay_list[8]
                    color = blue
                elif 871 < x1 < 933:
                    header = header_overlay_list[9]
                    color = dark_blue
                elif  948 < x1 < 1012:
                    header = header_overlay_list[10]
                    color = pink
                elif 1028 < x1 < 1090:
                    header = header_overlay_list[11]
                    color = violet
                elif 1106 < x1 < 1168:
                    header = header_overlay_list[12]
                    color = white
                elif 1181 < x1 < 1250:
                    header = header_overlay_list[13]
                    color = (0, 0, 0)
                else:
                    pass
            elif x1 < 100:
                if 104 < y1 < 172:
                    stroke_side = stroke_size_overlay_list[0]
                    brush_thickness = 10
                    eraser_thickness = brush_thickness*3
                elif 180 < y1 < 257:
                    stroke_side = stroke_size_overlay_list[1]
                    brush_thickness = 14
                    eraser_thickness = brush_thickness*3
                elif 277 < y1 < 363:
                    stroke_side = stroke_size_overlay_list[2]
                    brush_thickness = 18
                    eraser_thickness = brush_thickness*3
                elif 373 < y1 < 466:
                    stroke_side = stroke_size_overlay_list[3]
                    brush_thickness = 22
                    eraser_thickness = brush_thickness*3
                elif 486 < y1 < 588:
                    stroke_side = stroke_size_overlay_list[4]
                    brush_thickness = 26
                    eraser_thickness = brush_thickness*3
                else:
                    pass
            cv2.rectangle(webcam_img, (x1, y1-15), (x2, y2+15),color,cv2.FILLED)
        # 5. Drawing Mode - Index finger
        if fingers[1] and fingers[2] == False:
            cv2.circle(webcam_img,(x1,y1),15,color,cv2.FILLED)
            # print('Drawing Mode')
            if x_prev ==0 and y_prev == 0:
                x_prev, y_prev = x1, y1
            if color == (0, 0, 0):
                cv2.line(webcam_img, (x_prev,y_prev), (x1,y1), color,eraser_thickness)
                cv2.line(img_canvas, (x_prev,y_prev), (x1,y1), color,eraser_thickness)
                cv2.line(img_white_screen, (x_prev,y_prev), (x1,y1), color,eraser_thickness)
            else:
                cv2.line(webcam_img, (x_prev,y_prev), (x1,y1), color,brush_thickness)
                cv2.line(img_canvas, (x_prev,y_prev), (x1,y1), color,brush_thickness)
                cv2.line(img_white_screen, (x_prev,y_prev), (x1,y1), color,brush_thickness)
            x_prev, y_prev = x1, y1

    # Merging images onto Web Cam
    img_gray = cv2.cvtColor(img_canvas, cv2.COLOR_BGR2GRAY)
    _, img_inv = cv2.threshold(img_gray, 50, 255, cv2.THRESH_BINARY_INV)
    img_inv = cv2.cvtColor(img_inv, cv2.COLOR_GRAY2BGR)
    webcam_img = cv2.bitwise_and(webcam_img, img_inv)
    webcam_img = cv2.bitwise_or(webcam_img, img_canvas)


    # Setting the header image
    webcam_img[0:100,0:1280] = header
    webcam_img[100:720,0:100] = stroke_side

    cv2.imshow("Suketchi", webcam_img)
    cv2.imshow("Canvas", img_white_screen)

    if cv2.waitKey(1) & 0xff == ord('q'):
        break

cv2.destroyAllWindows()
