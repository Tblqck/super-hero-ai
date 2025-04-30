import os
import json
import pyautogui
import originalscreen

CONFIG_FILE = "positionsChanges.py"

def get_current_screen_size():
    """Fetch the current screen resolution."""
    screen_width, screen_height = pyautogui.size()
    return screen_width, screen_height

def scale_position(original_pos, base_width, base_height, new_width, new_height):
    """Adjust positions based on new screen size."""
    scale_x = new_width / base_width
    scale_y = new_height / base_height
    if isinstance(original_pos, tuple):
        return tuple(int(coord * scale_x if i % 2 == 0 else coord * scale_y) for i, coord in enumerate(original_pos))
    return original_pos

def update_config():
    """Updates config.py with adjusted screen positions and 'C1_' prefix."""
    new_width, new_height = get_current_screen_size()
    
    new_positions = {
        "WATCH_REGION": scale_position(originalscreen.WATCH_REGION, originalscreen.BASE_SCREEN_WIDTH, originalscreen.BASE_SCREEN_HEIGHT, new_width, new_height),
        "SCREENSHOT_REGION2": scale_position(originalscreen.SCREENSHOT_REGION2, originalscreen.BASE_SCREEN_WIDTH, originalscreen.BASE_SCREEN_HEIGHT, new_width, new_height),
        "SCREEN_POSITIONS": {key: scale_position(value, originalscreen.BASE_SCREEN_WIDTH, originalscreen.BASE_SCREEN_HEIGHT, new_width, new_height) for key, value in originalscreen.SCREEN_POSITIONS.items()},
        "TOGGLE_BUTTON_POS": scale_position(originalscreen.TOGGLE_BUTTON_POS, originalscreen.BASE_SCREEN_WIDTH, originalscreen.BASE_SCREEN_HEIGHT, new_width, new_height),
        "STAKE_FIELD_POS": scale_position(originalscreen.STAKE_FIELD_POS, originalscreen.BASE_SCREEN_WIDTH, originalscreen.BASE_SCREEN_HEIGHT, new_width, new_height),
        "SCROLL_POS": scale_position(originalscreen.SCROLL_POS, originalscreen.BASE_SCREEN_WIDTH, originalscreen.BASE_SCREEN_HEIGHT, new_width, new_height),
        "NUMBER_PAD_POSITIONS": {key: scale_position(value, originalscreen.BASE_SCREEN_WIDTH, originalscreen.BASE_SCREEN_HEIGHT, new_width, new_height) for key, value in originalscreen.NUMBER_PAD_POSITIONS.items()},
        "TOGGLE_REGION": scale_position(originalscreen.TOGGLE_REGION, originalscreen.BASE_SCREEN_WIDTH, originalscreen.BASE_SCREEN_HEIGHT, new_width, new_height),
        "STAKE_REGION": scale_position(originalscreen.STAKE_REGION, originalscreen.BASE_SCREEN_WIDTH, originalscreen.BASE_SCREEN_HEIGHT, new_width, new_height),
        "CLICK_LOCATION_CLASS_2": scale_position(originalscreen.CLICK_LOCATION_CLASS_2, originalscreen.BASE_SCREEN_WIDTH, originalscreen.BASE_SCREEN_HEIGHT, new_width, new_height),
        "CLICK_LOCATION_CLASS_3": scale_position(originalscreen.CLICK_LOCATION_CLASS_3, originalscreen.BASE_SCREEN_WIDTH, originalscreen.BASE_SCREEN_HEIGHT, new_width, new_height),
        "BASE_SCREEN_WIDTH": new_width,
        "BASE_SCREEN_HEIGHT": new_height,
        "SCREENSHOT_REGION": scale_position(originalscreen.SCREENSHOT_REGION, originalscreen.BASE_SCREEN_WIDTH, originalscreen.BASE_SCREEN_HEIGHT, new_width, new_height),
        "SCREEN_RECTANGLE ": scale_position(originalscreen.SCREEN_RECTANGLE, originalscreen.BASE_SCREEN_WIDTH, originalscreen.BASE_SCREEN_HEIGHT, new_width, new_height),
        
        
    }

    with open(CONFIG_FILE, "w") as f:
        f.write("# Auto-generated config file\n\n")
        for key, value in new_positions.items():
            key = f"C1_{key}"  # Add the 'C1_' prefix to each variable name
            if isinstance(value, dict):
                formatted_dict = {k: tuple(v) for k, v in value.items()}  # Ensure all values remain tuples
                f.write(f"{key} = {formatted_dict}\n")
            elif isinstance(value, tuple):
                f.write(f"{key} = {value}\n")
            else:
                f.write(f"{key} = {json.dumps(value)}\n")

    print(f"Updated {CONFIG_FILE} with new screen positions and 'C1_' prefix.")

if __name__ == "__main__":
    update_config()
