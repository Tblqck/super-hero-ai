so this is more of a repo
__________________
from mouse_actions import click_position

def main():
     x = 1021  # Example X coordinate
     y = 210  # Example Y coordinate
     click_position(x, y)

if __name__ == "__main__":
    main()
    _____
where the above is just mouse location for the history in avaitor
----------------------
___________________
      x = 610  # Example X coordinate
     y = 635 # Example Y coordinate
     click_position(x, y)
___________________________________
where to go to bet 
----------------------------

   x = 654  # Example X coordinate
    y = 704  # Example Y coordinate
    click_position(x, y)

----------------------------------------
=============================================



______________________________________________

from screenshot_saver import take_screenshot

result = take_screenshot()
print(result)  # Output: "Done" if the screenshot was saved successfully

_______-________________screenshot of the historical avaitor

=========================================================================================


-----------------------
from screen_watch import monitor_for_text

result = monitor_for_text(reference_image_path="flew_away_template.png", threshold=0.8)
print(result)  # Output: "Done" if the process completes successfully
 

 -------
_______________________________ screen detecting  for the end of round
----------------------------------------
# Call the function to transfer data
transfer_data()
=======
remove data from csv
-==========================

____________________-
from data_extractor import data_line_1


--------------------- gettimg text from each rounds & saving to csv db
{best just for the first ignition sequence}
_____________________________

from data_extractor import data_line_2

# Call the function
if __name__ == "__main__":
    # Execute data_line_2 to extract, process, and save data
    data_line_2()

--------------------- gettimg text from histories of rounds & saving to csv db
_____________________________------------------


import subprocess
import os
import re

def extract_floats_with_tesseract(image_path):
    """Extract float numbers from image text using the tesseract CLI."""
    try:
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image file not found: {image_path}")

        output_file = "output_text"
        subprocess.run(["tesseract", image_path, output_file], check=True)
        
        with open(f"{output_file}.txt", "r", encoding="utf-8") as file:
            text = file.read()
        
        os.remove(f"{output_file}.txt")  # Cleanup intermediate file
        
        # Extract and return float numbers from the text
        return re.findall(r"\d+\.\d+", text)
    except Exception as e:
        print(f"Error using tesseract CLI: {e}")
        return []

if __name__ == "__main__":
    image_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'final_screenshot.png')
    extracted_floats = extract_floats_with_tesseract(image_path)
    
    if extracted_floats:
        print("Extracted float values:", extracted_floats)
    else:
        print("No float values found or failed to extract text.")
-------------------------------------------------------------
the above code just get the text from the screenshot of round and then strip it to the float --- it is so fast so should be used to feed the prediction 
model 
___________________________________________________________________________________
from train_model import train_and_save_model  # Import the function

train_and_save_model()  # Call the function to train and save the model-

--------------- training of the model
____________________________________________


