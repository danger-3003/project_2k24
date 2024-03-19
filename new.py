
'''
the architecture of the  mediapipe module for hand detection be like...

mediapipe --- main module
code: import mediapipe

solutions --- provides a suite of libraries for detecting hands, face, bodymarks for better predection using ML & AI algorithms
code: mediapipe.solutions

hands --- submodule for hands in suite of libararies
code: mediapipe.solutions.hands

Hands() --- class to detect hands in the given input
code: mediapipe.solutions.hands.Hands(<parameters>)

HandLandmark[--point_name--] --- used to access each point on the hand, --point_name-- for identification like THUMB_TIP, INDEX_FINGER_TIP etc..
code: mediapipe.solutions.hands.HandLandmark[--point_name--]

process(image) --- used to identigy the hand in the given image
code: mediapipe.solutions.hands.Hands().process(<image>)

drawing_utils --- function used to draw the points on the predected image
code: mediapipe.solutions.drawing_utils
'''
import cv2
import mediapipe as mp
import pyautogui
from math import dist
import SpeechRecognition as S

mp_hand_detector = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
screen_width, screen_height = pyautogui.size()  # getting the screen size using pyautogui module

input = cv2.VideoCapture(0)  # capturing the video using opencv module
hand_detection = mp_hand_detector.Hands(max_num_hands=1, min_detection_confidence=0.9)

def position(point_name):
    # Get finger point number
    point_value = mp_hand_detector.HandLandmark[point_name].value
    # Get finger point position
    point_position_x = int((hand_landmarks.landmark[point_value].x * frame_width)*screen_width/frame_width)#getting finger point x cordinates
    point_position_y = int((hand_landmarks.landmark[point_value].y * frame_height)*screen_height/frame_height)#getting finger point y cordinates

    return ([point_position_x, point_position_y])

def speech():
    command=S.voice_command_processor()
    S.executable(command)

frame_count=0
while input.isOpened():

    _, image = input.read()  # reading input video from cv2 module
    frame_height, frame_width, _ = image.shape  # getting the dimensions of the frame

    image = cv2.flip(image, 1)  # flipping the image
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hand_detection.process(image)  # making hand prediction of the image
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    if results.multi_hand_landmarks:
        hand_landmarks = results.multi_hand_landmarks[0]  # predicting landmarks of one hand only
        mp_draw.draw_landmarks(image, hand_landmarks, mp_hand_detector.HAND_CONNECTIONS)  # drawing the points of the hand on the image

        thumb_finger_tip = position("THUMB_TIP")  # getting the location of the thumb finger tip

        index_finger_tip = position("INDEX_FINGER_TIP")  # getting the location of the index finger tip
        index_finger_dip = position("INDEX_FINGER_DIP")  # getting the location of index finger dip

        middle_finger_tip = position("MIDDLE_FINGER_TIP")  # getting the location of middle finger tip
        middle_finger_dip = position("MIDDLE_FINGER_DIP")  # getting the location of middle finger dip

        ring_finger_dip = position("RING_FINGER_DIP")  # getting the location of ring finger dip

        pinky_finger_tip = position("PINKY_TIP")  # getting the location of pinky finger tip
        pinky_finger_dip = position("PINKY_DIP")  # getting the location of pinky finger dip

        thumb_index_dist = int(dist(index_finger_tip,thumb_finger_tip))  # calculating the distance between the thumb and index finger tip

        #calculating distances for open palm
        index_middle_dist = int(dist(middle_finger_dip, index_finger_tip))  # calculating the distance between the middle finger dip and index finger tip
        middle_ring_dist = int(dist(ring_finger_dip, middle_finger_dip))  # calculating the distance between the ring finger dip and middle finger dip
        ring_pinky_dist = int(dist(pinky_finger_tip, ring_finger_dip))  # calculating the distance between the ring finger dip and pinky finger tip

        #calculating distances for closed palm
        index_tip_dip_dist = int(dist(index_finger_tip, index_finger_dip))  # calculating the distance between the index finger dip and index finger tip
        middle_tip_dip_dist = int(dist(middle_finger_tip, middle_finger_dip))  # calculating the distance between the middle finger tip and middle finger dip
        pinky_tip_dip_dist = int(dist(pinky_finger_tip, pinky_finger_dip))  # calculating the distance between the pinky finger dip and pinky finger tip

        if thumb_index_dist >= 50 and thumb_index_dist <= 180 and index_middle_dist >= 80:  # if the distance between the thumb finger and index finger tips is less than 130 and grater than 50 decreasing the volume
            pyautogui.press('volumedown')
            print(thumb_index_dist)
        elif thumb_index_dist >= 181 and thumb_index_dist <= 300 and index_middle_dist >= 81:  # if the distance between the thumb finger and index finger tips is less than 250 and grater than 130 increasing the volume
            pyautogui.press('volumeup')
            print(thumb_index_dist)
        elif index_tip_dip_dist <= 50 and middle_tip_dip_dist <= 40 and pinky_tip_dip_dist <= 40 and thumb_index_dist <= 100:
            print("closed palm")
        elif index_middle_dist <= 80 and middle_ring_dist <= 90 and ring_pinky_dist <= 80 and thumb_index_dist >= 230 and not (pinky_tip_dip_dist <= 20):
            print("open palm")
            #increamenting the frame_count with 1 when there is an open palm on the screen
            frame_count+=1
            #activating the speech function if the frame_count equals to 5
            if frame_count==5:
                speech()
                frame_count=0
            

    cv2.imshow('Hand Detection', image)  # display the video on the screen
    if cv2.waitKey(5) & 0xFF == 27:  # close the output if we press Esc button
        break

input.release()
cv2.destroyAllWindows()