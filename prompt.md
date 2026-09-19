Assuming 'Keycloak' was an autocorrect for Copilot or Claude, here is a precise prompt you can paste into your AI assistant to generate the complete Python script.

---

**Prompt to paste into your AI assistant:**

Write a Python script to manage the Microsoft PowerToys Keyboard Manager state without requiring administrator privileges.

The script must modify the PowerToys JSON configuration file located at `%LOCALAPPDATA%\Microsoft\PowerToys\settings.json`. Implement the following four functions:

1. `check_status()`: Read the JSON file and print whether 'Keyboard Manager' is currently enabled or disabled.
2. `toggle_status()`: Read the current state, flip the boolean value, and save it back to the JSON file.
3. `set_on()`: Explicitly set the 'Keyboard Manager' enabled state to `true` and save the file.
4. `set_off()`: Explicitly set the 'Keyboard Manager' enabled state to `false` and save the file.

For the state-changing functions (2, 3, and 4), the script must automatically apply the changes by forcefully killing the PowerToys process (`taskkill /F /IM PowerToys.exe`) and restarting it. The executable path will be either `%LOCALAPPDATA%\PowerToys\PowerToys.exe` or `%LOCALAPPDATA%\Microsoft\PowerToys\PowerToys.exe`. Ensure file read/write operations handle UTF-8 encoding correctly. Use `argparse` to allow executing these four functions via command-line arguments.