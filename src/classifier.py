import cv2
import mediapipe as mp

def classify_gesture(image_path):
    mp_hands = mp.solutions.hands
    mp_drawing = mp.solutions.drawing_utils

    img = cv2.imread(image_path)
    if img is None:
        return "rock"  # fallback if image not found

    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    with mp_hands.Hands(static_image_mode=True, max_num_hands=1) as hands:
        result = hands.process(img_rgb)

        if not result.multi_hand_landmarks:
            return "rock"  # fallback if no hand detected

        landmarks = result.multi_hand_landmarks[0].landmark

        # Determine finger states (1: open, 0: closed)
        fingers = []

        # Thumb (x comparison due to orientation)
        fingers.append(1 if landmarks[4].x < landmarks[3].x else 0)

        # Index to Pinky fingers (y comparison)
        tip_ids = [8, 12, 16, 20]
        fingers.extend([
            1 if landmarks[tip].y < landmarks[tip - 2].y else 0
            for tip in tip_ids
        ])

        total = sum(fingers)

        # Gesture classification
        if fingers[1] and fingers[2] and not fingers[3] and not fingers[4]:
            return "scissors"
        elif total == 0 or total == 1:
            return "rock"
        elif total >= 4:
            return "paper"
        else:
            return "rock"  # fallback

