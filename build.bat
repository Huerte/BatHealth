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

echo [3/4] Cleaning up...
rmdir /s /q build 2>nul
echo       Done.
echo.

echo [4/4] Building Windows Installer Using Inno Setup...
set ISCC="C:\Program Files (x86)\Inno Setup 6\ISCC.exe"
if not exist %ISCC% set ISCC="C:\Program Files\Inno Setup 6\ISCC.exe"

if not exist %ISCC% (
    echo [INFO] Inno Setup Compiler not found. Installing via winget...
    winget install --id JRSoftware.InnoSetup -e --accept-package-agreements --accept-source-agreements --silent >nul 2>&1
    set ISCC="C:\Program Files (x86)\Inno Setup 6\ISCC.exe"
)

if exist %ISCC% (
    %ISCC% "installer\installer.iss" >nul 2>&1
    if errorlevel 1 (
        echo [ERROR] Failed to compile installer.
    ) else (
        echo       Installer successfully created in Output\
    )
) else (
    echo [WARNING] Could not locate or install ISCC.exe. Installer was not built.
)
echo.

echo ============================================
echo   Build complete!
echo   Executable : dist\BatHealth.exe
echo   Installer  : Output\BatHealth_Setup_v1.0.exe
echo ============================================
pause
