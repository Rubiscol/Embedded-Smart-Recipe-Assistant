# Lab Session: Tuesday
# Demo: 12/12/2024
# Anishka Raina(Ar933), YI GU(yg642), Group 5import os
import torch
from torchvision import models, transforms
from PIL import Image

# Function to load a pre-trained MobileNetV2 model and modify it for the specific number of classes
def load_model(model_path, device, num_classes):
    # Initialize a MobileNetV2 model without preloaded weights
    model = models.mobilenet_v2(weights=None)
    # Modify the classifier layer to match the number of classes
    model.classifier[1] = torch.nn.Linear(model.last_channel, num_classes)
    try:
        # Load the state dictionary (model weights) from the specified path
        state_dict = torch.load(model_path, map_location=device, weights_only=True)  # Safe loading
    except TypeError:  # Fallback for older PyTorch versions
        state_dict = torch.load(model_path, map_location=device)
    # Load the weights into the model
    model.load_state_dict(state_dict)
    # Move the model to the specified device (CPU or GPU)
    model.to(device)
    # Set the model to evaluation mode
    model.eval()
    return model

# Function to classify a single image
def predict_single_image(model, image_path, transform, device, class_names):
    # Open the image and convert it to RGB format
    image = Image.open(image_path).convert('RGB')
    # Apply the defined transforms to the image and add a batch dimension
    input_tensor = transform(image).unsqueeze(0)
    # Move the input tensor to the specified device
    input_tensor = input_tensor.to(device)

    # Perform inference without calculating gradients (for efficiency)
    with torch.no_grad():
        outputs = model(input_tensor)  # Get model predictions
        _, predicted = outputs.max(1)  # Get the class index with the highest score
        return class_names[predicted.item()]  # Return the corresponding class name

# Main function to classify all images in a folder
def run_image_classification(model_path, images_folder, class_names):
    # Define device (use GPU if available, otherwise fallback to CPU)
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    
    # Get the total number of classes
    num_classes = len(class_names)
    
    # Load the trained model
    model = load_model(model_path, device, num_classes)
    
    # Define transformations for preprocessing images
    transform = transforms.Compose([
        transforms.Resize((224, 224)),  # Resize image to match the model's input size
        transforms.ToTensor(),  # Convert image to tensor
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),  # Normalize with ImageNet mean and std
    ])

    # Get a sorted list of image files in the folder (only '.jpg' files)
    image_files = sorted(
        [f for f in os.listdir(images_folder) if f.lower().endswith(('.jpg'))]
    )
    
    # Store the predicted labels for all images
    result = []
    
    # Iterate over each image and predict its label
    for filename in image_files:
        image_path = os.path.join(images_folder, filename)  # Get the full path of the image
        predicted_label = predict_single_image(model, image_path, transform, device, class_names)
        result.append(predicted_label)  # Append the label to the result list
    
    # Return the list of predicted labels
    return result

# Define the path to the trained model and images folder
model_path = 'mobilenet_v2.pth'
images_folder = '/home/pi/lab7/project/captured_images'
# List of class names corresponding to the model's output
class_names = ['banana', 'broccoli', 'butter', 'corn', 'cream', 'egg', 'garlic', 'onion', 'pepper', 'potato', 'tomato']

# Run the classification on all images in the folder and print the results
result = run_image_classification(model_path, images_folder, class_names)
print(result)  # Output the predicted labels for all images
