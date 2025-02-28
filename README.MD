# Windows Daily Wallpaper Changer

A Python based script that automatically changes your Windows desktop background to a random image from a specified folder. Perfect for keeping your desktop fresh with minimal effort.

## Features

- **Random Selection**: Selects a random image each time the script runs
- **Format Support**: Works with common image formats (.png, .jpg, .jpeg, .bmp)
- **Error Handling**: Comprehensive error checking and user feedback
- **Scheduling**: Can be set up to run automatically on a daily schedule
- **Silent Operation**: Can be configured to run without showing a command prompt
- **Advanced Logging**: Maintains detailed logs of all wallpaper changes and errors
- **Customizable Styles**: Easily change how wallpapers are displayed (Fill, Fit, Stretch, etc.)

## Requirements

- Windows operating system
- Python 3.x
- pywin32 library

## Installation

1. Clone or download this repository to your local machine.
2. Install the required dependency:
   ```
   pip install pywin32
   ```
3. Update the `wallpaper_folder` variable in the script to point to your images folder.

## Usage

### Basic Usage

Run the script directly to change your wallpaper immediately:

```
python wallpaper_changer.py
```

### Using Windows Task Scheduler

To set up automatic daily wallpaper changes:

1. Open Windows Task Scheduler (search for 'Task Scheduler' in the Start menu)
2. Click on 'Create Basic Task' in the right panel
3. Enter a name (e.g., "Daily Wallpaper Change") and description
4. Set the trigger to 'Daily' and choose your preferred time
5. For the action, select 'Start a program'
6. Browse and select your Python executable (e.g., C:\Python39\python.exe)
7. In 'Add arguments', enter the full path to this script (e.g., "C:\Scripts\wallpaper_changer.py")
8. Complete the wizard and the task will be scheduled

### Using VBS Scripting with Task Scheduler

To run the script without showing a command prompt window:

1. Create a new text file and paste the following code:
   ```vbs
   Option Explicit
   Dim WShell, strPath
   Set WShell = CreateObject("WScript.Shell")
   strPath = "python.exe " & Chr(34) & "C:\path\to\your\wallpaper_changer.py" & Chr(34)
   WShell.Run strPath, 0, False
   Set WShell = Nothing
   ```
2. Replace "C:\path\to\your\wallpaper_changer.py" with the actual path to your Python script
3. Save the file with a .vbs extension (e.g., "run_wallpaper_changer.vbs")
4. You can run this VBS script directly or schedule it using Task Scheduler

## Customization

### Wallpaper Style

The script allows you to easily change the wallpaper style by modifying the `wallpaper_style` variable in the `main()` function:

```python
# Change this line to set your preferred style
wallpaper_style = 6  # 6 = Fit
```

Available styles:
- 0 = Centered (image centered on screen, original size)
- 1 = Tiled (image repeated across screen)
- 2 = Stretched (image stretched to fill screen, may distort)
- 6 = Fit (image scaled to fit screen, may have black bars)
- 10 = Fill (image scaled to fill screen, may crop)

### Image Folder

Change the `wallpaper_folder` variable in the `main()` function to use a different folder for your images:

```python
wallpaper_folder = r"C:\Wallpapers"  # Change this to your folder path
```

## Logging

The script now includes a comprehensive logging system:

- Creates a "logs" folder in the same directory as the script
- Saves detailed logs in "wallpaper_changer.log"
- Logs include:
  - Timestamp of each wallpaper change
  - Selected image and style
  - Any errors or exceptions that occur
  - Operation success/failure status

To view logs:
1. Navigate to the "logs" folder in the script directory
2. Open "wallpaper_changer.log" with any text editor
3. Review entries chronologically with newest at the bottom

## Troubleshooting

- **"Module not found" error**: Make sure you've installed the pywin32 library using pip.
- **No images being found**: Verify that your wallpaper folder contains images with the supported file extensions.
- **Script not running automatically**: Check the Task Scheduler logs to see if there are any issues with the scheduled task.
- **Permission issues**: Make sure the script has appropriate permissions to write to the logs directory.
- **Style not changing**: Ensure you're modifying the correct variable (`wallpaper_style` in the `main()` function).

## License

This project is open source and available under the [MIT License](LICENSE).