@echo off
echo Creating DevServerManager v2.1.2 Windows Release Package
echo.

set VERSION=2.1.2
set RELEASE_NAME=DevServerManager-v%VERSION%-Windows

rem Clean existing release directories
if exist release-v%VERSION% rmdir /s /q release-v%VERSION%
if exist %RELEASE_NAME%.zip del %RELEASE_NAME%.zip

echo Creating release directory...
mkdir release-v%VERSION%

echo Copying executable...
copy dist\DevServerManager.exe release-v%VERSION%\

echo Copying configuration files...
xcopy config release-v%VERSION%\config\ /E /I

echo Copying documentation...
copy README.md release-v%VERSION%\
copy CHANGELOG.md release-v%VERSION%\
copy ANTIVIRUS_FALSE_POSITIVE_SOLUTION.md release-v%VERSION%\
copy .env.example release-v%VERSION%\

echo Creating ZIP package...
powershell -command "Compress-Archive -Path 'release-v%VERSION%\*' -DestinationPath '%RELEASE_NAME%.zip' -Force"

if exist "%RELEASE_NAME%.zip" (
    echo.
    echo ✅ Release package created successfully: %RELEASE_NAME%.zip
    echo.
    for %%A in ("%RELEASE_NAME%.zip") do echo Package size: %%~zA bytes
    echo.
    echo 📋 Package contains:
    echo   - DevServerManager.exe v%VERSION% (with python-dotenv support)
    echo   - Configuration files and templates
    echo   - Environment configuration example (.env.example)
    echo   - Documentation (README.md, CHANGELOG.md)
    echo   - Antivirus solution guide
    echo.
    echo 🚀 Ready for GitHub release v%VERSION%!
) else (
    echo ❌ Failed to create release package
    pause
    exit /b 1
)

pause