# Lab Session: Tuesday
# Demo: 12/12/2024
# Anishka Raina(Ar933), YI GU(yg642), Group 5
import os
from PIL import Image
# This is code for preprocessing
def convert_jpeg_to_jpg(input_file, resolution=(300, 400)):
    """Convert a single JPEG file to JPG format and resize it."""
    # Open the image
    image = Image.open(input_file)
    
    # Resize the image
    image = image.resize(resolution, Image.Resampling.LANCZOS)
    
    # Save as .jpg
    output_file = os.path.splitext(input_file)[0] + '.jpg'
    image.save(output_file, "JPEG")
    
    # Remove the original .jpeg file
    os.remove(input_file)
    print(f"Converted and resized: {input_file} -> {output_file}")

def process_folder_jpeg_to_jpg(input_folder, resolution=(300, 400)):
    """Find all JPEG files in the input folder and replace them with resized JPGs."""
    for root, _, files in os.walk(input_folder):
        for file in files:
            if file.lower().endswith('.jpeg'):
                input_file = os.path.join(root, file)
                convert_jpeg_to_jpg(input_file, resolution)

# Example usage
input_folder = "dataset/source/banana"  # Replace with the folder containing JPEG files
process_folder_jpeg_to_jpg(input_folder, resolution=(300, 400))
