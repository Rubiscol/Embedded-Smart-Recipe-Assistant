# Lab Session: Tuesday
# Demo: 12/12/2024
# Anishka Raina(Ar933), YI GU(yg642), Group 5

import cv2
import RPi.GPIO as GPIO
import time
import os

GPIO.setmode(GPIO.BCM)
BUTTON_PIN = 17
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Configure as input with pull-up resistor

# Initialize the camera using OpenCV
camera = cv2.VideoCapture(0)  # Adjust the camera ID if necessary

if not camera.isOpened():
    print("Error: Could not open the camera.")
    exit()
print("Camera initialized successfully. Press 'q' to quit the live stream.")

image_save_path = "/home/pi/captured_images/"  # Update this path as needed

if not os.path.exists(image_save_path):
    os.makedirs(image_save_path)

image_count = 0  # Counter for saved images

try:
    while True:
        ret, frame = camera.read()
        if not ret:
            print("Failed to grab frame.")
            break
        cv2.imshow("frame",frame)
        if GPIO.input(BUTTON_PIN) == GPIO.LOW:  # Button pressed
            image_name = f"image_{image_count}.jpg"
            image_path = os.path.join(image_save_path, image_name)
            cv2.imwrite(image_path, frame)
            print(f"Image saved at {image_path}")
            image_count += 1
            time.sleep(0.5)  # Debounce delay
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

except KeyboardInterrupt:
    print("Program interrupted by user.")

finally:
    # Release the camera and close all OpenCV windows
    camera.release()
    # cv2.destroyAllWindows()
    GPIO.cleanup()  # Clean up GPIO settings
    print("Resources released and GPIO cleaned up.")

