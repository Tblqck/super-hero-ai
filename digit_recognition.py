import cv2
import numpy as np
import os

def load_reference_chars(reference_path):
    """Loads reference digits (0-9), 'x', and '.' from the given path."""
    reference_chars = {}
    for char in list("0123456789x."):  # Include decimal point
        ref_img_path = os.path.join(reference_path, f"{char}.png")
        reference_chars[char] = cv2.imread(ref_img_path, cv2.IMREAD_GRAYSCALE)
    return reference_chars

def segment_digits(image):
    """Finds individual characters (digits + 'x' + '.') and sorts them left to right."""
    contours, _ = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=lambda c: cv2.boundingRect(c)[0])  # Sort by X position

    digit_regions = []
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        
        # Detecting decimal point separately (small and almost square)
        if 2 <= w <= 10 and 2 <= h <= 10:
            digit_regions.append((x, None, "."))  # Mark as decimal
        elif w > 5 and h > 10:  # Filter out small noise
            char_img = image[y:y+h, x:x+w]  # Extract character
            char_img = cv2.resize(char_img, (20, 30))  # Resize to standard size
            digit_regions.append((x, char_img, None))  # Store (x-position, image, None for decimal check)
    
    return digit_regions

def match_character(char_img, reference_chars):
    """Matches the extracted character to the closest reference (0-9, 'x', or '.')."""
    if char_img is None:
        return "."  # This is a decimal point
    
    best_match = None
    highest_score = -1

    for label, ref_img in reference_chars.items():
        if ref_img is None:
            continue
        
        ref_resized = cv2.resize(ref_img, (20, 30))  # Ensure size matches
        result = cv2.matchTemplate(char_img, ref_resized, cv2.TM_CCOEFF_NORMED)
        score = result.max()

        if score > highest_score:
            highest_score = score
            best_match = label

    return best_match if best_match else "?"

def recognize_number(reference_path, image_path):
    """Full OCR pipeline: Load reference → Segment → Match → Output digits & decimal point correctly."""
    reference_chars = load_reference_chars(reference_path)
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    
    if image is None:
        print(f"Error: Could not read image at {image_path}")
        return ""
    
    digit_images = segment_digits(image)
    
    # Sort characters by x-position before assembling the final text
    digit_images.sort(key=lambda item: item[0])  # Sort by x position
    
    recognized_text = ""
    for _, char_img, override_char in digit_images:
        recognized_text += override_char if override_char else match_character(char_img, reference_chars)
    
    return recognized_text

def process_recognized_text(recognized_text):
    """Cleans and converts recognized text into a valid float by:
    - Removing any decimals at the beginning.
    - Keeping only the first decimal in the last valid number.
    - Ignoring 'x' and everything after it.
    """
    if not recognized_text:
        return None

    # Ignore everything after 'x'
    recognized_text = recognized_text.split('x')[0]

    # Remove leading decimal points
    recognized_text = recognized_text.lstrip('.')

    # Keep only the first decimal in the last number
    if '.' in recognized_text:
        parts = recognized_text.split('.')
        cleaned_text = parts[0] + '.' + ''.join(parts[1:]).replace('.', '')  # Keep only the first decimal
    else:
        cleaned_text = recognized_text

    try:
        return float(cleaned_text)
    except ValueError:
        return None  # If conversion fails, return None


