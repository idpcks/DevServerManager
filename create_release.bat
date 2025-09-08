@echo off
echo DevServer Manager - Release Creator
echo ====================================

if "%1"=="" (
    echo Usage: create_release.bat ^<version^>
    echo Example: create_release.bat 1.0.0
    pause
    exit /b 1
)

set VERSION=%1
echo Creating release version %VERSION%...
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    pause
    exit /b 1
)

REM Check if release script exists
if not exist "scripts\create_release.py" (
    echo Error: Release script not found
    pause
    exit /b 1
)

REM Run the release script
echo Running release script...
python scripts\create_release.py %VERSION%

if errorlevel 1 (
    echo.
    echo Release creation failed!
    pause
    exit /b 1
)

echo.
echo Release created successfully!
echo.
echo Next steps:
echo 1. Push changes: git push origin main
echo 2. Push tags: git push origin --tags
echo 3. GitHub Actions will create the release automatically
echo.
pause
