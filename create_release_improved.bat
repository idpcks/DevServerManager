@echo off
echo Creating release package for DevServerManager v2.1.1 (Improved)
echo.

set RELEASE_NAME=DevServerManager-v2.1.1-Improved-Windows

if exist "%RELEASE_NAME%.zip" (
    echo Removing existing release package...
    del "%RELEASE_NAME%.zip"
)

echo Creating ZIP package...
powershell -command "Compress-Archive -Path 'release-v2.1.1-improved\*' -DestinationPath '%RELEASE_NAME%.zip' -Force"

if exist "%RELEASE_NAME%.zip" (
    echo.
    echo ✅ Release package created successfully: %RELEASE_NAME%.zip
    echo.
    for %%A in ("%RELEASE_NAME%.zip") do echo Package size: %%~zA bytes
    echo.
    echo 📋 Package contains:
    echo   - DevServerManager.exe (improved icon support)
    echo   - Configuration files
    echo   - Documentation (README.md, CHANGELOG.md)
    echo   - Antivirus solution guide
    echo.
    echo 🚀 Ready for GitHub release!
) else (
    echo ❌ Failed to create release package
    pause
    exit /b 1
)

pause