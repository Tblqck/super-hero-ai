import tkinter as tk

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

# Application Size Constants
APP_WIDTH = 632
APP_HEIGHT = 353
