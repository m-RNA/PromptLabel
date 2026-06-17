# -*- mode: python ; coding: utf-8 -*-

import importlib.util
from pathlib import Path

block_cipher = None

datas = [
    ("ui/*.qss", "ui"),
    ("ui/*.png", "ui"),
    ("README_RELEASE.txt", "."),
    ("SAM_LICENSE.txt", "."),
]

sam3_spec = importlib.util.find_spec("sam3")
if sam3_spec and sam3_spec.submodule_search_locations:
    sam3_dir = Path(next(iter(sam3_spec.submodule_search_locations)))
    datas.append((str(sam3_dir), "sam3"))

hiddenimports = []

a = Analysis(
    ["main.py"],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="PromptLabel",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name="PromptLabel",
)
