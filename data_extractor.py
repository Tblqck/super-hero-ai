# data_extractor.py

import os
from ocr_extractor import extract_text_with_tesseract_cli, process_text_to_numbers, save_data_to_csv
from ocr_extractor import extract_text_from_ocr_space

# Data line 1: Extracting and processing data from final_screenshot.png
def data_line_1():
    """Extract, process and save data from final_screenshot.png."""
    # Get the absolute path of the current script
    script_directory = os.path.dirname(os.path.abspath(__file__))

    # Set the relative path to the final_screenshot.png
    image_path = os.path.join(script_directory, 'final_screenshot.png')

    # Extract text using pytesseract from final_screenshot.png
    extracted_text = extract_text_with_tesseract_cli(image_path)

    if extracted_text:
        # Process the extracted text into a list of numbers
        numbers = process_text_to_numbers(extracted_text)
        
        # Save the processed data to a CSV file with timestamp and sequence
        save_data_to_csv(numbers)
    else:
        print("No text extracted from final_screenshot.png.")

# Data line 2: Extracting and processing data from screenshot.png (using OCR.space)
def data_line_2():
    """Extract, process and save data from screenshot.png using OCR.space."""
    # Get the absolute path of the current script
    script_directory = os.path.dirname(os.path.abspath(__file__))

    # Set the relative path to the screenshot
    image_path = os.path.join(script_directory, 'screenshot.png')

    # Extract text using OCR.space
    extracted_text = extract_text_from_ocr_space(image_path)

    if extracted_text:
        # Process the extracted text into a list of numbers
        numbers = process_text_to_numbers(extracted_text)
        
        # Save the processed data to a CSV file with timestamp and sequence
        save_data_to_csv(numbers)
    else:
        print("No text extracted from the image.")
