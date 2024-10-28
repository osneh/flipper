import tkinter as tk
from tkinter import messagebox
import subprocess
import os

# Function to run the delete.sh script
def run_delete():
    try:
        result = subprocess.run(["bash", "delete.sh"], check=True, capture_output=True, text=True)
        print(result.stdout)  # Print any output from the script
    except subprocess.CalledProcessError as e:
        print(f"Error running delete.sh: {e}")

# Function to run the RUNtcp.bat script with the provided parameter
def run_tcp(param):
    try:
        result = subprocess.run(["RUNtcp.bat", param], check=True, capture_output=True, text=True)
        print(result.stdout)  # Print any output from the script
    except subprocess.CalledProcessError as e:
        print(f"Error running RUNtcp.bat: {e}")

# Function to handle the button click
def on_run():
    param = entry.get()  # Get the input from the entry field
    if param:
        run_delete()  # Call delete.sh
        run_tcp(param)  # Call RUNtcp.bat with the parameter
        messagebox.showinfo("Success", "Scripts executed successfully!")
    else:
        messagebox.showwarning("Input Error", "Please provide a parameter.")

# Create the GUI window
root = tk.Tk()
root.title("Run TCP/IP Flipper")

# Create a label and an entry field
label = tk.Label(root, text="Enter inital VRefN:")
label.pack(padx=5, pady=5)

entry = tk.Entry(root)
entry.pack(padx=5, pady=5)

# Create a button to trigger the script execution
button = tk.Button(root, text="Run", command=on_run)
button.pack(padx=20, pady=10)

# Start the GUI event loop
root.mainloop()
