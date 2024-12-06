import os
from PIL import Image
import imageio

def create_gif_from_folder(image_folder, gif_filename, duration=0.5):
    # Get the list of image files in the folder
    #image_files = [f for f in os.listdir(image_folder) if f.endswith(('.png', '.jpg', '.jpeg'))]

    image_files = [f"clustering{i}.png" for i in range(0,61)]
    
    # Sort files alphabetically (optional, adjust if you need specific ordering)
    #image_files.sort()

    # Load all images into a list
    images = []
    for file in image_files:
        img_path = os.path.join(image_folder, file)
        img = Image.open(img_path)
        images.append(img)

    # Save the images as a GIF
    images[0].save(gif_filename, save_all=True, append_images=images[1:], duration=duration * 1000, loop=0)

    print(f"GIF saved as {gif_filename}")

# Folder containing images
image_folder = 'clustering_frames'  # Change this to your folder path
gif_filename = 'clustering.gif'      # Output gif file name

# Create the GIF
create_gif_from_folder(image_folder, gif_filename, duration=0.2)
