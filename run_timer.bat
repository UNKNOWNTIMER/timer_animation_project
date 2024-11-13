@echo off

:: Set Python version and download URL
set PYTHON_VERSION=3.11.0
set PYTHON_INSTALLER=python-%PYTHON_VERSION%-amd64.exe
set PYTHON_DOWNLOAD_URL=https://www.python.org/ftp/python/%PYTHON_VERSION%/%PYTHON_INSTALLER%

:: Check if Python is already installed
python --version >nul 2>&1
if %errorlevel%==0 (
    echo Python is already installed.
) else (
    :: Download Python installer if it doesn't exist
    if not exist %PYTHON_INSTALLER% (
        echo Downloading Python %PYTHON_VERSION%...
        powershell -Command "Invoke-WebRequest -Uri %PYTHON_DOWNLOAD_URL% -OutFile %PYTHON_INSTALLER%"
    )

    :: Install Python silently if it's not already installed
    if not exist "%ProgramFiles%\Python%PYTHON_VERSION%" (
        echo Installing Python %PYTHON_VERSION%...
        start /wait %PYTHON_INSTALLER% /quiet InstallAllUsers=1 PrependPath=1 Include_pip=1
    )

    :: Ensure pip is available and update to the latest version
    python -m ensurepip
    python -m pip install --upgrade pip
)

:: Check if required libraries are installed
python -c "import PIL" >nul 2>&1
if %errorlevel%==0 (
    echo Required libraries are already installed.
) else (
    :: Install required libraries
    python -m pip install pillow
)

:: Run TIMER_graphics_password.py in the same directory as the batch script
set SCRIPT_PATH=%~dp0TIMER_graphics_password.py
if exist "%SCRIPT_PATH%" (
    python "%SCRIPT_PATH%"
) else (
    echo ERROR: Could not find TIMER_graphics_password.py in the current directory.
)

pause
