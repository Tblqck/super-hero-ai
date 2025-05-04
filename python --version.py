import pyautogui
import time

print("Press Ctrl+C to quit.")
try:
    while True:
        x, y = pyautogui.position()  # Get the current mouse position
        print(f"Mouse Position: X={x}, Y={y}", end="\r")  # Print position
        time.sleep(0.1)  # Update every 100ms
except KeyboardInterrupt:
    print("\nExited.")
