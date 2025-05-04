import tkinter as tk
from PIL import Image, ImageTk

class HomePage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.configure(bg="white")

        # Load image
        image_path = r"C:\Users\DArK_SIDE\Documents\sporty\esport-removebg-preview.png"
        self.image = Image.open(image_path)
        self.image = ImageTk.PhotoImage(self.image)
        
        canvas = tk.Canvas(self, width=632, height=313, highlightthickness=0)
        canvas.pack(fill=tk.BOTH, expand=True)
        canvas.create_image(0, 0, anchor=tk.NW, image=self.image)
        
        # Invisible button
        canvas.create_rectangle(11, 101, 333, 287, outline="", fill="", tags="transparent_button")
        canvas.tag_bind("transparent_button", "<Button-1>", self.button_clicked)

    def button_clicked(self, event):
        print("Invisible button clicked!")  # You can add logic to switch frames here.
