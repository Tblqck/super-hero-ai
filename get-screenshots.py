import pyautogui
import cv2
import numpy as np
import os

# Define the screenshot region
SCREENSHOT_REGION = (700, 492, 157, 52)  # Adjust based on your screen
SAVE_FOLDER = "test"
os.makedirs(SAVE_FOLDER, exist_ok=True)  # Ensure directory exists

def process_screenshot_for_ocr(region):
    """Takes a screenshot of the given region and processes it for OCR."""
    screenshot = pyautogui.screenshot(region=region)
    screenshot_np = np.array(screenshot)
    screenshot_gray = cv2.cvtColor(screenshot_np, cv2.COLOR_BGR2GRAY)

    # Apply additional processing for better OCR results
    processed_image = cv2.threshold(screenshot_gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

    return processed_image

# Capture and process screenshots
for i in range(10):  # Capture images for numbers 0-9
    processed_img = process_screenshot_for_ocr(SCREENSHOT_REGION)

    # (Optional: If you want to analyze black pixels like in monitor_and_process)
    black_pixels = np.sum(processed_img < 10)
    total_pixels = processed_img.size
    black_ratio = black_pixels / total_pixels
    print(f"Black ratio: {black_ratio:.2%}")

    # Save the processed image
    filename = os.path.join(SAVE_FOLDER, f"{i}.png")
    cv2.imwrite(filename, processed_img)
    print(f"Saved: {filename}")

print("Training data collected!")
