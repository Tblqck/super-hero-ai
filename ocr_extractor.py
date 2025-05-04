import os
import requests
import pandas as pd
import re
import pytesseract
from PIL import Image
from datetime import datetime

# Set the path to Tesseract executable (if using pytesseract)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe"

# Method for extracting text from image using OCR.space API
def extract_text_from_ocr_space(image_path):
    """Extract text from image using OCR.space API."""
    with open(image_path, "rb") as img:
        response = requests.post(
            'https://api.ocr.space/parse/image',
            files={'file': img},
            data={'apikey': 'helloworld'}
        )
        result = response.json()

        if result['IsErroredOnProcessing']:
            print("Error processing the image with OCR.space API")
            return None
        else:
            text = result['ParsedResults'][0]['ParsedText']
            return text



import subprocess
import os

def extract_text_with_tesseract_cli(image_path):
    """
    Extract text from an image using the tesseract CLI.
    
    Args:
        image_path (str): Path to the image file.
    
    Returns:
        str: Extracted text from the image, or None if an error occurs.
    """
    try:
        # Ensure the image file exists
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image file not found: {image_path}")
        
        # Define the output file name (without extension)
        output_file = "output_text"
        
        # Run the tesseract command
        subprocess.run(["tesseract", image_path, output_file], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Read the output text file
        with open(f"{output_file}.txt", "r", encoding="utf-8") as file:
            text = file.read()
        
        # Optionally delete the intermediate file
        os.remove(f"{output_file}.txt")
        
        return text
    except FileNotFoundError as fnf_error:
        print(fnf_error)
        return None
    except subprocess.CalledProcessError as cpe:
        print(f"Error during tesseract CLI execution: {cpe}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None


import os
import pandas as pd
import re

def process_text_to_numbers(text):
    """Process extracted text into numbers and sequence them."""
    text = text.replace('k', 'x').replace('I', '1')
    pattern = r'(\d+\.\d+|\d+)(x)?'
    matches = re.findall(pattern, text)
    numbers = []
    for match in matches:
        number, suffix = match
        if suffix == 'x':  # Convert 'x' to 1
            number = float(number)
        else:
            number = float(number)
        numbers.append(number)
    
    # Now we sequence the numbers with the highest sequence as the latest
    sequence = get_next_sequence() + len(numbers) - 1  # Start with the highest sequence
    # This step ensures each number gets a sequence value starting from the highest
    sequenced_data = [{'Sequence': sequence - i, 'Value': num} for i, num in enumerate(numbers)]
    
    return sequenced_data

def reverse_sequence_data(sequenced_data):
    """Reverse the sequence so that the data with sequence 1 has the highest number."""
    # Sort the data in descending order based on the sequence field
    reversed_data = sorted(sequenced_data, key=lambda x: x['Sequence'], reverse=True)
    
    # Update the sequence to be in the reverse order (from 1 upwards)
    for i, item in enumerate(reversed_data):
        item['Sequence'] = i + 1  # Set the sequence starting from 1
    
    return reversed_data




def save_data_to_csv(numbers):
    """Save the processed data to a CSV file with sequence and timestamp."""
    # Each number already has its sequence when processed
    df = pd.DataFrame(numbers)

    # Add the current date and time as a column
    df['timestamp'] = pd.Timestamp.now()

    # Append data to CSV
    csv_file = 'data.csv'
    df.to_csv(csv_file, mode='a', header=not os.path.exists(csv_file), index=False)

    print(f"Data saved to {csv_file}.")


def get_next_sequence():
    """Get the next sequence number based on the last entry in the CSV."""
    csv_file = 'data.csv'
    if os.path.exists(csv_file):
        df = pd.read_csv(csv_file)
        if not df.empty:
            # Returns the maximum sequence value already in the file
            return df['Sequence'].max() + 1
    return 1  # Start from 1 if the CSV file is empty 




