# -*- mode: python ; coding: utf-8 -*-

import sys
import os

spec_dir = os.path.dirname(os.path.abspath(SPEC))
icon_path = os.path.join(spec_dir, "assets", "icon.ico")

a = Analysis(
    [os.path.join(spec_dir, "src", "bathealth.py")],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        "tkinter", "_tkinter", "unittest", "email",
        "html", "http", "xml", "pydoc", "doctest",
        "argparse", "difflib", "inspect", "calendar",
        "pickle", "shelve", "sqlite3", "decimal",
        "fractions", "csv", "configparser", "textwrap",
    ],
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name="BatHealth",
    debug=False,
    bootloader_ignore_signals=False,
    strip=True,
    upx=True,
    console=True,
    icon=icon_path if os.path.exists(icon_path) else None,
)
