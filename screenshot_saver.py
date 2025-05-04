import pyautogui
import os

def take_screenshot():
    # Coordinates for the rectangle
    x1, y1 = 609, 467 # Top-left corner 833, 394, 846, 411

    x2, y2 = 739, 504# Bottom-right corner

    # Calculate width and height of the rectangle
    width = x2 - x1
    height = y2 - y1

    try:
        # Take the screenshot
        screenshot = pyautogui.screenshot(region=(x1, y1, width, height))

        # Get the current directory where the script is located
        current_dir = os.path.dirname(os.path.abspath(__file__))

        # Save the screenshot in the same directory
        screenshot_path = os.path.join(current_dir, "screenshot.png")
        screenshot.save(screenshot_path)

        print(f"Screenshot saved as '{screenshot_path}'")
        return "Done"

    except Exception as e:
        print(f"An error occurred: {e}")
        return "Failed"

# Example usage:
if __name__ == "__main__":
    result = take_screenshot()
    print(result)
