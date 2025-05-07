import cv2
import mediapipe as mp


def classify_gesture(image_path):
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(static_image_mode=True, max_num_hands=1)
    mp_drawing = mp.solutions.drawing_utils

    img = cv2.imread(image_path)
    if img is None:
        return "rock"  # fallback
    
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    result = hands.process(img_rgb)

    if not result.multi_hand_landmarks:
        return "rock"  # fallback if no hand detected

    hand_landmarks = result.multi_hand_landmarks[0]

    # Finger tip landmark IDs
    # Thumb: 4
    # Index: 8
    # Middle: 12
    # Ring: 16
    # Pinky: 20

    fingers = []

    # Thumb
    if hand_landmarks.landmark[4].x < hand_landmarks.landmark[3].x:
        fingers.append(1)  # Open
    else:
        fingers.append(0)  # Closed

    # Other fingers (index, middle, ring, pinky)
    for tip_id in [8, 12, 16, 20]:
        if hand_landmarks.landmark[tip_id].y < hand_landmarks.landmark[tip_id - 2].y:
            fingers.append(1)
        else:
            fingers.append(0)

    total_fingers = sum(fingers)

    # Now special handling for Scissors:
    # if only two fingers open (index and middle), it's Scissors
    if fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 0 and fingers[4] == 0:
        return "scissors"
    elif total_fingers == 0 or total_fingers == 1:
        return "rock"
    elif total_fingers >= 4:
        return "paper"
    else:
        return "rock"  # fallback
