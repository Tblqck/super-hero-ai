import cv2
import numpy as np
import tempfile
from digit_recognition import recognize_number, process_recognized_text 

def process_and_recognize(image_path, reference_path):
    """Processes an image for OCR and returns the recognized text."""
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError("Error: Unable to load image.")

    # Convert to grayscale and apply thresholding
    image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    processed_image = cv2.threshold(image_gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    
    # Save to a temporary file
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as temp_file:
        temp_path = temp_file.name
        cv2.imwrite(temp_path, processed_image)
    
    # Perform OCR
    recognized_text = recognize_number(reference_path, temp_path)
    final_number = process_recognized_text(recognized_text)
    return final_number


