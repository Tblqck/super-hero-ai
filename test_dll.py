import pyautogui
import time

def get_mouse_click_position():
    """
    Waits for the user to click and returns the mouse position.
    """
    print("Move your mouse to the desired position and press Enter.")
    input("Press Enter to capture position...")  # Wait for user confirmation
    return pyautogui.position()

def capture_screenshot_from_selection():
    """
    Allows the user to select the top-left and bottom-right corners of a rectangle,
    then captures a screenshot of that region.
    """
    print("Select the top-left corner.")
    top_left = get_mouse_click_position()
    
    print("Select the bottom-right corner.")
    bottom_right = get_mouse_click_position()
    
    # Calculate width and height
    x1, y1 = top_left
    x2, y2 = bottom_right
    width = x2 - x1
    height = y2 - y1

    if width <= 0 or height <= 0:
        print("Invalid selection. Please try again.")
        return
    
    screenshot_path = "screenshot.png"
    screenshot = pyautogui.screenshot(region=(x1, y1, width, height))
    screenshot.save(screenshot_path)
    
    print(f"Screenshot taken and saved at: {screenshot_path}")
    print(f"Screenshot coordinates: Top-Left({x1}, {y1}) - Bottom-Right({x2}, {y2})")

# Run the function
capture_screenshot_from_selection()
