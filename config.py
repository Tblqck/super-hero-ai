# positionsChanges.py

import os
import positionsChanges
config1 = positionsChanges
WATCH_REGION = config1.C1_WATCH_REGION
SCREENSHOT_REGION2 = config1.C1_SCREENSHOT_REGION2



#USE_ONNX_MODEL = True # Set to False to use pattern_model.py instead


# Trade simulation settingsn
INITIAL_BALANCE = 1091
STAKING_AMOUNT = "10.00"
STOP_LOSS = 500
NEXT_TARGET = 2500

# config.p
MODEL_SELECTION = 1  # Change to 0 to use model112.onnx
MODEL_PATHS = {
    1: "model12112(best).onnx",
    0: "model112.onnx"
}
# Action locations (modify based on screen size)
CLICK_LOCATION_CLASS_2 = config1.C1_CLICK_LOCATION_CLASS_2
CLICK_LOCATION_CLASS_3 = config1.C1_CLICK_LOCATION_CLASS_3
# Toggle button region (x, y, width, height)
TOGGLE_REGION = config1.C1_TOGGLE_REGION
# Staking amount region (x, y, width, height)
STAKE_REGION = config1.C1_STAKE_REGION
# Click positions
TOGGLE_BUTTON_POS = config1.C1_TOGGLE_BUTTON_POS 
STAKE_FIELD_POS = config1.C1_STAKE_FIELD_POS
SCROLL_POS = config1.C1_SCROLL_POS
NUMBER_PAD_POSITIONS = config1.C1_NUMBER_PAD_POSITIONS
# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_FILE = os.path.join(BASE_DIR, "predictions_log.csv")
# Screenshot region (x, y, width, height)
SCREENSHOT_REGION = config1.C1_SCREENSHOT_REGION
# Screen positions stored as a dictionary for easy modification

SCREEN_POSITIONS = config1.C1_SCREEN_POSITIONS

# Base resolution (Your current screen resolution)
BASE_SCREEN_WIDTH = config1.C1_BASE_SCREEN_WIDTH 
BASE_SCREEN_HEIGHT = config1.C1_BASE_SCREEN_HEIGHT


# File paths
REFERENCE_IMAGE_PATH = "flew_away_template1.png"
IMAGE_2_PATH = "Screenshot_2.png"
IMAGE_1_PATH = "Screenshot_1.png"
CAPTURED_IMAGE = "button_watch12.png"
REFERENCE_IMAGE_PATH1 = r"C:\Users\DArK_SIDE\Documents\sporty\digits\New folder"
PREDICTIONS_LOG = "predictions_log.csv"
ROUNDS_LOG = "rounds_log.csv"
STATE_FILE = "state.csv"
FIREBASE_CRED = r"C:\Users\DArK_SIDE\Documents\sport-ae89b-firebase-adminsdk-fbsvc-294f54575a.json"
SYSTEM_INFO_FILE = r"C:\Users\DArK_SIDE\Documents\sporty\system_info.csv"
LOCAL_MESSAGES_FILE = r"C:\Users\DArK_SIDE\Documents\sporty\local_messages.csv"
# Thresholds
THRESHOLD = 0.8  # Adjust based on template matching sensitivity
MAX_BLACK_RATIO = 0.50  # If >95% of pixels are black, retake screenshot
TESSERACT_PATH = r"C:\Program Files\Tesseract-OCR\tesseract.exe"  # Adjust based on your installation
SCREEN_RECTANGLE = config1.C1_SCREEN_RECTANGLE
# OCR Configuration
OCR_CONFIG = "--oem 3 --psm 6"  # Common OCR config for Tesseract
REAL_STAKING = True
ENABLE_ACTIONS = True
