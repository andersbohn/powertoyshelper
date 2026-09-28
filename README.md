# PowerToys Helper

A Python utility to manage the Microsoft PowerToys Keyboard Manager state without requiring administrator privileges.

## Overview

This script provides command-line tools to check, enable, and disable the PowerToys Keyboard Manager by directly modifying the PowerToys JSON configuration file located at `%LOCALAPPDATA%\Microsoft\PowerToys\settings.json`.

**Key Features:**
- ✅ No administrator privileges required for state changes
- ✅ Automatic PowerToys process restart to apply changes
- ✅ UTF-8 safe JSON handling
- ✅ Clear status messages
- ✅ Comprehensive error handling

## Installation

Ensure you have Python 3.6+ installed. No external dependencies are required beyond the Python standard library.

### Optional: Create a Virtual Environment

```bash
python -m venv .venv
.\.venv\Scripts\activate  # Windows
```

## Project Structure

```
powertoyshelper/
├── src/
│   └── powertoys_manager.py       # Main Python script
├── scripts/
│   ├── enable_keyboard_manager.bat
│   ├── disable_keyboard_manager.bat
│   ├── toggle_keyboard_manager.bat
│   ├── check_keyboard_manager_status.bat
│   ├── enable_keyboard_manager_silent.bat
│   └── disable_keyboard_manager_silent.bat
├── README.md                       # This file
└── prompt.md
```

## Basic Usage

### Check Current Status

Display whether the Keyboard Manager is currently enabled or disabled:

```bash
python src\powertoys_manager.py check
```

**Output example:**
```
Keyboard Manager is currently enabled.
```

### Toggle Keyboard Manager

Toggle the Keyboard Manager state (on ↔ off) and automatically restart PowerToys:

```bash
python src\powertoys_manager.py toggle
```

**Output example:**
```
Toggled Keyboard Manager from enabled to disabled.
Restarting PowerToys...
```

### Enable Keyboard Manager

Explicitly enable the Keyboard Manager and restart PowerToys:

```bash
python src\powertoys_manager.py on
```

**Output example:**
```
Keyboard Manager is now enabled.
Restarting PowerToys...
```

### Disable Keyboard Manager

Explicitly disable the Keyboard Manager and restart PowerToys:

```bash
python src\powertoys_manager.py off
```

**Output example:**
```
Keyboard Manager is now disabled.
Restarting PowerToys...
```

### Command-Line Help

View all available commands and options:

```bash
python src\powertoys_manager.py -h
```

## Batch File Shortcuts

### Interactive Batch Files (with output window)

Located in the `scripts/` folder:

- **`enable_keyboard_manager.bat`** - Enable Keyboard Manager and show output
- **`disable_keyboard_manager.bat`** - Disable Keyboard Manager and show output
- **`toggle_keyboard_manager.bat`** - Toggle Keyboard Manager state and show output
- **`check_keyboard_manager_status.bat`** - Check current status and show output

### Silent Batch Files (no output window)

Located in the `scripts/` folder, ideal for automation and scheduled tasks:

- **`enable_keyboard_manager_silent.bat`** - Enable silently
- **`disable_keyboard_manager_silent.bat`** - Disable silently

### Creating Desktop Shortcuts

**For Enable/Disable shortcuts:**
1. Right-click on your desktop → **New** → **Shortcut**
2. Paste this path (adjust username if needed):
   ```
   C:\Users\YourUsername\Projects\powertoyshelper\scripts\enable_keyboard_manager.bat
   ```
3. Click **Next**, name it "Enable Keyboard Manager", click **Finish**
4. Repeat for `disable_keyboard_manager.bat`

**Optional: Add custom icons and admin privileges**
- Right-click the shortcut → **Properties** → **Advanced** → ✓ **Run as administrator** (optional)
- Or right-click → **Properties** → **Shortcut** tab → **Change Icon** to pick a custom icon

## Implementation Details

### Core Functions

The script implements the following functions in the `PowerToysManager` class:

1. **`check_status()`** - Reads the JSON configuration and prints the current Keyboard Manager state (read-only)
2. **`toggle_status()`** - Flips the boolean value, saves it back, then restarts PowerToys
3. **`set_on()`** - Sets Keyboard Manager to enabled, then restarts PowerToys
4. **`set_off()`** - Sets Keyboard Manager to disabled, then restarts PowerToys

### Configuration File Format

The script operates on the following JSON structure in `settings.json`:

```json
{
  "enabled": {
    "Keyboard Manager": true
  }
}
```

### Process Management

For state-changing operations (toggle, on, off):
1. Modifies the JSON configuration file
2. Kills the PowerToys process using: `taskkill /F /IM PowerToys.exe`
3. Restarts PowerToys from one of these locations:
   - `%LOCALAPPDATA%\PowerToys\PowerToys.exe`
   - `%LOCALAPPDATA%\Microsoft\PowerToys\PowerToys.exe`

### Error Handling

The script gracefully handles:
- Missing configuration file
- Invalid JSON syntax
- Missing PowerToys executable
- File write permission issues
- Process termination/restart failures

## Advanced Usage Examples

### Create Windows Batch Shortcut
Create a custom batch file to easily toggle from desktop:

```batch
@echo off
cd /d "%LOCALAPPDATA%\..\..\Projects\powertoyshelper" 2>nul || cd /d "%~dp0"
python src\powertoys_manager.py toggle
pause
```

### Create Windows Shortcut via Command Line
1. Right-click on desktop → New → Shortcut
2. Target: `C:\Windows\System32\cmd.exe /c "python C:\Users\YourUsername\Projects\powertoyshelper\src\powertoys_manager.py on"`
3. Name: "Enable Keyboard Manager"
4. Advanced → Run minimized

### Schedule with Task Scheduler
Create a scheduled task to check status at startup:

```batch
schtasks /create /tn "PowerToys Check" /tr "python C:\Users\YourUsername\Projects\powertoyshelper\src\powertoys_manager.py check" /sc onstart
```

### Via PowerShell
```powershell
cd C:\Users\YourUsername\Projects\powertoyshelper
python src\powertoys_manager.py toggle
```

### Python: Check status and perform action
```python
import sys
sys.path.insert(0, r'C:\Users\YourUsername\Projects\powertoyshelper\src')
from powertoys_manager import PowerToysManager

manager = PowerToysManager()

# Check status
manager.check_status()

# Enable if disabled
config = manager._read_config()
if not manager._get_keyboard_manager_enabled(config):
    manager.set_on()
```

### Batch: Check and Log
```batch
@echo off
setlocal enabledelayedexpansion

for /f "delims=" %%a in ('python src\powertoys_manager.py check') do set result=%%a
echo %date% %time%: %result% >> keyboard_manager_log.txt
```

## Performance Notes

- **Check operation:** ~100-200ms (read-only)
- **State change operation:** ~1-2 seconds (includes process restart)
- **JSON file size:** Typically 1-5 KB
- **CPU impact during restart:** Minimal (brief spike during taskkill/restart)

## Security Notes

✅ **No admin required** - Uses user's own LOCALAPPDATA folder
✅ **Safe JSON handling** - Uses Python's built-in json module with UTF-8 encoding
✅ **No external dependencies** - Uses only Python standard library
✅ **UTF-8 safe** - Handles any character in JSON correctly
⚠️ **File permissions** - Requires read/write access to %LOCALAPPDATA%\Microsoft\PowerToys\settings.json
⚠️ **Process management** - Uses taskkill which may affect unsaved work in PowerToys

## Requirements

- **OS:** Windows (PowerToys is Windows-only)
- **Python:** 3.6 or later
- **PowerToys:** Must be installed in the default location

## Troubleshooting

### "LOCALAPPDATA environment variable not found"
This should never occur on Windows systems. Verify you're running on Windows with `echo %LOCALAPPDATA%` in Command Prompt.

### "PowerToys settings file not found"
Ensure PowerToys is installed and has been run at least once to generate the `settings.json` file.

### "Invalid JSON in settings file"
The settings file may be corrupted. Try:
1. Reinstalling PowerToys
2. Restoring a backup if available
3. Deleting the settings file and letting PowerToys regenerate it

### "PowerToys executable not found"
The script tried to restart PowerToys but couldn't find the executable. Try:
1. Verify PowerToys is installed in the default location
2. Restart PowerToys manually
3. Check that the installation path matches one of the expected locations

### Changes not applying after restart
PowerToys may need a moment to fully restart. Wait a few seconds and verify with the `check` command.

## License

Use freely for personal or professional purposes.

## Notes

- All file operations use UTF-8 encoding to safely handle any characters in the JSON structure
- The script does not require administrator privileges to modify the configuration
- State changes automatically apply after PowerToys restarts
- The configuration file is backed up implicitly by Windows; manual backups are recommended for important settings
