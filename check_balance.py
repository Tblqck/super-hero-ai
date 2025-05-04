import pandas as pd
import pyautogui
import cv2
import numpy as np
import pytesseract
import os
from config import CSV_FILE, TESSERACT_PATH, SCREENSHOT_REGION, OCR_CONFIG

# Ensure Tesseract OCR is installed
pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH

def capture_and_extract_text():
    """Capture a screenshot and extract numbers using Tesseract OCR."""
    screenshot = pyautogui.screenshot(region=SCREENSHOT_REGION)
    img = np.array(screenshot)

    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    # Increase contrast using thresholding
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)

    # Resize to improve OCR accuracy
    resized = cv2.resize(thresh, None, fx=3, fy=3, interpolation=cv2.INTER_CUBIC)

    # Perform OCR
    extracted_text = pytesseract.image_to_string(resized, config=OCR_CONFIG).strip()

    return extracted_text

def update_csv(file_path, value):
    """Update the most recent row in the CSV file."""
    if not os.path.exists(file_path):
        print(f"Error: {file_path} not found.")
        return

    df = pd.read_csv(file_path)

    if df.empty:
        print("CSV file is empty. No update needed.")
        return

    if "Sequence" not in df.columns or "RealAccount" not in df.columns:
        print("Error: Required columns not found in CSV.")
        return

    latest_row_index = df["Sequence"].idxmax()

    try:
        numeric_value = float(value)
    except ValueError:
        print(f"Error: Extracted value '{value}' is not a valid number.")
        return

    if pd.isna(df.at[latest_row_index, "RealAccount"]) or df.at[latest_row_index, "RealAccount"] == "":
        df.at[latest_row_index, "RealAccount"] = numeric_value
        df.to_csv(file_path, index=False)
        print(f"Updated row {latest_row_index} (Sequence {df.at[latest_row_index, 'Sequence']}) with value: {numeric_value}")
    else:
        print("Most recent row already filled. No update needed.")

def check_balance():
    """Extract and update balance in CSV."""
    extracted_number = capture_and_extract_text()
    print("Extracted Number:", extracted_number)
    update_csv(CSV_FILE, extracted_number)

# Example usage:
# check_balance()