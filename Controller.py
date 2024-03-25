import time
import cv2
import mediapipe as mp
import pyautogui

# Initialize video capture
cap = cv2.VideoCapture(0)

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.5, min_tracking_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

# Initialize key states
w_pressed = False
s_pressed = False
a_pressed = False
d_pressed = False

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Flip the frame horizontally to fix mirroring
    frame = cv2.flip(frame, 1)

    # Convert BGR image to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the frame to detect hands
    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Draw hand landmarks on the frame
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Get the landmarks of the hand
            thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
            middle_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]

            # Check if hand is open or closed
            if thumb_tip.y > middle_finger_tip.y:  # Hand open
                if w_pressed:
                    pyautogui.keyUp('w')
                    w_pressed = False
                pyautogui.press('s')
                s_pressed = True
            else:  # Hand closed
                if s_pressed:
                    pyautogui.keyUp('s')
                    s_pressed = False
                pyautogui.press('w')
                w_pressed = True

            # Check hand movement to left or right
            # if thumb_tip.x > middle_finger_tip.x:  # Hand moved right
            #     if a_pressed:
            #         pyautogui.keyUp('a')
            #         a_pressed = False
            #     pyautogui.press('d')
            #     d_pressed = True
            # else:  # Hand moved left
            #     if d_pressed:
            #         pyautogui.keyUp('d')
            #         d_pressed = False
            #     pyautogui.press('a')
            #     a_pressed = True

    # Display the frame
    cv2.imshow('Hand Detection', frame)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
