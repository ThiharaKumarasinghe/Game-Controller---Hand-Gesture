from cvzone.HandTrackingModule import HandDetector
import cv2
import socket

# parameters
width, height = 1280, 720

# webcam
cap = cv2.VideoCapture(0)
cap.set(3, width)
cap.set(4, height)

# Hand detector
detector = HandDetector(maxHands=1, detectionCon=0.8)


# communication
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

serverAddressPort = ("127.0.0.1", 1500)


while True:
    # get the frame from the webcam
    success, img = cap.read()
    # hands
    hands, img = detector.findHands(img)

    data = []

    if hands:
        hand = hands[0]
        lmList = hand['lmList']
        #print(lmList)
        for lm in lmList:
            data.extend([lm[0], height - lm[1], lm[2]])
        # print(data)
        sock.sendto(str.encode(str(data)), serverAddressPort)
    img = cv2.resize(img, (0, 0), None, 1, 1)
    cv2.imshow("Image", img)
    cv2.waitKey(1)