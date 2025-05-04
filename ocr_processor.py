import pytesseract
from PIL import Image
import os
import os
import requests
import pandas as pd
import re
import pytesseract
from PIL import Image
from datetime import datetime
import cv2
import numpy as np

def extract_text_from_image(image_path):
    """Enhance image and extract text using Tesseract OCR."""
    try:
        # Load the image
        image = cv2.imread(image_path)

        # Increase image size for better OCR detection
        scale_factor = 2  # Adjust this to enlarge the image further
        image = cv2.resize(image, None, fx=scale_factor, fy=scale_factor, interpolation=cv2.INTER_CUBIC)

        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Apply contrast enhancement
        alpha = 2.0  # Contrast control (higher value increases contrast)
        beta = 50    # Brightness control
        enhanced = cv2.convertScaleAbs(gray, alpha=alpha, beta=beta)

        # Apply thresholding to make text stand out
        _, binary = cv2.threshold(enhanced, 150, 255, cv2.THRESH_BINARY_INV)

        # Convert processed image to PIL format for Tesseract
        img_pil = Image.fromarray(binary)

        # Use Tesseract to extract text
        extracted_text = pytesseract.image_to_string(img_pil)

        return extracted_text
    except Exception as e:
        print(f"Error extracting text: {e}")
        return None


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


def process_text_to_numbers(text):
    """Process the extracted text to a list of numbers with specific formatting rules."""
    numbers = []
    
    # Replace 'j' or 'i' with '1' before 'x'
    if "x" in text:
        text = text.split('x')[0].strip()  # Remove anything after 'x'
    text = text.replace('j', '1').replace('i', '1')
    
    try:
        # Ensure the text is purely numeric before conversion
        text = ''.join(filter(str.isdigit, text))
        
        # Add a decimal point before the last two digits
        if len(text) > 2:
            text = text[:-2] + '.' + text[-2:]
        else:
            # If the number is less than 3 characters long, assume cents (e.g., '67' -> '0.67')
            text = '0.' + text.zfill(2)

        # Convert the processed text into a float number
        number = float(text)
        numbers.append(number)
    except ValueError:
        print(f"Error processing text '{text}' into a number.")
    
    return numbers

