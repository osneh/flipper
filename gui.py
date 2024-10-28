import os
import socket as fast_socket
import tkinter as tk
from tkinter import messagebox
import subprocess
##import configparser

# ##################################### #
#   Settings of input/output files      #
# ##################################### #
##CWD = os.path.sep.join(os.path.abspath(__name__).split(os.path.sep)[:-1])
##ConfigFolder = os.path.sep.join([CWD,'conf_Files'])
##ConfFile = os.path.sep.join([ConfigFolder,'parameters.conf'])

def getIPAddr():
    hostanme = fast_socket.gethostname()
    IPAddr = fast_socket.gethostbyname(hostname)
    return IPAddr

# Function to execute the tcp_connect.py script with the provided vrefn value
def run_tcp_connect():
    # Get the vrefn value from the input field
    vrefn_value = vrefn_entry.get()
    
    # Check if vrefn_value is provided
    if not vrefn_value:
        messagebox.showwarning("Input Error", "Please enter a value for VRefN.")
        return
    # Define the base command
    command = [
        "python", r".\routines\tcp_connect.py", 
        ##"-host", "134.158.137.124",
        "-host", getIPAdrr(),
        "-port", "8247",
        "-vrefn", vrefn_value,
        "-dirname", r"K:\RUNDATA\TCPdata"
    ]
    
    # Execute the command
    try:
        subprocess.run(command, check=True)
        messagebox.showinfo("Success", "Command executed successfully.")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Execution Error", f"An error occurred: {e}")
    except Exception as e:
        messagebox.showerror("Error", f"An unexpected error occurred: {e}")

# Initialize the main Tkinter window
root = tk.Tk()
root.title("Flipper")

# Label and Entry for VRefN
vrefn_label = tk.Label(root, text="VRefN:")
vrefn_label.grid(row=0, column=0, padx=10, pady=10)
vrefn_entry = tk.Entry(root, width=20)
vrefn_entry.grid(row=0, column=1, padx=10, pady=10)

# Run Button to execute the command
run_button = tk.Button(root, text="Run Filpper", command=run_tcp_connect)
run_button.grid(row=1, column=0, columnspan=2, pady=10)

# Run the Tkinter main loop
root.mainloop()
