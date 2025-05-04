import time
import pyautogui
import numpy as np
import cv2
import config

def watch_location():
    watch_x1, watch_y1, watch_x2, watch_y2 = config.WATCH_REGION
    template = cv2.imread(config.REFERENCE_IMAGE_PATH, cv2.IMREAD_GRAYSCALE)

    if template is None:
        print(f"Error: Reference image '{config.REFERENCE_IMAGE_PATH}' not found.")
        return

    print("Watching for the target location...")

    start_time = time.time()
    MAX_RUNTIME = 60  # Stop watching after 60 seconds if nothing is found

    while True:
        try:
            if time.time() - start_time > MAX_RUNTIME:
                print("Timeout: Target location not found. Stopping watch.")
                break  

            screenshot = pyautogui.screenshot(region=(watch_x1, watch_y1, watch_x2, watch_y2))
            screenshot_np = np.array(screenshot)
            screenshot_gray = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2GRAY)

            result = cv2.matchTemplate(screenshot_gray, template, cv2.TM_CCOEFF_NORMED)
            _, max_val, _, max_loc = cv2.minMaxLoc(result)

            if max_val >= config.THRESHOLD:
                print(f"Target detected at {max_loc} with confidence {max_val:.2f}")
                break  # Stop after detecting the target

        except Exception as e:
            print(f"An error occurred: {e}")

        time.sleep(0.2)  # Small delay before checking again

# Run the function
watch_location()
