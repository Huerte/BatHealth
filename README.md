<div align="center">

# BatHealth

<p align="center">
  <img width="950" height="500" alt="image" src="https://github.com/user-attachments/assets/b9808855-d250-4635-9f19-ee5d99681ef0" />
</p>

[![Version](https://img.shields.io/badge/version-1.0-blue.svg)](#)
[![Platform](https://img.shields.io/badge/platform-Windows-blueviolet.svg)](#)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](#)

**A lightweight, zero-admin battery health checker for Windows**

</div>

---

## Installation Guide

### For Normal Users

BatHealth is designed to be easily installed by anyone. No technical steps are required.

1. Download the `BatHealth_Setup_v1.0.exe` installer from the latest releases (or from the `Output` folder if built locally).
2. Double-click the file to launch the setup wizard.
3. Follow the standard installation prompts (Next -> Install -> Finish).
4. Launch **BatHealth** from your Desktop shortcut or Start Menu.

### For Developers

If you are a developer and want to modify or rebuild BatHealth locally:

**Prerequisites:**
- Python 3.7+
- pip
- Windows OS

**Build Instructions:**
Simply run the provided batch script in the project root:

```bash
build.bat
```

This script automates the entire process:
1. Installs PyInstaller (if missing).
2. Compiles `src/bathealth.py` into a standalone `dist/BatHealth.exe`.
3. Installs Inno Setup via `winget` (if missing).
4. Compiles the Windows installer to `Output/BatHealth_Setup_v1.0.exe`.

## Features

When you run BatHealth, it provides the following metrics:

| Metric           | Description                                   |
|------------------|-----------------------------------------------|
| Battery Health   | Percentage with visual bar and status rating   |
| Full Capacity    | Current maximum charge capacity in mWh         |
| Design Capacity  | Original factory capacity in mWh               |
| Cycle Count      | Number of charge cycles (if reported)          |
| Chemistry        | Battery chemistry type (Li-Ion, NiMH, etc.)   |

## How It Works

BatHealth queries the Windows battery driver directly using the native Win32 Battery IOCTL API. 
It does not use `powercfg`, does not need administrator privileges, and does not require an internet connection. Results appear instantly.

## Health Ratings

The application uses the following scale to determine battery condition:

| Range       | Rating    | Meaning                                  |
|-------------|-----------|------------------------------------------|
| 90 - 100%   | Excellent | Battery is in great condition            |
| 75 - 89%    | Good      | Normal wear, still healthy               |
| 50 - 74%    | Fair      | Noticeable degradation, monitor closely  |
| 25 - 49%    | Poor      | Consider replacing your battery          |
| 0 - 24%     | Critical  | Battery needs immediate replacement      |
### Project Structure

```text
BatHealth/
├── src/
│   └── bathealth.py          # Main application source
├── assets/
│   └── icon.ico              # Application icon
├── installer/
│   └── installer.iss         # Inno Setup installer script
├── dist/                     # Standalone exe (after build)
├── Output/                   # Windows installer (after build)
├── build.bat                 # One-click build script
├── bathealth.spec            # PyInstaller configuration
└── README.md                 # Project documentation
```

## Contributing

Contributions, issues, and feature requests are welcome! 

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Creator

**Huerte**

- GitHub: [@Huerte](https://github.com/Huerte)

---
*This project is built to make battery health monitoring accessible to everyone.*
