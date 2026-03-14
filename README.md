# NFC PC/SC to NFC Keyboard HID

NFC-based identification tool that reads card UIDs via a PC/SC NFC reader and automatically injects them as keyboard input into existing systems.

## Description

This Windows application reads NFC cards using a PC/SC compatible reader and automatically types the card UID into any focused application. The tool is designed to streamline NFC card identification workflows by eliminating manual data entry.

## Features

- Automatic NFC card UID detection
- Keyboard simulation for seamless data entry
- Clipboard support as fallback method
- Support for any PC/SC compatible NFC reader
- 30-second cooldown between consecutive reads of the same card
- Automatic card removal detection

## Requirements

### Hardware
- PC/SC compatible NFC reader
- Windows operating system

### Software
- Python 3.6 or higher
- PC/SC Smart Card service (usually pre-installed on Windows)

### Python Dependencies
See `requirements.txt` for the complete list of dependencies.

## Installation

1. Install Microsoft C++ Build Tools (required for pyscard):
   - Download from: https://visualstudio.microsoft.com/visual-cpp-build-tools/
   - Run the installer and select "Desktop development with C++"
   - Alternatively, install Visual Studio with C++ support

2. Ensure your NFC reader is connected and recognized by Windows

3. Install the required Python packages.

Note: If you encounter build errors with pyscard, restart your terminal after installing the C++ Build Tools.

## Quick start (clone and run in 2-3 commands)

From the project folder:

```bash
python -m venv .venv
.venv\Scripts\python -m pip install -r requirements.txt
.venv\Scripts\python convertor.py
```

## Usage

### Running the Python Script

If dependencies are already installed:

```bash
python convertor.py
```

2. Open your target application (e.g., web browser with CRL web app)

3. Click on the field where you want the NFC UID to be entered

4. Place an NFC card on the reader

5. The UID will be automatically typed into the focused field

### Building as Executable (.exe)

To create a standalone .exe file:

1. Build from the included spec file:
```bash
.venv\Scripts\pyinstaller nfc-reader.ico.spec --clean
```

2. Find the executable in `dist\NFC-Reader.exe`

3. You can distribute this .exe file without requiring Python installation

## How It Works

1. The script connects to the first available PC/SC NFC reader
2. It continuously polls for NFC cards
3. When a card is detected, it reads the UID using the GET_UID command
4. The UID is formatted as a hexadecimal string
5. The UID is copied to the clipboard and automatically typed using keyboard simulation
6. A 30-second cooldown prevents duplicate entries from the same card
7. Card removal is detected and resets the system for the next scan

## Operation Modes

### Auto-typing Mode
When pyautogui is available, the script will automatically type the UID into the focused field.

### Clipboard-only Mode
If pyautogui is not available, the script will copy the UID to the clipboard. You can then paste it manually using Ctrl+V.

## Troubleshooting

### Windows SmartScreen Warning
When running the .exe, you may see: "Microsoft Defender SmartScreen prevented an unrecognized app from starting."

This is normal for unsigned executables. To run the app:

**Option 1: Run Anyway (Quick)**
1. Click "More info" in the SmartScreen dialog
2. Click "Run anyway"

**Option 2: Add to Windows Defender Exclusions**
1. Open Windows Security > Virus & threat protection
2. Scroll down to "Virus & threat protection settings" and click "Manage settings"
3. Scroll to "Exclusions" and click "Add or remove exclusions"
4. Click "Add an exclusion" > "File"
5. Browse and select `nfc-reader.exe`

**Option 3: Code Signing (For Distribution)**
For professional distribution, you can purchase a code signing certificate from a trusted Certificate Authority. This will eliminate the warning for all users.

### Build error: Microsoft Visual C++ 14.0 or greater is required
- Install Microsoft C++ Build Tools from https://visualstudio.microsoft.com/visual-cpp-build-tools/
- Select "Desktop development with C++" during installation
- Restart your terminal and try installing again

### No NFC reader found
- Verify the reader is connected
- Check that the PC/SC Smart Card service is running
- Try reconnecting the reader

### Auto-typing not working
- Ensure pyautogui is installed: `python -m pip install pyautogui`
- Verify the target field is focused before placing the card
- Check if the application allows keyboard input

### Clipboard not working
- Ensure pyperclip is installed: `python -m pip install pyperclip`

### Disabling USB connection sounds
Windows plays sounds when the NFC card is placed/removed. To disable:
1. Open Windows Settings > System > Sound
2. Scroll down and click "More sound settings" or "Sound Control Panel"
3. Go to the "Sounds" tab
4. Find "Device Connect" and "Device Disconnect" in the Program Events list
5. For each, select it and choose "(None)" from the Sounds dropdown
6. Click "Apply" and "OK"

Alternatively, you can mute "System Sounds" volume in the Volume Mixer.

## Exit

Press Ctrl+C to stop the script and disconnect from the reader.
