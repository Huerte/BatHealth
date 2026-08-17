<div align="center">

# BatHealth

<p align="center">
  <img width="950" height="500" alt="BatHealth screenshot" src="https://github.com/user-attachments/assets/b9808855-d250-4635-9f19-ee5d99681ef0" />
</p>

[![Version](https://img.shields.io/badge/version-1.0.1-blue.svg)](#)
[![Platform](https://img.shields.io/badge/platform-Windows-blueviolet.svg)](#)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](#)

**A lightweight, zero-admin battery health checker for Windows.**

[Report a Bug](https://github.com/Huerte/BatHealth/issues) · [Request a Feature](https://github.com/Huerte/BatHealth/issues)

</div>

---

<p align="center">
  BatHealth reads your battery's health directly from Windows. No admin password needed. No internet connection. No installation wizard if you don't want one. Run it and your results appear instantly.
</p>

---

## Table of Contents

- [Installation Guide](#installation-guide)
- [What It Shows](#what-it-shows)
- [How It Works](#how-it-works)
- [Health Ratings](#health-ratings)
- [Contributing](#contributing)
- [Creator](#creator)
- [License](#license)

---

## Installation Guide

There are two ways to get BatHealth. Pick whichever fits you.

### Option A: Download the Installer (Recommended)

You do not need Python, Git, or any technical knowledge for this option.

1. Go to the [**Releases**](https://github.com/Huerte/BatHealth/releases) page.
2. Under the latest release, click **`BatHealth_Setup_v1.0.1.exe`** to download it.
3. Double-click the downloaded file to open the setup wizard.
4. Click **Next → Install → Finish**.
5. Find the **BatHealth** shortcut on your Desktop or in the Start Menu and open it.

> **Note:** If Windows shows a warning saying "Windows protected your PC", click **More info** then **Run anyway**. This appears because the app is new and does not yet have a paid code-signing certificate. The app itself is safe.

---

### Option B: Build from Source (For developers)

Use this if you want to read the code, modify it, or compile the installer yourself.

**Prerequisites:**

| What you need | Where to get it |
|---------------|-----------------|
| Python 3.7+   | [python.org](https://www.python.org/downloads/) |
| Windows OS    | Already on your machine |

**Steps:**

1. Clone the repository:
   ```
   git clone https://github.com/Huerte/BatHealth.git
   cd BatHealth
   ```

2. Run the build script:
   ```
   build.bat
   ```

The script handles everything automatically:

- Installs **PyInstaller** if you don't have it, then compiles `src/bathealth.py` into `dist/BatHealth.exe`.
- Installs **Inno Setup** via `winget` if you don't have it, then compiles the installer to `Output/BatHealth_Setup_v1.0.1.exe`.

After the script finishes you can run the standalone `dist/BatHealth.exe` directly, or distribute the installer from the `Output/` folder.

**Project structure:**

```
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
└── README.md                 # This file
```

---

## What It Shows

When you open BatHealth, a small window appears at the top-left corner of your screen with the following information:

| Metric           | What it means                                                                                         |
|------------------|-------------------------------------------------------------------------------------------------------|
| Battery Health   | A percentage showing how much capacity remains compared to when the battery was new. Includes a color-coded bar and a label (Excellent, Good, Fair, Poor, Critical). |
| Full Capacity    | The maximum charge your battery can hold right now, in mWh.                                           |
| Design Capacity  | The maximum charge the battery was designed to hold when it was new, in mWh.                          |
| Cycle Count      | How many full charge cycles the battery has completed (shown only if your battery reports this).       |
| Chemistry        | The battery technology type, for example: Li-Ion, LiP.                                               |

---

## How It Works

BatHealth talks directly to the Windows battery driver using the built-in Win32 Battery IOCTL API. This is the same interface that Windows itself uses internally.

- No `powercfg` command is used.
- No administrator privileges are required.
- No data is sent anywhere. Everything stays on your machine.

The window opens at the top-left corner of your screen at a compact size so it stays out of the way. Press any key to close it when you are done.

---

## Health Ratings

BatHealth uses the following scale to rate your battery:

| Range       | Rating    | What it means                            |
|-------------|-----------|------------------------------------------|
| 90-100%     | Excellent | Battery is in great condition            |
| 75-89%      | Good      | Normal wear, still healthy               |
| 50-74%      | Fair      | Noticeable degradation, monitor closely  |
| 25-49%      | Poor      | Consider replacing your battery          |
| 0-24%       | Critical  | Battery needs immediate replacement      |

---

## Contributing

Contributions are welcome. Here is how to go from zero to a submitted pull request.

### Getting Started

**Prerequisites:** Python 3.7+ and Git.

**Fork and clone:**

```
# 1. Fork the repo on GitHub, then clone your fork
git clone https://github.com/YOUR_USERNAME/BatHealth.git
cd BatHealth

# 2. Keep your fork in sync with the original
git remote add upstream https://github.com/Huerte/BatHealth.git
```

### Making Changes

**Branch naming:**

```
feat/short-description    # New features
fix/short-description     # Bug fixes
docs/short-description    # Documentation only
chore/short-description   # Maintenance or refactoring
```

**Commit messages:** Use plain English. Describe what changed and why:

```
# Good
git commit -m "fix: handle no-battery case when device has no ACPI battery"
git commit -m "feat: add voltage reading to the output display"
git commit -m "docs: clarify installer warning in README"

# Avoid
git commit -m "fix stuff"
git commit -m "update"
```

**Code style:**

- Follow the existing patterns in `src/bathealth.py`. One file, keep it readable.
- Keep functions short. If something is growing, split it.
- Add a comment when the purpose of something is not immediately obvious.
- Never swallow exceptions silently with a bare `except: pass` unless the operation is purely cosmetic.

### Submitting a Pull Request

1. Push your branch to your fork:
   ```
   git push origin feat/your-feature
   ```

2. Open a Pull Request against `Huerte/BatHealth:main` on GitHub.

3. In the PR description, briefly explain: what you changed, why, and how to test it.

4. If your change affects the app's output or behavior, update this README accordingly.

---

## Contributor

<div align="center">
  <table>
    <tr>
      <td align="center"><a href="https://github.com/Huerte"><img src="https://github.com/Huerte.png" width="80px;" alt=""/></a><br /><a href="https://github.com/Huerte"><b>Huerte</b></a><br />Creator</td>
    </tr>
  </table>
</div>

---

## License

Distributed under the **MIT** License. See [`LICENSE`](LICENSE) for details.

---

*Built to make battery health monitoring accessible to everyone.*
