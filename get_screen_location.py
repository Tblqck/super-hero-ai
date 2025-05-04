import pyautogui
import time

# Function to capture a screenshot of the area you're selecting
def capture_screenshot_of_area():
    print("Move the mouse to the top-left corner of the area.")
    
    # Wait for 2 seconds to allow the user to position the mouse
    time.sleep(3)

    # Get the top-left corner coordinates of the area
    start_x, start_y = pyautogui.position()
    print(f"Top-left corner: {start_x}, {start_y}")

    # Now, move the mouse to the bottom-right corner of the area
    print("Move the mouse to the bottom-right corner of the area.")
    
    # Wait for another 2 seconds to allow the user to position the bottom-right corner
    time.sleep(3)

    # Get the bottom-right corner coordinates of the area
    end_x, end_y = pyautogui.position()
    print(f"Bottom-right corner: {end_x}, {end_y}")

    # Ensure the coordinates are in the correct order
    if end_x < start_x:
        start_x, end_x = end_x, start_x
    if end_y < start_y:
        start_y, end_y = end_y, start_y

    # Calculate the width and height based on the two corners
    width = end_x - start_x
    height = end_y - start_y

    # Take the screenshot of the selected area
    screenshot = pyautogui.screenshot(region=(start_x, start_y, width, height))
    screenshot.save("selected_area.png")
    
    # Print out the coordinates and the screenshot details
    print(f"Screenshot saved as 'selected_area.png'")
    print(f"Screenshot Coordinates: Top-Left ({start_x}, {start_y}), "
          f"Bottom-Right ({end_x}, {end_y}), "
          f"Width: {width}, Height: {height}")

# Call the function to start tracking and taking a screenshot
capture_screenshot_of_area()
