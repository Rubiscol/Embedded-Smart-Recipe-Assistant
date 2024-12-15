# Smart Recipe Assistant

## 1. Overall Design

The Smart Recipe Assistant utilizes PiGame to create an interactive interface for users, providing an easy and intuitive way to identify ingredients and suggest recipes. Below is an overview of the design flow.

### 1.1 Menu Screen

Upon entering the menu screen, users can interact with two primary buttons:

- **Detect Button**:
    - Clicking the button changes its color to red and activates the camera.
    - Users can photograph an ingredient by pressing button 27. Successful photo capture is indicated by a blinking LED.
    - Clicking the Detect button again changes its color to blue and turns off the camera.
    - The captured photo is processed by the ingredient detection model, which identifies the ingredients and displays a corresponding list.

- **Generate Button**:
    - Matches the identified ingredients with the top four recipes that can be prepared.
    - Clicking this button navigates the program to the Recipe Selection Page.

### 1.2 Recipe Selection Page

In this interface, users can:

- View recipes displayed with their names and corresponding images.
- Select a recipe to navigate to the Recipe Guide Page.

### 1.3 Recipe Guide Page

This page provides step-by-step guidance for preparing the selected recipe. Users can navigate the steps using hand gestures:

- **Clenching a fist**: Moves to the previous step.
- **Jazzing a hand**: Advances to the next step.

At the end of the recipe guide, users can choose to:

- Exit the guide.
- Re-scan ingredients.
- Select a new recipe.

## 2. Food Ingredient Detection Model

To simplify the user experience, the system automatically identifies and detects food ingredients using computer vision, eliminating manual input requirements. The detection model is based on MobileNet V3.

### 2.1 Model Selection and Challenges

We evaluated the following modeling methods:

- **Haar Cascade**:
    - Relies on key visual data points for ingredient classification.
    - **Challenges**: Low accuracy (35%), inability to classify multiple categories, and poor efficiency.

- **YOLOv8**:
    - Fine-tuned using over 900 food-labeled images from Roboflow.
    - **Challenges**: Unbalanced datasets, poor scalability for new categories, and sensitivity to lighting and background variations.

| Multi-class Classification | Training Speed | Detection Speed/Image | Accuracy (%) |
|----------------------------|----------------|-----------------------|--------------|
| Haar Cascade               | No             | Slow (28 ms)          | 35           |
| YOLOv8                     | Yes            | Slow (86 ms)          | 53 ± 12      |
| Ours (MobileNet V3)        | Yes            | Fast (50 ms)          | 100          |

**Table 1**: A comparison of detection models on Raspberry Pi

### 2.2 Our Approach

To address these challenges, we implemented the following strategies:

- **Data Collection and Preprocessing**: Captured ingredient photos with standardized backgrounds to reduce environmental noise.
- **Data Augmentation**: Applied techniques to simulate various angles and lighting conditions, improving model robustness.
- **Model Optimization**: Leveraged MobileNet V3 for its lightweight architecture optimized for mobile CPUs. Reduced input resolution to 300×400 pixels to accelerate training.

### 2.3 Experimental Results

Training and testing were conducted on an NVIDIA RTX 3070 GPU. Each dataset consisted of 80 training images, 20 validation images, and 3 test images. The model was trained for 10 epochs with a learning rate of 0.0001, achieving 100% detection accuracy on 36 test images. Sample results are illustrated below.

## 3. Gesture Detection Model

To enhance usability, especially when users' hands are wet or dirty, we integrated gesture detection for navigating recipe steps. This feature was implemented using MediaPipe.

### 3.1 Challenges

- **Slow Detection Speed**: Initial processing times exceeded 300 milliseconds, resulting in laggy performance.
- **Consecutive Gesture Detection**: The system frequently detected the same gesture repeatedly, causing redundant actions.

### 3.2 Our Approach

To resolve these issues:

- **Increased Detection Speed**: Reduced frame resolution to 320×240 pixels, achieving 40 FPS.
- **Controlled Gesture Execution**: Introduced a global variable to prevent consecutive gesture detections. Restricted detection to one gesture every 1.4 seconds, ensuring smooth and accurate operation.
