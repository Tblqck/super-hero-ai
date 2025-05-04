import pyautogui

# Define the region: (left, top, width, height)
region = (609, 467, 739, 505)  # Example area you want to capture

# Take the screenshot
screenshot = pyautogui.screenshot(region=region)

# Save the screenshot to a file
screenshot.save("captured_region.png")
