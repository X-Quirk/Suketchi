import cv2
import numpy as np
from datetime import datetime
import os
import hand_tracking_module as htm
import playsound as ps
import threading

# Paths for Audio Files
intro_audio_path = './Assets/Audio/Player_boost_recharging.wav'
color_change_audio_path = './Assets/Audio/Player_jumping_in_a_video_game_trimmed.wav'
stroke_size_audio_path = './Assets/Audio/Sci_fi_Positive_Notification_trimmed.wav'
clear_screen_audio_path = './Assets/Audio/Owl_Hoot_trimmed.wav'

# Functions to play sound effects
def play_intro():
    ps.playsound(intro_audio_path)

def play_color_change():
    ps.playsound(color_change_audio_path)

def play_stroke_size_change():
    ps.playsound(stroke_size_audio_path)

def play_clear_screen():
    ps.playsound(clear_screen_audio_path)

# Functions to create threads to play sound asynchronously
def sound_color_change():
    threading.Thread(target=play_color_change, daemon=True).start()

def sound_stroke_size_change():
    threading.Thread(target=play_stroke_size_change, daemon=True).start()

# Function to Export Saved Images
def save_image(img):
     now = datetime.now()
     try:
        if os.path.exists("./Saves") :
        # Change the current working Directory    
            os.chdir("./Saves")
            print("Directory changed")
            cv2.imwrite('{}-{}-{} {}_{}_{} White Board'.format(
                now.day,now.month,now.year,now.hour,now.minute,now.second
                )+'.png',img)
     except OSError:
        print("Error Occured while Switching Directories")

def sound_clear_screen():
    threading.Thread(target=play_clear_screen, daemon=True).start()

# Paths for UI
header_path = './UI/Header Selection'
header_list = os.listdir(header_path)
# print(header_list)

stroke_size_path = './UI/Stroke Size Selection'
stroke_size_list = os.listdir(stroke_size_path)
# # print(stroke_size_list)

# Lists to store diffrent UI elements
header_overlay_list = []
stroke_size_overlay_list = []

# Reading images from the list and storing them in another list
for im_path in header_list:
    image = cv2.imread(f'{header_path}/{im_path}')
    header_overlay_list.append(image)
# print(len(header_overlay_list))

for im_path in stroke_size_list:
    image = cv2.imread(f'{stroke_size_path}/{im_path}')
    stroke_size_overlay_list.append(image)
# print(len(stroke_size_overlay_list))

# Setting default images for UI
header = header_overlay_list[0]
stroke_side = stroke_size_overlay_list[2]

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

# Setting default color as red
color = red
# Setting eraser color as white for white board
eraser_color_for_board = (255, 255, 255)

# Setting default brush size and eraser size
brush_thickness = 18
eraser_thickness = 54

# Intialising x and y co-ordinates for drawing
x_prev, y_prev = 0, 0

# Setting window dimensions
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

# Creating canvases to draw on top of them
# For overlaying onto webcam
img_canvas = np.zeros((720, 1280, 3), np.uint8)
# For overlaying onto whiteboard
img_white_board = 255 * np.ones((720, 1280, 3), np.uint8)

# Creating object of hand_detection_module
detector = htm.handDetector(detection_confidence=0.85)

# Playing intro sound effect
play_intro()

while True:

    # 1. Import Image
    success, webcam_img = cap.read()
    webcam_img = cv2.flip(webcam_img, 1)  # To avoid the mirror effect

    # 2. Tracking hand Landmarks
    webcam_img = detector.findHands(webcam_img)
    landmark_list = detector.findLandmarkPosition(webcam_img, draw=False)

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

            # Checking for the click and change in color
            if y1 < 100:

                if 149 < x1 < 213:
                    header = header_overlay_list[0]
                    if color != red:
                        color = red
                        sound_color_change()

                elif 237 < x1 < 299:
                    header = header_overlay_list[1]
                    if color != dark_red:
                        color = dark_red
                        sound_color_change()

                elif 317 < x1 < 377:
                    header = header_overlay_list[2]
                    if color != brown:
                        color = brown
                        sound_color_change()

                elif 394 < x1 < 458:
                    header = header_overlay_list[3]
                    if color != orange:
                        color = orange
                        sound_color_change()

                elif 475 < x1 < 528:
                    header = header_overlay_list[4]
                    if color != yellow:
                        color = yellow
                        sound_color_change()

                elif 553 < x1 < 614:
                    header = header_overlay_list[5]
                    if color != flu_green:
                        color = flu_green
                        sound_color_change()

                elif 633 < x1 < 694:
                    header = header_overlay_list[6]
                    if color != green:
                        color = green
                        sound_color_change()

                elif 710 < x1 < 773:
                    header = header_overlay_list[7]
                    if color != dark_green:
                        color = dark_green
                        sound_color_change()

                elif 791 < x1 < 852:
                    header = header_overlay_list[8]
                    if color != blue:
                        color = blue
                        sound_color_change()

                elif 871 < x1 < 933:
                    header = header_overlay_list[9]
                    if color != dark_blue:
                        color = dark_blue
                        sound_color_change()

                elif 948 < x1 < 1012:
                    header = header_overlay_list[10]
                    if color != pink:
                        color = pink
                        sound_color_change()

                elif 1028 < x1 < 1090:
                    header = header_overlay_list[11]
                    if color != violet:
                        color = violet
                        sound_color_change()

                elif 1106 < x1 < 1168:
                    header = header_overlay_list[12]
                    if color != white:
                        color = white
                        sound_color_change()

                elif 1181 < x1 < 1250:
                    header = header_overlay_list[13]
                    if color != (0, 0, 0):
                        color = (0, 0, 0)
                        sound_color_change()

                elif 15 < x1 < 112:
                    if (np.sum(img_canvas) != 0):
                        img_canvas = np.zeros((720, 1280, 3), np.uint8)
                        img_white_board = 255 * np.ones((720, 1280, 3), np.uint8)
                        sound_clear_screen()
                    
                else:
                    pass

            # Checking for the click and change in stroke size
            elif x1 < 100:

                if 204 < y1 < 272:
                    stroke_side = stroke_size_overlay_list[0]
                    if brush_thickness != 10:
                        brush_thickness = 10
                        eraser_thickness = brush_thickness*3
                        sound_stroke_size_change()

                elif 280 < y1 < 357:
                    stroke_side = stroke_size_overlay_list[1]
                    if brush_thickness != 14:
                        brush_thickness = 14
                        eraser_thickness = brush_thickness*3
                        sound_stroke_size_change()

                elif 377 < y1 < 463:
                    stroke_side = stroke_size_overlay_list[2]
                    if brush_thickness != 18:
                        brush_thickness = 18
                        eraser_thickness = brush_thickness*3
                        sound_stroke_size_change()

                elif 473 < y1 < 566:
                    stroke_side = stroke_size_overlay_list[3]
                    if brush_thickness != 22:
                        brush_thickness = 22
                        eraser_thickness = brush_thickness*3
                        sound_stroke_size_change()

                elif 586 < y1 < 688:
                    stroke_side = stroke_size_overlay_list[4]
                    if brush_thickness != 26:
                        brush_thickness = 26
                        eraser_thickness = brush_thickness*3
                        sound_stroke_size_change()

                else:
                    pass

            cv2.rectangle(webcam_img, (x1, y1-15),
                          (x2, y2+15), color, cv2.FILLED)

        # 5. Drawing Mode - Index finger
        if fingers[1] and fingers[2] == False:
            cv2.circle(webcam_img, (x1, y1), 15, color, cv2.FILLED)
            # print('Drawing Mode')
            if x_prev == 0 and y_prev == 0:
                x_prev, y_prev = x1, y1
            if color == (0, 0, 0):
                cv2.line(webcam_img, (x_prev, y_prev),
                         (x1, y1), color, eraser_thickness)
                cv2.line(img_canvas, (x_prev, y_prev),
                         (x1, y1), color, eraser_thickness)
                cv2.line(img_white_board, (x_prev, y_prev), (x1, y1),
                         eraser_color_for_board, eraser_thickness)
            else:
                cv2.line(webcam_img, (x_prev, y_prev),
                         (x1, y1), color, brush_thickness)
                cv2.line(img_canvas, (x_prev, y_prev),
                         (x1, y1), color, brush_thickness)
                cv2.line(img_white_board, (x_prev, y_prev),
                         (x1, y1), color, brush_thickness)
            x_prev, y_prev = x1, y1

        # 6. Exporting Saved copy
        if fingers[0] and fingers[4] and fingers[1] == False and fingers[2]== False and fingers[3] == False :
            if (np.sum(img_canvas) != 0):
                save_image(img_white_board)
                img_canvas = np.zeros((720, 1280, 3), np.uint8)
                img_white_board = 255 * np.ones((720, 1280, 3), np.uint8)
        

    # Merging images onto Web Cam
    img_gray = cv2.cvtColor(img_canvas, cv2.COLOR_BGR2GRAY)
    _, img_inv = cv2.threshold(img_gray, 50, 255, cv2.THRESH_BINARY_INV)
    img_inv = cv2.cvtColor(img_inv, cv2.COLOR_GRAY2BGR)
    webcam_img = cv2.bitwise_and(webcam_img, img_inv)
    webcam_img = cv2.bitwise_or(webcam_img, img_canvas)

    # Setting the UI elements
    webcam_img[0:100, 0:1280] = header
    webcam_img[100:720, 0:100] = stroke_side

    # Displaying the windows
    cv2.imshow("Suketchi", webcam_img)
    cv2.imshow("White Board", img_white_board)

    # Refreshing images and condition for exiting
    if cv2.waitKey(1) & 0xff == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
