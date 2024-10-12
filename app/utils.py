import os
import random

# Define the path to the Quiz-images folder
IMAGE_DIR = 'app/static/images/Quiz-images'

def get_random_country_image(used_images):
    # Get a list of all country folders in the Quiz-images directory
    country_folders = [f for f in os.listdir(IMAGE_DIR) if os.path.isdir(os.path.join(IMAGE_DIR, f))]

    # Filter out images that have already been used
    available_images = []
    for country in country_folders:
        country_path = os.path.join(IMAGE_DIR, country)
        image_files = [f for f in os.listdir(country_path) if f.endswith(('png', 'jpg', 'jfif', 'webp', 'jpeg'))]

        # Only keep images that haven't been used
        unused_images = [img for img in image_files if f'{country}/{img}' not in used_images]
        
        if unused_images:
            available_images.append((country, unused_images))

    if not available_images:
        raise Exception("No more unused images are available.")

    # Select a random country and a random image from the available images
    selected_country, images = random.choice(available_images)
    selected_image = random.choice(images)

    # Return the selected country and image path (relative to the static folder)
    image_path = f'images/Quiz-images/{selected_country}/{selected_image}'
    return selected_country, image_path


def generate_quiz_options(correct_country, num_options=4):
    # Get the list of all country folders again
    country_folders = [f for f in os.listdir(IMAGE_DIR) if os.path.isdir(os.path.join(IMAGE_DIR, f))]

    # Remove the correct country from the list
    country_folders.remove(correct_country)
    
    # Randomly select (num_options - 1) other countries as incorrect options
    incorrect_options = random.sample(country_folders, num_options - 1)
    
    # Combine correct country with incorrect options and shuffle the options
    options = incorrect_options + [correct_country]
    random.shuffle(options)
    
    return options