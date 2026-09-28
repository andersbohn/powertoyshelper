@echo off
REM Disable PowerToys Keyboard Manager
REM This script disables the Keyboard Manager and restarts PowerToys

setlocal enabledelayedexpansion

REM Get the directory where this script is located
set SCRIPT_DIR=%~dp0
REM Remove trailing backslash
set SCRIPT_DIR=!SCRIPT_DIR:~0,-1!
REM Go up one level to project root
for %%A in ("!SCRIPT_DIR!\..") do set PROJECT_DIR=%%~fA

REM Navigate to project directory
cd /d "!PROJECT_DIR!"
if errorlevel 1 (
    echo Error: Failed to change to project directory
    echo Expected: !PROJECT_DIR!
    pause
    exit /b 1
)

REM Run the Python script
python "%PROJECT_DIR%\src\powertoys_manager.py" off
if errorlevel 1 (
    echo.
    echo Error: Failed to run PowerToys manager
    pause
    exit /b 1
)

pause
endlocal
