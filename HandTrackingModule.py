import cv2
import mediapipe as mp
import time

import PythonToFLStudioBridge as PTSB

class handDetector():
    def __init__(self, mode=False, maxHands=2, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon
        
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(static_image_mode = self.mode, 
                                        max_num_hands = self.maxHands,
                                        min_detection_confidence = self.detectionCon, 
                                        min_tracking_confidence = self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        #print(results.multi_hand_landmarks)
        
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw: self.mpDraw.draw_landmarks(img, handLms, 
                                                    self.mpHands.HAND_CONNECTIONS)
        return img

    def findPosition(self, img, handNo=0, draw=True):
        
        height, width, _ = img.shape
        center_x, center_y = width // 2, height // 2
        cv2.line(img, (center_x, 0), (center_x, height), (0, 255, 0), 2)  # Y-axis
        cv2.line(img, (0, center_y), (width, center_y), (255, 0, 0), 2)  # X-axis

        # Display the min and max coordinates for the axes
        cv2.putText(img, f"(0, {center_y})", (10, center_y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1, cv2.LINE_AA)  # Min X
        cv2.putText(img, f"({width}, {center_y})", (width - 150, center_y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1, cv2.LINE_AA)  # Max X
        cv2.putText(img, f"({center_x}, 0)", (center_x + 10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1, cv2.LINE_AA)  # Min Y
        cv2.putText(img, f"({center_x}, {height})", (center_x + 10, height - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1, cv2.LINE_AA)  # Max Y

        
        
        
        lmList = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            
            for id, lm in enumerate(myHand.landmark):
                # print(id, lm)
                h,w,c = img.shape
                
                cx, cy = int(lm.x*w), int(lm.y*h)
                # cx0, cy0 = int(myHand.landmark[8].x*w), int(myHand.landmark[8].y*h)
                lmList.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 25, (255,255,255), cv2.FILLED)
                # cv2.circle(img, (cx0, cy0), 15, (255,255,0), cv2.FILLED)
        return lmList
    
    
def main():
    pTime = 0
    cTime = 0
    cap = cv2.VideoCapture(0)
    detector = handDetector()
    while True:
        success, img = cap.read()
        img = detector.findHands(img)
        lmList = detector.findPosition(img, draw=False)
        if len(lmList)!=0: print(lmList[0])
        
        if len(lmList)>7: print(lmList[8])
        if len(lmList)>2:PTSB.data_writer(data=lmList[8][1:])
        
        cTime = time.time()
        fps = 1/(cTime-pTime)
        pTime = cTime
        
        cv2.putText(img, str(int(fps)), (10,10), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX,
                    1, (255,255,255), 3)
        
        cv2.imshow("Image", img)
        cv2.waitKey(1)


if __name__ == "__main__":
    main()