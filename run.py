# Lab Session: Tuesday
# Demo: 12/12/2024
# Anishka Raina(Ar933), YI GU(yg642), Group 5
import mediapipe as mp
import pygame
import pigame
import cv2 
import shutil
from pygame.locals import *
import os
import time
import RPi.GPIO as GPIO
import glob
from time import sleep
from detect import run_image_classification
from database import find_recipes
import shutil
from threading import Thread

os.putenv('SDL_VIDEODRV', 'fbcon')
os.putenv('SDL_FBDEV', '/dev/fb0')
os.putenv('SDL_MOUSEDRV', 'dummy')
os.putenv('SDL_MOUSEDEV', '/dev/null')
os.putenv('DISPLAY', '')
os.putenv('SDL_VIDEODRIVER', 'fbcon')

GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_PHOTO, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Configure as input with pull-up resistor
GPIO.setup(BUTTON_PREV, GPIO.IN, pull_up_down=GPIO.PUD_UP) 
GPIO.setup(BUTTON_NEXT, GPIO.IN, pull_up_down=GPIO.PUD_UP) 
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(27, GPIO.FALLING, callback=button_27_callback, bouncetime=300)
LED_PIN = 5  # Choose a GPIO pin for the LED
GPIO.setup(LED_PIN, GPIO.OUT)
BUTTON_PHOTO = 17
BUTTON_PREV = 22
BUTTON_NEXT = 23
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255,0 ,0)
BLUE = (0, 102, 204)  # Blue color
SCAN_COLOR = (0, 102, 204)
button_width = 150  # Increase width
button_height = 70  # Increase height

def clear_directory(directory_path):
    """
    Clears all files and subdirectories in the specified directory but keeps the directory itself.
    """
    if not os.path.exists(directory_path):
        print(f"Directory {directory_path} does not exist.")
        return

    for item in os.listdir(directory_path):
        item_path = os.path.join(directory_path, item)
        try:
            if os.path.isfile(item_path) or os.path.islink(item_path):
                os.unlink(item_path)  # Remove file or symlink
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)  # Remove directory and its contents
        except Exception as e:
            print(f"Failed to delete {item_path}. Reason: {e}")
def button_27_callback(channel):
    global my_running
    print("Button 27 pressed....")
    GPIO.cleanup()
    my_running = False
def detect():
    model_path = 'mobilenet_v2.pth'
    images_folder = '/home/pi/lab7/project/captured_images'
    class_names = ['banana', 'broccoli', 'butter', 'corn','cream', 'egg','garlic','onion','pepper','potato', 'tomato']
    return run_image_classification(model_path, images_folder, class_names)

def get_quadrant(x, y, center_x, center_y):
    if x < center_x and y < center_y:
        return 1  # Top-left
    elif x >= center_x and y < center_y:
        return 2  # Top-right
    elif x < center_x and y >= center_y:
        return 3  # Bottom-left
    elif x >= center_x and y >= center_y:
        return 4  # Bottom-left
    else:
        return None  # No action
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
        return "Forward"
    else:
        return "Backward"
def draw_menu(lcd, font_big, rects, touch_buttons, ingredients):
    # Clear screen
    lcd.fill(WHITE)
    
    # Title
    font_big = pygame.font.Font(None, 30)
    font_title = pygame.font.Font(None, 40)
    title_text = font_title.render('Smart Recipe Assistant', True, BLACK)
    title_rect = title_text.get_rect(center=(160, 30))
    lcd.blit(title_text, title_rect)

    # Ingredients Section Title
    font_section_title = pygame.font.Font(None, 24)
    section_title_text = font_section_title.render("Ingredients:", True, BLACK)
    lcd.blit(section_title_text, (20, 70))  # Position the title above the ingredient list

    # List ingredients on the left-hand side
    font_ingredients = pygame.font.Font(None, 24)
    y_start = 100  # Starting y-coordinate for the ingredients
    x_offset = 20  # Offset from the left edge
    line_spacing = 30  # Space between lines
    DARK_GREEN = (0, 100, 0)  # Define dark green color for ingredients

    if ingredients:
        for i, ingredient in enumerate(ingredients):
            ingredient_text = font_ingredients.render(f"- {ingredient}", True,  (0, 100, 0))
            lcd.blit(ingredient_text, (x_offset, y_start + i * line_spacing))

    # Draw buttons
    for k, v in touch_buttons.items():
        # Create button background color
        if k == "Scan":
            pygame.draw.rect(lcd, SCAN_COLOR, (v[0] - button_width // 2, v[1] - button_height // 2, button_width, button_height))
        else:
            pygame.draw.rect(lcd, BLUE, (v[0] - button_width // 2, v[1] - button_height // 2, button_width, button_height))

        # Create button text with white color
        text_surface = font_big.render('%s' % k, True, WHITE)
        rect = text_surface.get_rect(center=v)
        rects[k] = rect
        lcd.blit(text_surface, rect)



def display_instructions(instructions, lcd, font, text_color, background_color):
    lcd.fill(background_color)
    y_offset = 40  # Start a little below the top
    line_spacing = 25  # Space between lines

    # Break instructions into lines that fit the screen width
    words = instructions.split(' ')
    line = ""
    for word in words:
        test_line = f"{line} {word}".strip()
        text_width, text_height = font.size(test_line)
        if text_width > lcd.get_width() - 20:  # Adjust for screen padding
            # Calculate x-coordinate to center the text
            rendered_text = font.render(line, True, text_color)
            x = (lcd.get_width() - font.size(line)[0]) // 2
            lcd.blit(rendered_text, (x, y_offset))
            y_offset += line_spacing
            line = word
        else:
            line = test_line

    # Draw the last line
    rendered_text = font.render(line, True, text_color)
    x = (lcd.get_width() - font.size(line)[0]) // 2  # Center the last line
    lcd.blit(rendered_text, (x, y_offset))


def main():
    # Declare global variables for managing application state
    global my_running
    global camera_running
    global SCAN_COLOR

    # Initialize MediaPipe Hands and drawing utilities
    mp_hands = mp.solutions.hands
    mp_drawing = mp.solutions.drawing_utils
    hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.5, min_tracking_confidence=0.5)

    # Variables for gesture detection
    gesture_start_time = None
    gesture_command = None
    gesture_hold_duration = 0 

    # Initialize Pygame and PiTFT display
    pygame.init()
    pitft = pigame.PiTft()

    # Set up the display
    lcd = pygame.display.set_mode((320, 240))
    lcd.fill((0, 0, 0))
    pygame.display.update()
    pygame.mouse.set_visible(False)

    # Load fonts for text rendering
    font_big = pygame.font.Font(None, 30)
    font_title = pygame.font.Font(None, 40)

    # Dictionary to store button rectangles for touch interaction
    rects = {}

    # Initialize application state variables
    my_running = True
    page = 0
    step = 0
    camera_running = False
    chosen_recipe = None

    # Start time for timeout or session tracking
    start_time = time.time()

    # Initialize the camera
    camera = cv2.VideoCapture(0)
    if not camera.isOpened():
        print("Error: Could not open the camera.")
        exit()
    print("Camera initialized successfully. Press 'q' to quit the live stream.")

    # Directory for saving captured images
    image_save_path = "/home/pi/lab7/project/captured_images"  # Update this path as needed
    if not os.path.exists(image_save_path):
        os.makedirs(image_save_path)

    # Counter for saved images and list of detected ingredients
    image_count = 0
    ingredients = []

    try:
        while my_running:
            # Update PiTFT display
            pitft.update()
            elapsed_time = time.time() - start_time

            if page == 0:
                # Define touch buttons and render the main menu
                touch_buttons = {
                    'Generate': (220, 180),
                    'Scan': (220, 100),
                }
                draw_menu(lcd, font_big, rects, touch_buttons, ingredients)

                if camera_running:
                    # Capture a frame from the camera
                    ret, frame = camera.read()
                    if not ret:
                        print("Failed to grab frame.")
                        break

                    # Save an image when the photo button is pressed
                    if GPIO.input(BUTTON_PHOTO) == GPIO.LOW:
                        GPIO.output(LED_PIN, GPIO.HIGH)  # Turn on the LED
                        time.sleep(0.5)                  # Wait for the button press duration
                        GPIO.output(LED_PIN, GPIO.LOW)   # Turn off the LED
                        image_name = f"image_{image_count}.jpg"
                        image_path = os.path.join(image_save_path, image_name)
                        cv2.imwrite(image_path, frame)
                        print(f"Image saved at {image_path}")
                        image_count += 1

                # Handle touch events
                for event in pygame.event.get():
                    if event.type == MOUSEBUTTONUP:
                        pos = pygame.mouse.get_pos()

                        # Check which button is clicked
                        for k, v in touch_buttons.items():
                            rect_x = v[0] - button_width // 2
                            rect_y = v[1] - button_height // 2

                            if rect_x <= pos[0] <= rect_x + button_width and rect_y <= pos[1] <= rect_y + button_height:
                                if k == "Generate":
                                    print("Generate")
                                    page = 1
                                elif k == "Scan":
                                    if SCAN_COLOR == BLUE:
                                        SCAN_COLOR = RED
                                        camera_running = True
                                        clear_directory('/home/pi/lab7/project/captured_images')
                                    else:
                                        SCAN_COLOR = BLUE
                                        camera_running = False
                                        ingredients = detect()

            if page == 1:
                # Render recipe suggestions
                lcd.fill((255, 255, 255)) 
                results = find_recipes(ingredients)
                font = pygame.font.SysFont(None, 23)
                y_position = 20

                # Define positions and quadrants for recipe display
                screen_width, screen_height = 320, 240
                center_x, center_y = screen_width // 2, screen_height // 2

                quadrants = [
                    (center_x // 2, center_y // 2),
                    (center_x + center_x // 2, center_y // 2),
                    (center_x // 2, center_y + center_y // 2),
                    (center_x + center_x // 2, center_y + center_y // 2),
                ]
                positions = [(0, 0), (160, 0), (0, 120), (160, 120)]

                # Display recipe images and names in quadrants
                for i, result in enumerate(results[:4]):
                    image = pygame.image.load(result['path'])
                    image = pygame.transform.scale(image, (160, 120))
                    lcd.blit(image, positions[i])

                    recipe_text = f"{result['name']}"
                    text_surface = font.render(recipe_text, True, BLACK, WHITE)
                    text_width, text_height = text_surface.get_size()

                    x = quadrants[i][0] - text_width // 2
                    y = quadrants[i][1] + center_y // 2 - text_height

                    if i == 0:
                        x = max(0, x)
                        y = min(screen_height // 2 - text_height, y)
                    elif i == 1:
                        x = min(screen_width - text_width, x)
                        y = min(screen_height // 2 - text_height, y)
                    elif i == 2:
                        x = max(0, x)
                        y = max(screen_height // 2, y)
                    elif i == 3:
                        x = min(screen_width - text_width, x)
                        y = max(screen_height // 2, y)

                    lcd.blit(text_surface, (x, y))

                # Draw quadrant dividing lines
                pygame.draw.line(lcd, BLACK, (center_x, 0), (center_x, screen_height))
                pygame.draw.line(lcd, BLACK, (0, center_y), (screen_width, center_y))

                # Handle mouse clicks for quadrant selection
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        x, y = pygame.mouse.get_pos()
                        quadrant = get_quadrant(x, y, center_x, center_y)
                        if quadrant:
                            page = 2
                            chosen_recipe = results[quadrant - 1]
                            camera.set(3, 320)
                            camera.set(4, 240)

            if page == 2:
                # Display recipe instructions and manage gesture control
                step_min = 0
                step_max = len(chosen_recipe["instructions"]) - 1
                lcd.fill((255, 255, 255))

                ret, frame = camera.read()
                if not ret:
                    break

                frame = cv2.flip(frame, 1)
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = hands.process(rgb_frame)

                if results.multi_hand_landmarks:
                    for landmarks in results.multi_hand_landmarks:
                        gesture = detect_gesture(landmarks)
                        if gesture == gesture_command:
                            if gesture_start_time and time.time() - gesture_start_time >= 1.4:
                                if gesture_command == "Backward":
                                    step = max(step - 1, step_min)
                                elif gesture_command == "Forward":
                                    step = min(step + 1, step_max)
                                gesture_start_time = time.time()
                        else:
                            gesture_command = gesture
                            gesture_start_time = time.time()

                # Handle GPIO button presses for navigation
                if GPIO.input(BUTTON_PREV) == GPIO.LOW:
                    step = max(step - 1, step_min)
                if GPIO.input(BUTTON_NEXT) == GPIO.LOW:
                    step = min(step + 1, step_max)
                if GPIO.input(BUTTON_PHOTO) == GPIO.LOW:
                    step = 0
                    page = 0

                # Display the current step of the recipe
                font = pygame.font.SysFont(None, 25)
                display_instructions(chosen_recipe["instructions"][step], lcd, font, BLACK, WHITE)

            pygame.display.update()
            sleep(0.1)
            lcd.fill((255, 255, 255))

    except KeyboardInterrupt:
        pass
    finally:
        # Cleanup resources
        del pitft


if __name__ == '__main__':
    main()
