import os
import shutil
import random


def copy_random_images(source_folder, destination_folder, percentage):
    # Ensure the destination folder exists
    os.makedirs(destination_folder, exist_ok=True)

    # Get all files in the source folder
    all_files = os.listdir(source_folder)

    # Filter for image files (you can add more extensions if needed)
    image_files = [f for f in all_files if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tif'))]

    # Calculate the number of images to copy
    num_to_copy = int(len(image_files) * (percentage / 100))

    # Randomly select images
    selected_images = random.sample(image_files, num_to_copy)

    # Copy selected images to the destination folder
    for image in selected_images:
        source_path = os.path.join(source_folder, image)
        destination_path = os.path.join(destination_folder, image)
        shutil.copy2(source_path, destination_path)

    print(f"Copied {num_to_copy} images to {destination_folder}")


# Example usage
source_folder = "val/receipt"
destination_folder = "data/receipt"
percentage = 5  # Copy 20% of the images

copy_random_images(source_folder, destination_folder, percentage)
