import os
import winshell
from win32com.client import Dispatch

def create_shortcut_on_desktop(target_path, shortcut_name, icon_path=None):
    # Path to the desktop
    desktop_path = winshell.desktop()
    
    # Full path for the shortcut
    shortcut_path = os.path.join(desktop_path, f"{shortcut_name}.lnk")
    
    # Create the shortcut
    shell = Dispatch('WScript.Shell')
    shortcut = shell.CreateShortcut(shortcut_path)
    shortcut.TargetPath = target_path  # Path to the application or file
    shortcut.WorkingDirectory = os.path.dirname(target_path)  # Set working directory
    
    # If an icon path is provided, set the icon for the shortcut
    if icon_path and os.path.exists(icon_path):
        shortcut.IconLocation = icon_path
    
    # Save the shortcut
    shortcut.save()
    print(f"Shortcut '{shortcut_name}' created on the desktop.")

# Example usage:
if __name__ == "__main__":
    CWD = os.path.sep.join(os.path.abspath(__name__).split(os.path.sep)[:-1])
    Files = os.path.sep.join([CWD,'files'])
    ##Routines = os.path.sep.join([CWD,'routines'])
    target_file = os.path.sep.join([CWD,'RUN.bat'])
    icon_file = os.path.sep.join([Files,'flipper.ico'])
    ##print(target_file)
    ##print(icon_file)
    ##print('-------------------')
    # Path to the target file or application
    ##target_file = r"D:\picmic_calibration\RUNtcp.bat"  # Replace with your target file path
    # Desired shortcut name on the desktop
    shortcut_name = "Flipper"
    # Path to the icon file
    ##icon_file = r"D:\picmic_calibration\files\flipper.ico"  # Replace with your icon file path
    
    create_shortcut_on_desktop(target_file, shortcut_name, icon_file)

