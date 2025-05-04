import tkinter as tk
from PIL import Image, ImageTk

def draw_gradient(canvas, width, height, color1, color2):
    """Draws a dynamic horizontal gradient using lines."""
    canvas.delete("gradient")  # Prevent multiple gradient layers
    for i in range(width):
        ratio = i / width
        r = int(color1[0] + (color2[0] - color1[0]) * ratio)
        g = int(color1[1] + (color2[1] - color1[1]) * ratio)
        b = int(color1[2] + (color2[2] - color1[2]) * ratio)
        color = f"#{r:02x}{g:02x}{b:02x}"
        canvas.create_line(i, 0, i, height, fill=color, width=1, tags="gradient")

def create_about_page(root, show_frame, frame_home):
    """Creates the About Page frame."""
    frame_about = tk.Frame(root, bg="white")
    
    tk.Label(frame_about, text="About Page", font=("Arial", 20)).pack(pady=20)
    
    btn_home = tk.Button(frame_about, text="Home", font=("Arial", 12), bg="#0A1F44", fg="white", command=lambda: show_frame(frame_home))
    btn_home.pack(pady=10)
    
    return frame_about
