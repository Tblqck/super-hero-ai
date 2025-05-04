import pyautogui
import cv2
import numpy as np
import pandas as pd
import os
import config  # Import screen positions from config

def check_image_on_screen(image_path, position):
    """Check if the given image appears at a specific position on the screen."""
    screenshot = pyautogui.screenshot(region=(position[0], position[1], 50, 50))  # Small crop around position
    screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2GRAY)  # Convert to grayscale

    template = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)  # Load template in grayscale
    if template is None:
        print(f"Error: Unable to load {image_path}")
        return 0  # Treat as not found

    result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, _ = cv2.minMaxLoc(result)

    return 0 if max_val > 0.9 else 1  # Return 1 if image is found, otherwise 0

def monitor_button():
    """Check if a button is visible on the screen based on predefined position."""
    position = config.SCREEN_POSITIONS["monitor_button"]
    return check_image_on_screen(config.CAPTURED_IMAGE, position)

def update_csv(file_path, value):
    """Update the most recent row (largest 'Sequence' number) in 'Unnamed: 2' column if empty."""
    if not os.path.exists(file_path):
        print(f"Error: {file_path} not found.")
        return "Terminate"

    df = pd.read_csv(file_path)

    # **Check if CSV has any data**
    if df.empty:
        print("CSV file is empty. No update needed.")
        return "Terminate"

    if "Sequence" not in df.columns:
        print("Error: Column 'Sequence' not found in CSV.")
        return "Terminate"

    if "Unnamed: 2" not in df.columns:
        print("Error: Column 'Unnamed: 2' not found in CSV.")
        return "Terminate"

    # Find the row with the largest 'Sequence' value (most recent)
    latest_row_index = df["Sequence"].idxmax()

    # Check if 'Unnamed: 2' in the latest row is empty
    if pd.isna(df.at[latest_row_index, "Unnamed: 2"]):
        df.at[latest_row_index, "Unnamed: 2"] = value
        df.to_csv(file_path, index=False)
        print(f"Updated row {latest_row_index} (Sequence {df.at[latest_row_index, 'Sequence']}) with value: {value}")
        return value
    else:
        print("Most recent row already filled. Terminating.")
        return "Terminate"

def check_staking():
    """Checks if staking is required and updates the CSV log."""
    result = monitor_button()
    update_csv(config.ROUNDS_LOG, result)
    print(result)
