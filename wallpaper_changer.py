import os
import sys
import random
import ctypes
import win32con
import win32gui
import winreg
import logging
from datetime import datetime

def setup_logging(log_file="wallpaper_changer.log"):
    # Create logs directory if it doesn't exist
    logs_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")
    os.makedirs(logs_dir, exist_ok=True)
    
    # Full path to log file
    log_path = os.path.join(logs_dir, log_file)
    
    # Configure logger
    logger = logging.getLogger("WallpaperChanger")
    logger.setLevel(logging.INFO)
    
    # File handler
    file_handler = logging.FileHandler(log_path)
    file_handler.setLevel(logging.INFO)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    
    # Create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    # Add handlers to logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger

def get_random_image(folder_path, logger):
    try:
        # Check if folder exists
        if not os.path.isdir(folder_path):
            logger.error(f"The folder '{folder_path}' does not exist.")
            return None
        
        # List all files in the folder
        files = os.listdir(folder_path)
        
        # Filter for image files with supported extensions
        image_extensions = ('.png', '.jpg', '.jpeg', '.bmp')
        image_files = [f for f in files if f.lower().endswith(image_extensions)]
        
        # Check if any image files were found
        if not image_files:
            logger.error(f"No image files found in '{folder_path}'.")
            return None
        
        # Select a random image
        random_image = random.choice(image_files)
        image_path = os.path.join(folder_path, random_image)
        
        logger.info(f"Selected image: {random_image}")
        return image_path
        
    except Exception as e:
        logger.exception(f"Error occurred while selecting a random image: {str(e)}")
        return None

def set_wallpaper(image_path, style=10, logger=None):
    try:
        # Check if the image file exists
        if not os.path.isfile(image_path):
            logger.error(f"The image file '{image_path}' does not exist.")
            return False
        
        # Get absolute path
        abs_image_path = os.path.abspath(image_path)
        
        # Get the style name for logging
        style_names = {
            0: "Centered",
            1: "Tiled",
            2: "Stretched",
            6: "Fit",
            10: "Fill"
        }
        style_name = style_names.get(style, "Unknown")
        
        # Open the registry key
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 
                            r"Control Panel\Desktop", 
                            0, 
                            winreg.KEY_SET_VALUE)
        
        # Set the appropriate registry values based on style
        if style == 0:    # Centered
            winreg.SetValueEx(key, "WallpaperStyle", 0, winreg.REG_SZ, "0")
            winreg.SetValueEx(key, "TileWallpaper", 0, winreg.REG_SZ, "0")
        elif style == 1:  # Tiled
            winreg.SetValueEx(key, "WallpaperStyle", 0, winreg.REG_SZ, "0")
            winreg.SetValueEx(key, "TileWallpaper", 0, winreg.REG_SZ, "1")
        elif style == 2:  # Stretched
            winreg.SetValueEx(key, "WallpaperStyle", 0, winreg.REG_SZ, "2")
            winreg.SetValueEx(key, "TileWallpaper", 0, winreg.REG_SZ, "0")
        elif style == 6:  # Fit
            winreg.SetValueEx(key, "WallpaperStyle", 0, winreg.REG_SZ, "6")
            winreg.SetValueEx(key, "TileWallpaper", 0, winreg.REG_SZ, "0")
        elif style == 10: # Fill
            winreg.SetValueEx(key, "WallpaperStyle", 0, winreg.REG_SZ, "10")
            winreg.SetValueEx(key, "TileWallpaper", 0, winreg.REG_SZ, "0")
        else:             # Default to Fill
            winreg.SetValueEx(key, "WallpaperStyle", 0, winreg.REG_SZ, "10")
            winreg.SetValueEx(key, "TileWallpaper", 0, winreg.REG_SZ, "0")
            style_name = "Fill (Default)"
        
        # Close the key
        winreg.CloseKey(key)
        
        # Set as wallpaper using win32 API
        win32gui.SystemParametersInfo(
            win32con.SPI_SETDESKWALLPAPER, 
            abs_image_path, 
            win32con.SPIF_UPDATEINIFILE | win32con.SPIF_SENDCHANGE
        )
        
        logger.info(f"Wallpaper successfully set to: {abs_image_path}")
        logger.info(f"Style: {style} ({style_name})")
        return True
        
    except Exception as e:
        logger.exception(f"Error occurred while setting the wallpaper: {str(e)}")
        return False

def main():
    try:
        # Set up logging
        logger = setup_logging()
        
        # Get the current timestamp for logging
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"--- Wallpaper Change Started: {current_time} ---")
        
        # Folder path containing the wallpaper images
        # Change this to your wallpaper images folder
        wallpaper_folder = r"C:\Wallpapers"
        logger.info(f"Using wallpaper folder: {wallpaper_folder}")
        
        # Get a random image from the folder
        image_path = get_random_image(wallpaper_folder, logger)
        
        if image_path:
            # Set the selected image as the wallpaper
            # You can change the style here: 0=Centered, 1=Tiled, 2=Stretched, 6=Fit, 10=Fill
            wallpaper_style = 10  # Default to Fill
            success = set_wallpaper(image_path, style=wallpaper_style, logger=logger)
            if success:
                logger.info("Wallpaper change completed successfully.")
            else:
                logger.error("Failed to set the wallpaper.")
        else:
            logger.error("Failed to select a random image.")
            
    except Exception as e:
        if 'logger' in locals():
            logger.exception(f"An unexpected error occurred: {str(e)}")
        else:
            print(f"A critical error occurred before logging was initialized: {str(e)}")
    
    if 'logger' in locals():
        logger.info(f"--- Wallpaper Change Finished ---\n")

if __name__ == "__main__":
    main()

"""
HOW TO SCHEDULE THIS SCRIPT TO RUN DAILY:
-----------------------------------------
1. Save this script as 'wallpaper_changer.py' on your computer.
2. Update the 'wallpaper_folder' variable in the main() function to point to your images folder.
3. Make sure you have the pywin32 library installed (pip install pywin32).
4. To schedule the script to run daily:
   a. Open Windows Task Scheduler (search for 'Task Scheduler' in the Start menu).
   b. Click on 'Create Basic Task' in the right panel.
   c. Enter a name (e.g., "Daily Wallpaper Change") and description.
   d. Set the trigger to 'Daily' and choose your preferred time.
   e. For the action, select 'Start a program'.
   f. Browse and select your Python executable (e.g., C:\Python39\python.exe).
   g. In 'Add arguments', enter the full path to this script (e.g., "C:\Scripts\wallpaper_changer.py").
   h. Complete the wizard and the task will be scheduled.

HOW TO RUN THE SCRIPT HIDDEN (NO COMMAND PROMPT):
------------------------------------------------
1. Create a VBS script to run the Python script without showing a command prompt window:
   a. Open Notepad and paste the following code:
   
      Option Explicit
      Dim WShell, strPath
      Set WShell = CreateObject("WScript.Shell")
      strPath = "python.exe " & Chr(34) & "C:\path\to\your\wallpaper_changer.py" & Chr(34)
      WShell.Run strPath, 0, False
      Set WShell = Nothing
   
   b. Replace "C:\path\to\your\wallpaper_changer.py" with the actual path to your Python script.
   c. Save the file with a .vbs extension (e.g., "run_wallpaper_changer.vbs").
   d. You can run this VBS script directly or schedule it using Task Scheduler instead of the Python script.
   e. If the python.exe is not in your PATH, use the full path to python.exe.

HOW TO VIEW LOGS:
----------------
1. The script creates a "logs" folder in the same directory as the script.
2. Log files are saved as "wallpaper_changer.log" in this folder.
3. Each log entry contains a timestamp, the event level, and a description.
4. You can open the log file with any text editor to view the history of wallpaper changes.
"""