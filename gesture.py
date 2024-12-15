# Lab Session: Tuesday
# Demo: 12/12/2024
# Anishka Raina(Ar933), YI GU(yg642), Group 5
import cv2
import mediapipe as mp
import time

# Initialize Mediapipe hand tracking model with minimal settings for performance
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.5, min_tracking_confidence=0.5)

# Initialize webcam (reduce frame size for performance)
camera = cv2.VideoCapture(0)
camera.set(3, 320)  # Set width to 320
camera.set(4, 240)  # Set height to 240

# Timer variables
gesture_start_time = None
gesture_command = None
gesture_hold_duration = 0  # Track the duration of the hold

def is_fist(landmarks):
    # Check if all the fingers are curled (fist gesture)
    for i in range(4, 20, 4):  # Check only fingertip landmarks (index, middle, ring, pinky)
        fingertip = landmarks[i]
        base_finger = landmarks[i - 2]  # The base of the finger (e.g., for index, it's 1)
        if fingertip.y < base_finger.y:  # If any fingertip is higher than its base, it's not a fist
            return False
    return True

def detect_gesture(landmarks):
    if is_fist(landmarks.landmark):
        return "Backward"
    else:
        return "Forward"

while camera.isOpened():
    ret, frame = camera.read()
    if not ret:
        break

    # Flip the frame horizontally for a more intuitive mirror effect
    frame = cv2.flip(frame, 1)

    # Convert the frame to RGB for Mediapipe
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks:
        for landmarks in results.multi_hand_landmarks:
            # Detect the gesture
            gesture = detect_gesture(landmarks)

            # If the gesture is the same as the previous, check how long it's been held
            if gesture == gesture_command:
                if gesture_start_time and time.time() - gesture_start_time >= 2:
                    # Print the command after 1 second and reset the timer
                    print(f"Command: {gesture_command}")
                    gesture_start_time = time.time()  # Reset timer after printing command
            else:
                # If the gesture changes, start the timer and reset hold duration
                gesture_command = gesture
                gesture_start_time = time.time()

            # Draw the hand landmarks
            mp_drawing.draw_landmarks(frame, landmarks, mp_hands.HAND_CONNECTIONS)

            # Display the gesture on the screen
            cv2.putText(frame, f"Gesture: {gesture}", (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Show the frame
    cv2.imshow("Gesture Control", frame)

    # Exit loop on pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close OpenCV window
camera.release()
cv2.destroyAllWindows()
