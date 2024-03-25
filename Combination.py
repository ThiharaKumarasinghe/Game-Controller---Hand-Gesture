from cvzone.HandTrackingModule import HandDetector
import cv2
import pyautogui


# Initialize video capture
cap = cv2.VideoCapture(0)

# Initialize key states
w_pressed = False
s_pressed = False
a_pressed = False
d_pressed = False

# Hand detector
detector = HandDetector(maxHands=1, detectionCon=0.8)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Flip the frame horizontally to fix mirroring
    frame = cv2.flip(frame, 1)

    # Convert BGR image to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # hands
    hands, frame = detector.findHands(frame)

    data =[]
    if hands:
        hand = hands[0]
        lmList = hand['lmList']
        # print(lmList)
        for lm in lmList:
            data.extend([lm[0], 720 - lm[1], lm[2]])

        # print(f'Wrist : {data[1]}')
        # print(f'thumb fingure : {data[4*3+1]}')
        # print(f'index fingure : {data[8*3+1]}')
        # print(f'middle fingure : {data[12*3+1]}')
        # print(f'ring fingure : {data[16*3+1]}')
        # print(f'small fingure : {data[20*3+1]}')

        print(f'X position : {data[9 * 3]}')



        # press button-----------------------------------
        # Check if hand is open or closed
        if data[12*3+1] > data[4*3+1]:  # Hand open
            pyautogui.press('s')
            # if w_pressed:
            #     pyautogui.keyUp('w')
            #     w_pressed = False
            # pyautogui.press('s')
            # s_pressed = True
        else:  # Hand closed
            pyautogui.press('w')
            # if s_pressed:
            #     pyautogui.keyUp('s')
            #     s_pressed = False
            # pyautogui.press('w')
            # w_pressed = True

        if data[9*3] < 440:  # Hand left
            a_pressed = True
            while a_pressed:
                pyautogui.press('a')
                if data[9*3] > 440:
                    a_pressed = False

        if data[9*3] > 800:  # Hand right
            d_pressed = True
            while d_pressed:
                pyautogui.press('d')
                if data[9 * 3] < 800:
                    d_pressed = False



    else:
        print('Show your hand to camera')








    # Display the frame
    cv2.imshow('Hand Detection', frame)

    # cv2.imshow('rgb Hand Detection', rgb_frame)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()

# while True:
#     # get the frame from the webcam
#     success, img = cap.read()
#     # hands
#     hands, img = detector.findHands(img)
#
#     data = []
#
#     if hands:
#         hand = hands[0]
#         lmList = hand['lmList']
#         #print(lmList)
#         for lm in lmList:
#             data.extend([lm[0], height - lm[1], lm[2]])
#         # print(data)
#         sock.sendto(str.encode(str(data)), serverAddressPort)
#     img = cv2.resize(img, (0, 0), None, 1, 1)
#     cv2.imshow("Image", img)
#     cv2.waitKey(1)