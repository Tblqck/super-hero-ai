import pyautogui
import time

def show_mouse_position():
    """
    Displays the current position of the mouse in real-time.
    Press Ctrl+C to stop the program.
    """
    print("Press Ctrl+C to stop.")
    try:
        while True:
            # Get the current position of the mouse
            x, y = pyautogui.position()
            # Print the position dynamically (overwrites the same line)
            print(f"Mouse Position: X={x}, Y={y}", end="\r")
            time.sleep(0.1)  # Update every 0.1 seconds
    except KeyboardInterrupt:
        print("\nProgram stopped.")

# Run the function
show_mouse_position()
