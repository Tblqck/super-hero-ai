import os
from ocr_extractor import extract_text_from_ocr_space, process_text_to_numbers, save_data_to_csv

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









