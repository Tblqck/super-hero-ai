import tkinter as tk
from PIL import Image, ImageTk
from send_message import send_message
from contact_page_ui import open_contact_page

def draw_gradient(canvas, width, height, color1, color2):
    """Draws a dynamic horizontal gradient using lines."""
    canvas.delete("gradient")
    for i in range(width):
        ratio = i / width
        r = int(color1[0] + (color2[0] - color1[0]) * ratio)
        g = int(color1[1] + (color2[1] - color1[1]) * ratio)
        b = int(color1[2] + (color2[2] - color1[2]) * ratio)
        color = f"#{r:02x}{g:02x}{b:02x}"
        canvas.create_line(i, 0, i, height, fill=color, width=1, tags="gradient")

class ImageZoomApp:
    def __init__(self, parent, image_path):
        self.parent = parent
        self.canvas = tk.Canvas(parent, highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        self.original_image = Image.open(image_path).convert("RGBA")
        self.image = self.original_image.copy()
        self.img_width, self.img_height = self.image.size
        self.photo = ImageTk.PhotoImage(self.image)
        self.image_id = self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)
        
        self.transparent_rect = self.canvas.create_rectangle(11, 101, 333, 287, outline="", fill="", tags="transparent_button")
        self.canvas.tag_bind("transparent_button", "<Button-1>", self.button_clicked)
        
        self.canvas.bind("<MouseWheel>", self.zoom)
        self.scale = 1.0
        self.canvas.bind("<Configure>", self.on_resize)

    def button_clicked(self, event):
        print("Invisible button clicked!")

    def zoom(self, event):
        zoom_factor = 1.1 if event.delta > 0 else 0.9
        self.scale *= zoom_factor
        new_size = (int(self.img_width * self.scale), int(self.img_height * self.scale))
        self.image = self.original_image.resize(new_size, Image.Resampling.LANCZOS)
        self.photo = ImageTk.PhotoImage(self.image)
        self.canvas.itemconfig(self.image_id, image=self.photo)

    def on_resize(self, event):
        self.canvas.delete("all")
        draw_gradient(self.canvas, event.width, event.height, (0, 0, 0), (53, 51, 205))
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)
        self.transparent_rect = self.canvas.create_rectangle(11, 101, 333, 287, outline="", fill="", tags="transparent_button")
        self.canvas.tag_bind("transparent_button", "<Button-1>", self.button_clicked)

root = tk.Tk()
root.geometry("632x353")
root.title("Tkinter Multi-Page App")

nav_canvas = tk.Canvas(root, height=40, bg="black", highlightthickness=0)
nav_canvas.pack(side=tk.TOP, fill=tk.X)
draw_gradient(nav_canvas, 632, 40, (0, 0, 0), (53, 51, 205))
button_bg = "#0A1F44"

btn_home = tk.Label(root, text="Home", fg="white", font=("Arial", 12), cursor="hand2", bg=button_bg)
btn_home.place(x=10, y=10)
btn_home.bind("<Button-1>", lambda e: show_frame(frame_home))

btn_about = tk.Label(root, text="About", fg="white", font=("Arial", 12), cursor="hand2", bg=button_bg)
btn_about.place(x=70, y=10)
btn_about.bind("<Button-1>", lambda e: show_frame(frame_about))

btn_contact = tk.Label(root, text="Contact", fg="white", font=("Arial", 12), cursor="hand2", bg=button_bg)
btn_contact.place(x=140, y=10)
btn_contact.bind("<Button-1>", lambda e: open_contact_page())

frame_home = tk.Frame(root)
image_path = r"C:\Users\DArK_SIDE\Documents\sporty\esport-removebg-preview.png"
app = ImageZoomApp(frame_home, image_path)

frame_about = tk.Frame(root)
canvas_about = tk.Canvas(frame_about, highlightthickness=0)
canvas_about.pack(fill=tk.BOTH, expand=True)
draw_gradient(canvas_about, 632, 353, (0, 0, 0), (53, 51, 205))

frame_contact = tk.Frame(root)
canvas_contact = tk.Canvas(frame_contact, highlightthickness=0)
canvas_contact.pack(fill=tk.BOTH, expand=True)
draw_gradient(canvas_contact, 632, 353, (0, 0, 0), (53, 51, 205))

message_entry = tk.Text(root, height=5, width=50, font=("Arial", 12))
message_entry.place(x=50, y=100)

def send_user_message():
    tag = "compliant"
    message = message_entry.get("1.0", tk.END).strip()
    if message:
        send_message(tag, message)
        message_entry.delete("1.0", tk.END)

send_button = tk.Button(root, text="Send", font=("Arial", 12), bg="#0A1F44", fg="white", command=send_user_message)
send_button.place(x=270, y=180)

def show_frame(frame):
    for f in (frame_home, frame_about, frame_contact):
        f.pack_forget()
    frame.pack(fill=tk.BOTH, expand=True)

show_frame(frame_home)
root.mainloop()
