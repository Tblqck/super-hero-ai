import pyautogui
import cv2
import numpy as np
import time
from PIL import Image
import pytesseract
import threading
import config  # Import configuration file

def extract_text(image):
    """Extract text from an image using pytesseract."""
    scale_factor = 5
    new_size = (image.shape[1] * scale_factor, image.shape[0] * scale_factor)
    resized_image = cv2.resize(image, new_size, interpolation=cv2.INTER_CUBIC)

    _, binary_image = cv2.threshold(resized_image, 150, 255, cv2.THRESH_BINARY)
    
    return pytesseract.image_to_string(Image.fromarray(binary_image), config="--psm 6").strip()

def match_images(template, screenshot):
    """Compare an image template with a screenshot."""
    result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, _ = cv2.minMaxLoc(result)
    return max_val

def process_staking():
    """Automates staking process based on image detection."""
    
    # Load reference images
    image_1 = cv2.imread(config.IMAGE_1_PATH, cv2.IMREAD_GRAYSCALE)
    image_2 = cv2.imread(config.IMAGE_2_PATH, cv2.IMREAD_GRAYSCALE)

    # Capture toggle button region
    x, y, width, height = config.TOGGLE_REGION
    screenshot = pyautogui.screenshot(region=(x, y, width, height))
    screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2GRAY)

    # Match images
    match_1 = match_images(image_1, screenshot)
    match_2 = match_images(image_2, screenshot)

    # Click toggle button if needed
    if match_1 > match_2:
        pyautogui.click(*config.TOGGLE_BUTTON_POS)

    time.sleep(1)

    # Capture staking amount region
    stake_x, stake_y, stake_w, stake_h = config.STAKE_REGION
    staking_screenshot = pyautogui.screenshot(region=(stake_x, stake_y, stake_w, stake_h))
    staking_image = cv2.cvtColor(np.array(staking_screenshot), cv2.COLOR_RGB2GRAY)

    extracted_text = None

    def run_ocr():
        nonlocal extracted_text
        extracted_text = extract_text(staking_image)

    ocr_thread = threading.Thread(target=run_ocr)
    ocr_thread.start()
    ocr_thread.join()  # Ensure OCR completes before proceeding

    if extracted_text == config.STAKING_AMOUNT:
        return "done"

    # Click stake field
    pyautogui.click(*config.STAKE_FIELD_POS)
    time.sleep(0.5)

    pyautogui.moveTo(*config.SCROLL_POS)
    time.sleep(0.5)

    for _ in range(4):
        pyautogui.scroll(-100)
        time.sleep(0.5)

    pyautogui.click(config.NUMBER_PAD_POSITIONS["clear"])
    time.sleep(0.5)

    # Enter stake amount
    for digit in config.STAKING_AMOUNT:
        pyautogui.click(*config.NUMBER_PAD_POSITIONS[digit])
        time.sleep(0.3)

    pyautogui.click(*config.NUMBER_PAD_POSITIONS["done"])
    time.sleep(0.5)

    for _ in range(4):
        pyautogui.scroll(100)
        time.sleep(0.5)

    return "done"