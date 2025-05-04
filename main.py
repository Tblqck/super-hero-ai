import tkinter as tk
from navigation import create_navbar
from home import HomePage
from about import AboutPage
from contact import ContactPage

def show_frame(frame):
    frame.tkraise()  # Bring the selected frame to the front

# Initialize main window
root = tk.Tk()
root.geometry("632x353")
root.title("Tkinter Multi-Page App")

# Create Frames
frame_home = HomePage(root)
frame_about = AboutPage(root)
frame_contact = ContactPage(root)

# Stack frames on top of each other
for frame in (frame_home, frame_about, frame_contact):
    frame.place(x=0, y=40, width=632, height=313)

# Create navigation bar
create_navbar(root, show_frame, frame_home, frame_about, frame_contact)

# Show default home page
show_frame(frame_home)

root.mainloop()
