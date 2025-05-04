import csv
import time
import pyautogui
import cv2
import numpy as np
from datetime import datetime
import pandas as pd
from predictor import make_prediction
import sys
from staking import process_staking
from check_staking import check_staking
from check_balance import check_balance
import config
import ctypes
import os
#from merge_and_backup import process_logs
from process_and_recognize import process_and_recognize

print("hello")
#process_logs()
STATE_FILE = config.STATE_FILE  # Ensure this is defined in config.py

def monitor_and_process():
    watch_x1, watch_y1, watch_x2, watch_y2 = config.WATCH_REGION
    screenshot_x1, screenshot_y1, screenshot_x2, screenshot_y2 = config.SCREENSHOT_REGION2

    template = cv2.imread(config.REFERENCE_IMAGE_PATH, cv2.IMREAD_GRAYSCALE)
    if template is None:
        print(f"Error: Reference image '{config.REFERENCE_IMAGE_PATH}' not found.")
        return

    print("Monitoring screen for the text...")

    last_number = None
    sequence = 1  

    if os.path.exists(config.PREDICTIONS_LOG) and os.path.getsize(config.PREDICTIONS_LOG) > 0:
        try:
            df = pd.read_csv(config.PREDICTIONS_LOG)
            if "Numbers" in df.columns and not df.empty:
                last_number = str(df["Numbers"].dropna().iloc[-1])
            if "Sequence" in df.columns and not df["Sequence"].dropna().empty:
                sequence = int(df["Sequence"].dropna().max()) + 1
        except Exception as e:
            print(f"Error reading sequence from CSV: {e}")

    start_time = time.time()  # Track when monitoring started
    MAX_RUNTIME = 60  # Stop monitoring after 60 seconds if nothing is found

    while True:
        try:
            # Check if we exceeded the max runtime
            if time.time() - start_time > MAX_RUNTIME:
                print("Timeout: No valid detection found. Stopping monitoring.")
                break  # Exit the loop after the timeout

            screenshot = pyautogui.screenshot(region=(watch_x1, watch_y1, watch_x2, watch_y2))
            screenshot_np = np.array(screenshot)
            screenshot_gray = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2GRAY)

            black_pixels = np.sum(screenshot_gray < 10)
            total_pixels = screenshot_gray.size
            black_ratio = black_pixels / total_pixels

            if black_ratio > config.MAX_BLACK_RATIO:
                print(f"Black screen detected ({black_ratio*100:.2f}% black). Retaking screenshot immediately...")
                continue  

            result = cv2.matchTemplate(screenshot_gray, template, cv2.TM_CCOEFF_NORMED)
            _, max_val, _, max_loc = cv2.minMaxLoc(result)

            if max_val >= config.THRESHOLD:
                final_screenshot_path = r"C:\Users\DArK_SIDE\Documents\sporty\final_screenshot000.png"
                pyautogui.screenshot(final_screenshot_path, region=(screenshot_x1, screenshot_y1, screenshot_x2, screenshot_y2))

                recognized_number = process_and_recognize(final_screenshot_path, config.REFERENCE_IMAGE_PATH1)
                print("Recognized number:", recognized_number)

                if recognized_number is not None:
                    new_number = str(recognized_number)

                    if last_number == new_number:
                        print(f"Extracted number ({new_number}) is the same as last recorded. Continuing monitoring...")
                        time.sleep(1)
                        continue

                    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    file_exists = os.path.exists(config.PREDICTIONS_LOG) and os.path.getsize(config.PREDICTIONS_LOG) > 0

                    with open(config.PREDICTIONS_LOG, mode='a', newline='') as file:
                        writer = csv.writer(file)
                        if not file_exists:
                            writer.writerow(["Timestamp", "Sequence", "Numbers", "RealAccount"])  

                        writer.writerow([current_time, sequence, new_number, ""])
                        print(f"Logged data: Time={current_time}, Sequence={sequence}, Numbers={new_number}")

                    last_number = new_number  
                    sequence += 1  

                    print("Success: A valid number was detected and logged. Stopping monitoring.")
                    break  # Stop monitoring after a successful detection

        except Exception as e:
            print(f"An error occurred: {e}")

        time.sleep(0.2)  # Small delay before checking again


def load_state():
    """Loads the last saved state from the state file."""
    if os.path.exists(STATE_FILE):
        try:
            state_df = pd.read_csv(STATE_FILE)
            if state_df.empty or 'sequence' not in state_df.columns:
                raise ValueError("State file is empty or missing 'sequence' column")

            return (
                float(state_df.iloc[-1]['balance']),
                float(state_df.iloc[-1]['stop_loss']),
                float(state_df.iloc[-1]['next_target']),
                int(state_df.iloc[-1]['sequence'])  # Ensure we store the last sequence
            )
        except Exception as e:
            print(f"⚠️ Error loading state: {e}")

    # Default values if no state file exists
    return float(config.INITIAL_BALANCE), float(config.STOP_LOSS), float(config.NEXT_TARGET), 0  


def save_state(balance, stop_loss, next_target, sequence):
    """Saves the current state to a CSV file by appending new rows instead of overwriting."""
    new_entry = pd.DataFrame([{ 
        "balance": balance, 
        "stop_loss": stop_loss, 
        "next_target": next_target, 
        "sequence": sequence 
    }])
    
    if os.path.exists(STATE_FILE):
        new_entry.to_csv(STATE_FILE, mode='a', header=False, index=False)
    else:
        new_entry.to_csv(STATE_FILE, index=False)


def simulate_trade():
    print("simulate_trade() called")
    """Simulates trading based on predictions and updates balance accordingly."""
    try:
        print("\n📄 Reading CSV files...")

        # Load saved state
        balance, stop_loss, next_target, last_sequence = load_state()

        # Read CSVs efficiently
        predictions_log = pd.read_csv(config.PREDICTIONS_LOG)
        rounds_log = pd.read_csv(config.ROUNDS_LOG)

        if predictions_log.empty or rounds_log.empty:
            return False  # Keep looping if data is missing

        staking = float(config.STAKING_AMOUNT)
        print(f"💰 Current balance: {balance} | Sequence: {last_sequence}")

        # Sort and merge both DataFrames on 'Sequence'
        merged = pd.merge(predictions_log, rounds_log, on='Sequence')
        merged = merged.sort_values(by='Sequence')

        # Filter out already processed sequences
        merged = merged[merged['Sequence'] > last_sequence]

        if merged.empty:
            return False  # No new data to process

        trade_made = False

        # Loop through merged and zipped data
        for _, row in merged.iterrows():
            sequence = row['Sequence']
            number = float(row['Numbers'])
            predicted_class = int(row['predicted_class'])

            stake_flag = float(row.get('Unnamed: 2', 0.0))  # Safe fallback

            if config.REAL_STAKING and (pd.isna(stake_flag) or stake_flag != 1.0):
                continue  # Skip this round

            # Simplified trade logic
            if predicted_class == 1:
                continue  # No trade
            elif predicted_class == 2:
                if number > 4.99:
                    balance += (staking * 4)
                else:
                    balance -= staking
                trade_made = True
            elif predicted_class == 9:
                if number > 8.99:
                    balance += (staking * 9)
                else:
                    balance -= staking
                trade_made = True

            # Dynamic stop-loss and target adjustment
            if balance >= next_target - 1:
                stop_loss = next_target - 34
                next_target += 300
                print(f"🔺 New Stop-Loss Set: {stop_loss}, Next Target: {next_target}")

            # Stop-loss trigger
            if config.REAL_STAKING and balance <= stop_loss + 9:
                print(f"\n🚨 Stop-Loss Triggered at {balance} 🚨")
                save_state(balance, stop_loss, next_target, sequence)
                return True

            last_sequence = sequence  # Update last processed sequence

        # Save state after all sequences
        save_state(balance, stop_loss, next_target, last_sequence)
        return False

    except FileNotFoundError:
        return False
    except Exception as e:
        print(f"⚠️ Error during trade simulation: {e}")
        return False



def handle_predictions():
    print("handle_predictions() called")
    predicted_class = make_prediction()
    if predicted_class is not None:
        print(f"Handling prediction: {predicted_class}")
        if predicted_class == 1:
            print("Executing action for class 2...")
        elif predicted_class == 2:
            print("Executing action for class 1...")
            if config.ENABLE_ACTIONS:
                pyautogui.click(*config.CLICK_LOCATION_CLASS_2)
                print("HI2")
        elif predicted_class == 3:
            print("Executing action for class 3...")
            if config.ENABLE_ACTIONS:
                #pyautogui.click(*config.CLICK_LOCATION_CLASS_3)
                print("HI3")


        
def prevent_sleep():
    # Prevent sleep and keep system awake (Windows only)
    ES_CONTINUOUS = 0x80000000
    ES_SYSTEM_REQUIRED = 0x00000001
    ES_DISPLAY_REQUIRED = 0x00000002
    
    ctypes.windll.kernel32.SetThreadExecutionState(
        ES_CONTINUOUS | ES_SYSTEM_REQUIRED | ES_DISPLAY_REQUIRED
    )



def main():
    try:
        while True:
            monitor_and_process()
            handle_predictions()
            stop_trading = simulate_trade()  # Run the trade simulation
            process_staking()
            check_staking()
            #check_balance()
            prevent_sleep() 
            
            # Reload the latest state after each iteration
            balance, stop_loss, next_target, last_sequence = load_state()
            
            if balance <= stop_loss + 9:  # Check stop-loss condition
                if config.REAL_STAKING:  # If real trading is enabled, stop execution
                    print("\n❌ Trading stopped due to stop-loss. Exiting program.")
                    break  
                else:  # If real trading is off, print a message and continue looping
                    print("\n⚠️ REAL_STAKING is False, but stop-loss condition met. Looping continues...")

            time.sleep(0)  # Pause before next iteration

    except KeyboardInterrupt:
        print("\n🚪 Program interrupted by user. Exiting gracefully...")


if __name__ == "__main__":
    main()
