import os
import Augmentor

# Set the dataset path
dataset_path = "dataset/source"

# Iterate through the folders
for folder in os.listdir(dataset_path):
    folder_path = os.path.join(dataset_path, folder)
    if os.path.isdir(folder_path) and "_test" not in folder:
        print(f"Augmenting data for folder: {folder}")

        # Create an Augmentor pipeline
        p = Augmentor.Pipeline(folder_path)

        # Add brightness adjustments
        p.random_brightness(probability=0.5, min_factor=0.5, max_factor=1.5)  # Simulate dim and bright lighting

        # Add contrast adjustments
        p.random_contrast(probability=0.5, min_factor=0.7, max_factor=1.3)  # Adjust contrast to simulate different light intensity
        p.rotate(probability=0.7, max_left_rotation=10, max_right_rotation=10)
        p.flip_left_right(probability=0.5)
        p.zoom_random(probability=0.5, percentage_area=0.8)
        p.random_distortion(probability=0.5, grid_width=4, grid_height=4, magnitude=2)

        # Add slight color changes (optional)
        p.random_color(probability=0.5, min_factor=0.7, max_factor=1.3)

        # Generate augmented samples
        p.sample(400)  # Generates 100 augmented images

print("Data augmentation with lighting changes complete.")
