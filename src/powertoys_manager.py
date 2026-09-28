#!/usr/bin/env python3
"""
PowerToys Keyboard Manager State Manager

This script manages the Microsoft PowerToys Keyboard Manager state by modifying
the PowerToys JSON configuration file without requiring administrator privileges.
"""

import json
import os
import subprocess
import sys
import argparse
from pathlib import Path
from typing import Optional, Dict, Any


class PowerToysManager:
    """Manages PowerToys Keyboard Manager state."""

    def __init__(self):
        """Initialize the PowerToys manager."""
        self.config_path = self._get_config_path()
        self.executable_path = self._find_executable()

    @staticmethod
    def _get_config_path() -> Path:
        """Get the PowerToys settings.json file path."""
        localappdata = os.getenv('LOCALAPPDATA')
        if not localappdata:
            raise RuntimeError("LOCALAPPDATA environment variable not found")

        config_path = Path(localappdata) / 'Microsoft' / 'PowerToys' / 'settings.json'
        return config_path

    @staticmethod
    def _find_executable() -> Optional[Path]:
        """
        Find the PowerToys executable.

        Returns:
            Path to the PowerToys executable or None if not found.
        """
        localappdata = os.getenv('LOCALAPPDATA')
        if not localappdata:
            return None

        possible_paths = [
            Path(localappdata) / 'PowerToys' / 'PowerToys.exe',
            Path(localappdata) / 'Microsoft' / 'PowerToys' / 'PowerToys.exe',
        ]

        for path in possible_paths:
            if path.exists():
                return path

        return None

    def _read_config(self) -> Dict[str, Any]:
        """
        Read the PowerToys settings.json file.

        Returns:
            Dictionary containing the settings.

        Raises:
            FileNotFoundError: If the settings.json file is not found.
            json.JSONDecodeError: If the file is not valid JSON.
        """
        if not self.config_path.exists():
            raise FileNotFoundError(
                f"PowerToys settings file not found at: {self.config_path}"
            )

        with open(self.config_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def _write_config(self, config: Dict[str, Any]) -> None:
        """
        Write the PowerToys settings.json file.

        Args:
            config: Dictionary containing the settings to write.

        Raises:
            IOError: If the file cannot be written.
        """
        self.config_path.parent.mkdir(parents=True, exist_ok=True)

        with open(self.config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)

    def _get_keyboard_manager_enabled(self, config: Dict[str, Any]) -> bool:
        """
        Get the Keyboard Manager enabled state from the config.

        Args:
            config: Dictionary containing the settings.

        Returns:
            True if Keyboard Manager is enabled, False otherwise.
        """
        # The structure is: {"enabled": {"Keyboard Manager": true}}
        try:
            return config.get('enabled', {}).get('Keyboard Manager', False)
        except (KeyError, TypeError, AttributeError):
            return False

    def _set_keyboard_manager_enabled(
        self, config: Dict[str, Any], enabled: bool
    ) -> Dict[str, Any]:
        """
        Set the Keyboard Manager enabled state in the config.

        Args:
            config: Dictionary containing the settings.
            enabled: True to enable, False to disable.

        Returns:
            Updated configuration dictionary.
        """
        if 'enabled' not in config:
            config['enabled'] = {}

        config['enabled']['Keyboard Manager'] = enabled
        return config

    @staticmethod
    def _kill_powertoys() -> None:
        """Kill the PowerToys process."""
        try:
            subprocess.run(
                ['taskkill', '/F', '/IM', 'PowerToys.exe'],
                check=False,
                capture_output=True,
            )
        except Exception as e:
            print(f"Warning: Could not kill PowerToys process: {e}", file=sys.stderr)

    def _restart_powertoys(self) -> None:
        """Restart the PowerToys application."""
        if not self.executable_path:
            print(
                "Warning: PowerToys executable not found. "
                "Please restart PowerToys manually.",
                file=sys.stderr,
            )
            return

        try:
            subprocess.Popen(
                [str(self.executable_path)],
                shell=False,
            )
        except Exception as e:
            print(
                f"Warning: Could not restart PowerToys: {e}. "
                "Please restart it manually.",
                file=sys.stderr,
            )

    def check_status(self) -> None:
        """Read the JSON file and print the current Keyboard Manager status."""
        try:
            config = self._read_config()
            enabled = self._get_keyboard_manager_enabled(config)

            status = "enabled" if enabled else "disabled"
            print(f"Keyboard Manager is currently {status}.")

        except FileNotFoundError as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON in settings file: {e}", file=sys.stderr)
            sys.exit(1)

    def fail_if_enabled(self) -> None:
        """Exit with code 1 if Keyboard Manager is enabled, 0 otherwise (read-only)."""
        try:
            config = self._read_config()
            enabled = self._get_keyboard_manager_enabled(config)

            if enabled:
                print(
                    "Keyboard Manager is enabled. Exiting with code 1.",
                    file=sys.stderr,
                )
                sys.exit(1)

            print("Keyboard Manager is disabled.")

        except FileNotFoundError as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON in settings file: {e}", file=sys.stderr)
            sys.exit(1)

    def toggle_status(self) -> None:
        """Read, flip the boolean value, and save it back to the JSON file."""
        try:
            config = self._read_config()
            current_state = self._get_keyboard_manager_enabled(config)
            new_state = not current_state

            config = self._set_keyboard_manager_enabled(config, new_state)
            self._write_config(config)

            old_status = "enabled" if current_state else "disabled"
            new_status = "enabled" if new_state else "disabled"
            print(f"Toggled Keyboard Manager from {old_status} to {new_status}.")

            # Kill and restart PowerToys to apply changes
            print("Restarting PowerToys...")
            self._kill_powertoys()
            self._restart_powertoys()

        except FileNotFoundError as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON in settings file: {e}", file=sys.stderr)
            sys.exit(1)
        except IOError as e:
            print(f"Error: Could not write to settings file: {e}", file=sys.stderr)
            sys.exit(1)

    def set_on(self) -> None:
        """Explicitly set the Keyboard Manager enabled state to true and save the file."""
        try:
            config = self._read_config()
            current_state = self._get_keyboard_manager_enabled(config)

            config = self._set_keyboard_manager_enabled(config, True)
            self._write_config(config)

            if current_state:
                print("Keyboard Manager is already enabled.")
            else:
                print("Keyboard Manager is now enabled.")

            # Kill and restart PowerToys to apply changes
            print("Restarting PowerToys...")
            self._kill_powertoys()
            self._restart_powertoys()

        except FileNotFoundError as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON in settings file: {e}", file=sys.stderr)
            sys.exit(1)
        except IOError as e:
            print(f"Error: Could not write to settings file: {e}", file=sys.stderr)
            sys.exit(1)

    def set_off(self) -> None:
        """Explicitly set the Keyboard Manager enabled state to false and save the file."""
        try:
            config = self._read_config()
            current_state = self._get_keyboard_manager_enabled(config)

            config = self._set_keyboard_manager_enabled(config, False)
            self._write_config(config)

            if not current_state:
                print("Keyboard Manager is already disabled.")
            else:
                print("Keyboard Manager is now disabled.")

            # Kill and restart PowerToys to apply changes
            print("Restarting PowerToys...")
            self._kill_powertoys()
            self._restart_powertoys()

        except FileNotFoundError as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON in settings file: {e}", file=sys.stderr)
            sys.exit(1)
        except IOError as e:
            print(f"Error: Could not write to settings file: {e}", file=sys.stderr)
            sys.exit(1)


def main():
    """Main entry point with argparse CLI."""
    parser = argparse.ArgumentParser(
        description='Manage PowerToys Keyboard Manager state without admin privileges'
    )

    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # check command
    subparsers.add_parser(
        'check',
        help='Check the current status of Keyboard Manager'
    )

    # fail-if-enabled command
    subparsers.add_parser(
        'fail-if-enabled',
        help='Exit with code 1 if Keyboard Manager is enabled (for blocking GUI tests); read-only'
    )

    # toggle command
    subparsers.add_parser(
        'toggle',
        help='Toggle Keyboard Manager on/off and restart PowerToys'
    )

    # on command
    subparsers.add_parser(
        'on',
        help='Enable Keyboard Manager and restart PowerToys'
    )

    # off command
    subparsers.add_parser(
        'off',
        help='Disable Keyboard Manager and restart PowerToys'
    )

    args = parser.parse_args()

    # If no command provided, show help
    if not args.command:
        parser.print_help()
        sys.exit(0)

    try:
        manager = PowerToysManager()
    except RuntimeError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    # Dispatch to the appropriate method
    if args.command == 'check':
        manager.check_status()
    elif args.command == 'fail-if-enabled':
        manager.fail_if_enabled()
    elif args.command == 'toggle':
        manager.toggle_status()
    elif args.command == 'on':
        manager.set_on()
    elif args.command == 'off':
        manager.set_off()


if __name__ == '__main__':
    main()
