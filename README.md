<div align="center">

# BatHealth

[![Version](https://img.shields.io/badge/version-1.0-blue.svg)](#)
[![Platform](https://img.shields.io/badge/platform-Windows-blueviolet.svg)](#)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](#)

**A lightweight, zero-admin battery health checker for Windows**

</div>

---

## Features

BatHealth provides a standalone Windows application designed for quick battery health assessment.  
Built to be **lightweight**, **permission-free**, and **fast**.

- **No Admin Required:** Runs with standard user privileges using direct Win32 API calls.
- **Zero Dependencies:** Standalone executable; no Python installation or external tools needed.
- **Direct API Access:** Queries Windows battery driver via native Win32 Battery IOCTL API instead of subprocess calls.
- **Instant Results:** Displays comprehensive battery metrics immediately upon launch.
- **Offline Support:** Core features remain fully functional without internet connectivity.

## Battery Metrics

| Metric           | Description                                   |
|------------------|-----------------------------------------------|
| Battery Health   | Percentage with visual bar and status rating   |
| Full Capacity    | Current maximum charge capacity in mWh         |
| Design Capacity  | Original factory capacity in mWh               |
| Cycle Count      | Number of charge cycles (if reported)          |
| Chemistry        | Battery chemistry type (Li-Ion, NiMH, etc.)   |

## Health Ratings

| Range       | Rating    |
|-------------|-----------|
| 90 – 100%   | Excellent |
| 75 – 89%    | Good      |
| 50 – 74%    | Fair      |
| 25 – 49%    | Poor      |
| 0 – 24%     | Critical  |

---

## Installation Guide

Follow these steps to install BatHealth locally.

### Prerequisites

- **Windows 7 or higher**
- **Python 3.7+** (for building from source only)

---

### Step 1: Get the Code

```bash
git clone https://github.com/Huerte/bathealth.git
cd bathealth
```

---

### Step 2: Build (If Applicable)

To build the executable from source:

```bash
build.bat
```

---

### Step 3: Run

**Pre-built Executable:**
```bash
dist\BatHealth.exe
```

**From Source:**
```bash
python src/bathealth.py
```

---

## Usage

1. **Launch the Application** – Double-click `BatHealth.exe` or run from command line
2. **View Battery Data** – Instantly displays battery health percentage, capacity, and chemistry
3. **Check Health Rating** – Compare your battery's status against the health rating scale
4. **No Configuration Needed** – Works immediately upon launch with no setup required

---

## Project Structure

```
bathealth/
│
├── src/
│   └── bathealth.py           # Core application logic and Win32 API integration
│
├── assets/
│   └── icon.ico               # Application icon
│
├── installer/
│   └── installer.iss          # Inno Setup installer configuration
│
├── build/                     # PyInstaller build artifacts (generated)
├── dist/                      # Compiled executable output
│
├── build.bat                  # One-click build automation script
├── bathealth.spec             # PyInstaller configuration file
├── .gitignore
└── README.md
```

---

## Building a Windows Installer

To create a distributable installer:

1. Install [Inno Setup](https://jrsoftware.org/isinfo.php)
2. Open `installer/installer.iss` in Inno Setup Compiler
3. Click **Build → Compile**
4. The installer will be created in the `Output/` folder

---

## How It Works

BatHealth interfaces directly with Windows' battery subsystem through Win32 IOCTL calls, bypassing the need for PowerShell, Command Prompt subprocesses, or administrative privileges. This approach ensures:

- **Fast execution** – Direct API access with minimal overhead
- **No privilege escalation** – Standard user permissions sufficient
- **Reliable results** – Direct communication with OS battery driver

---

## Contributing

1. Fork the Project  
2. Create a Feature Branch (`git checkout -b feature/enhancement`)  
3. Commit Changes (`git commit -m 'Add enhancement'`)  
4. Push to Branch (`git push origin feature/enhancement`)  
5. Open a Pull Request  

---

## License

Distributed under the MIT License. See `LICENSE` for details.

---

© 2026 [Huerte](https://github.com/Huerte). All Rights Reserved.
