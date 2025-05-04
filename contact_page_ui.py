import tkinter as tk
from tkinter import scrolledtext
import pandas as pd
from background import draw_gradient, APP_WIDTH, APP_HEIGHT  # Import background settings
from send_message import send_message

# CSV file path
CSV_PATH = r"C:\Users\DArK_SIDE\Documents\sporty\local_messages.csv"

def open_contact_page():
    contact_window = tk.Toplevel()  # Create a new window
    contact_window.geometry(f"{APP_WIDTH}x{APP_HEIGHT}")  
    contact_window.title("Contact Page")

    # Create a canvas for background
    canvas = tk.Canvas(contact_window, width=APP_WIDTH, height=APP_HEIGHT)
    canvas.pack(fill=tk.BOTH, expand=True)
    draw_gradient(canvas, APP_WIDTH, APP_HEIGHT, (0, 0, 0), (53, 51, 205))

    # Chat display section
    chat_display = scrolledtext.ScrolledText(contact_window, wrap=tk.WORD)
    chat_display.place(relx=0.05, rely=0.12, relwidth=0.9, relheight=0.6)
    chat_display.config(state=tk.DISABLED)  

    # User input field
    user_input = tk.Text(contact_window, height=2)
    user_input.place(relx=0.05, rely=0.75, relwidth=0.65, relheight=0.1)

    def load_messages():
        chat_display.config(state=tk.NORMAL)
        chat_display.delete("1.0", tk.END)  
        
        try:
            df = pd.read_csv(CSV_PATH)
            df = df.sort_values(by="Timestamp")
            
            for _, row in df.iterrows():
                role = "[User]" if row["Role"].lower() == "user" else "[Admin]"
                chat_display.insert(tk.END, f"{role} {row['Message']}\n")
        except Exception as e:
            chat_display.insert(tk.END, f"Error loading messages: {e}\n")
        
        chat_display.config(state=tk.DISABLED)

    def send_user_message():
        tag = "compliant"  
        message = user_input.get("1.0", tk.END).strip()  
        if message:
            send_message(tag, message)  
            chat_display.config(state=tk.NORMAL)
            chat_display.insert(tk.END, f"[User] {message}\n")  
            chat_display.config(state=tk.DISABLED)
            user_input.delete("1.0", tk.END)  

    # Send button
    send_button = tk.Button(contact_window, text="Send", command=send_user_message, bg="#4CAF50", fg="white", font=("Arial", 10, "bold"))
    send_button.place(relx=0.72, rely=0.75, relwidth=0.12, relheight=0.1)

    # Refresh button
    refresh_button = tk.Button(contact_window, text="Refresh", command=load_messages, bg="#FF9800", fg="white", font=("Arial", 10, "bold"))
    refresh_button.place(relx=0.85, rely=0.75, relwidth=0.12, relheight=0.1)

    # Load messages initially
    load_messages()

