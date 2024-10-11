import os
import random

# Path to the Quiz-images folder (update to be relative to the app's directory)
IMAGE_DIR = 'app/static/images/Quiz-images'

# Function to get a random country folder and image
def get_random_country_image():
    # Get a list of all country folders
    country_folders = [f for f in os.listdir(IMAGE_DIR) if os.path.isdir(os.path.join(IMAGE_DIR, f))]
    
    # Select a random country folder
    selected_country = random.choice(country_folders)
    
    # Path to the selected country's folder
    country_path = os.path.join(IMAGE_DIR, selected_country)
    
    # Get all image files (supports png, jpg, jfif)
    image_files = [f for f in os.listdir(country_path) if f.endswith(('png', 'jpg', 'jfif'))]
    
    # Select a random image from the folder
    selected_image = random.choice(image_files)
    
    # Return the selected country and image path
    image_path = f'images/Quiz-images/{selected_country}/{selected_image}'  # Relative to the static folder
    return selected_country, image_path

# Function to generate quiz options
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