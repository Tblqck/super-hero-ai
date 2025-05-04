import pyautogui
import cv2
import numpy as np
import time

def monitor_for_text(reference_image_path, threshold=0.60):
    """
    Monitor a predefined region of the screen for specific text using image matching.

    Args:
        reference_image_path (str): Path to the reference image.
        threshold (float): Matching threshold (default: 0.60).

    Returns:
        str: Confirmation message when the process is complete.
    """
    # Define coordinates for monitoring and screenshot regions
    watch_x1, watch_y1, watch_x2, watch_y2 = 595, 393, 885, 509
    screenshot_x1, screenshot_y1, screenshot_x2, screenshot_y2 = 685, 279, 1018, 395

    # Load the reference image
    template = cv2.imread(reference_image_path, cv2.IMREAD_GRAYSCALE)
    if template is None:
        print(f"Error: Reference image '{reference_image_path}' not found.")
        return "Error: Reference image not found."

    print("Monitoring screen for the text...")

    while True:
        try:
            # Capture the region to monitor
            screenshot = pyautogui.screenshot(region=(watch_x1, watch_y1, watch_x2 - watch_x1, watch_y2 - watch_y1))

            # Convert the screenshot to grayscale for OpenCV
            screenshot_np = np.array(screenshot)
            screenshot_gray = cv2.cvtColor(screenshot_np, cv2.COLOR_BGR2GRAY)

            # Perform template matching
            result = cv2.matchTemplate(screenshot_gray, template, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

            # Print matching confidence for debugging
            #print(f"Matching confidence: {max_val:.2f}")

            # Check if the match meets or exceeds the threshold
            if max_val >= threshold:
               # print(f"Match threshold met! Match confidence: {max_val:.2f}")
              #  print("Stopping the process as confidence reached the threshold.")
                break  # Exit the loop

            # Sleep for a short time before the next check
            time.sleep(0.5)

        except Exception as e:
            print(f"An error occurred: {e}")
            break

    return "Done"


# Example usage
result = monitor_for_text(reference_image_path="flew_away_template2.png", threshold=0.40)
print(result)
