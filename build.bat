@echo off
echo ============================================
echo   BatHealth — Build Script
echo ============================================
echo.

where pip >nul 2>&1
if errorlevel 1 (
    echo [ERROR] pip is not installed or not in PATH.
    echo         Install Python and ensure pip is available.
    pause
    exit /b 1
)

echo [1/3] Installing PyInstaller...
pip install pyinstaller --quiet
if errorlevel 1 (
    echo [ERROR] Failed to install PyInstaller.
    pause
    exit /b 1
)
echo       Done.
echo.

echo [2/3] Building BatHealth.exe...
pyinstaller bathealth.spec --distpath dist --workpath build --clean --noconfirm
if errorlevel 1 (
    echo [ERROR] Build failed.
    pause
    exit /b 1
)
echo       Done.
echo.

echo [3/3] Cleaning up...
rmdir /s /q build 2>nul
echo       Done.
echo.

echo ============================================
echo   Build complete!
echo   Output: dist\BatHealth.exe
echo ============================================
pause
