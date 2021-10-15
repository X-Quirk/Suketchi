import cv2 
import mediapipe as mp
import time

class handDetector():
    def __init__(self,
                 mode = False,
                 max_hands = 2,
                 detection_confidence = 0.5,
                 track_confidence =  0.5):
        self.mode = mode
        self.max_hands = max_hands
        self.detection_confidence = detection_confidence
        self.track_confidence = track_confidence

        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(self.mode,self.max_hands,
                                         self.detection_confidence,self.track_confidence)
        self.mp_draw = mp.solutions.drawing_utils # Drawing the line between two landmarks
        self.tip_ids = [4, 8, 12, 16, 20] # Landmark id of the tip of the fingers

    def findHands(self, img, draw = True):
        
        img_RGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) # Because mediapipe functions only take RGB Images
   
        self.results = self.hands.process(img_RGB)

        if self.results.multi_hand_landmarks:
            for hand_landmarks in self.results.multi_hand_landmarks:   
                if draw:   
                    # Detecting the landmarks and Drawing them
                    self.mp_draw.draw_landmarks(img,hand_landmarks,self.mp_hands.HAND_CONNECTIONS)         

        return img

    def findLandmarkPosition(self, img, hand_num=0, draw=True):
        self.landmark_list = {}

        if self.results.multi_hand_landmarks:
            hand = self.results.multi_hand_landmarks[hand_num]

            # Detecting postion of each landmark in x,y coordinates wrt height and width of image in pixels
            for id, landmark in enumerate(hand.landmark):
                #  print(id,landmark)
                height, width, channels = img.shape
                center_x,  center_y = int(landmark.x * width), int(landmark.y * height)
                self.landmark_list[id] = [center_x,center_y]
                if draw:
                    cv2.circle(img, (center_x,center_y),7,(0,255,0),cv2.FILLED) 
        return self.landmark_list

    def fingersUp(self):
        fingers = []

        # Detection for Thumb
        if self.landmark_list[self.tip_ids[0]][0] < self.landmark_list[self.tip_ids[0]-1][0]:  
                fingers.append(1) 
        else:
            fingers.append(0)
  
        # Detection for other fingers
        for id in range(1,5):
            if self.landmark_list[self.tip_ids[id]][1] < self.landmark_list[self.tip_ids[id]-2][1]: # Because top most value in opencv is lower 
                fingers.append(1)
            else:
                fingers.append(0)
        return fingers

                



def main():
    # For frame rates 
    prev_time = 0
    current_time = 0

    cap = cv2.VideoCapture(0)

    detector = handDetector()


    while True:
        success, img = cap.read()

        img = detector.findHands(img)
        landmark_list = detector.findLandmarkPosition(img)

        if len(landmark_list) != 0:
            print(landmark_list[4])

        current_time = time.time()
        fps = 1/(current_time-prev_time)
        prev_time = current_time

        cv2.putText(img, str(int(fps)),(10,70),cv2.FONT_HERSHEY_PLAIN,2,(255,0,0),2) # Viewing the fps

        cv2.imshow('Image', img)
    
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

if __name__ == '__main__':
    main()