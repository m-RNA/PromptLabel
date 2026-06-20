# -*- mode: python ; coding: utf-8 -*-

import fnmatch
import importlib.util
from pathlib import Path

block_cipher = None

datas = [
    ("assets/promptlabel_pl.ico", "assets"),
    ("assets/promptlabel_pl.png", "assets"),
    ("ui/*.qss", "ui"),
    ("ui/*.png", "ui"),
    ("README_RELEASE.txt", "."),
    ("SAM_LICENSE.txt", "."),
]


def _append_package_sources(package_dir, package_name, excluded_dirs=None):
    excluded_dirs = set(excluded_dirs or [])
    for source_path in package_dir.rglob("*.py"):
        rel_path = source_path.relative_to(package_dir)
        if any(part in excluded_dirs for part in rel_path.parts):
            continue
        datas.append((str(source_path), str(Path(package_name) / rel_path.parent)))


sam3_spec = importlib.util.find_spec("sam3")
if sam3_spec and sam3_spec.submodule_search_locations:
    sam3_dir = Path(next(iter(sam3_spec.submodule_search_locations)))
    bpe_vocab = sam3_dir / "assets" / "bpe_simple_vocab_16e6.txt.gz"
    if bpe_vocab.exists():
        datas.append((str(bpe_vocab), "sam3/assets"))
    _append_package_sources(sam3_dir, "sam3", excluded_dirs={"agent", "eval", "__pycache__"})

hiddenimports = []
excludes = [
    # UI and SAM inference do not use SAM3's agent/eval/demo visualization helpers.
    "sam3.agent",
    "sam3.eval",
    "sam3.visualization_utils",
    # Keep PyTorch/CUDA runtime, but skip optional tooling that pulls in bulky extras.
    "IPython",
    "jupyter",
    "matplotlib",
    "llvmlite",
    "numba",
    "notebook",
    "pandas",
    "pytest",
    "scipy",
    "skimage",
    "sklearn",
    "tensorboard",
    "tkinter",
    "torchaudio",
    "torch.utils.tensorboard",
]


def _toc_name(item):
    return item[0].replace("/", "\\")


def _drop_toc_items(toc, patterns):
    return [item for item in toc if not any(fnmatch.fnmatchcase(_toc_name(item), pattern) for pattern in patterns)]

a = Analysis(
    ["main.py"],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=excludes,
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
    module_collection_mode={
        "enum": "pyz+py",
    },
)

a.binaries = _drop_toc_items(
    a.binaries,
    [
        # The app uses Windows GUI rendering only; ANGLE/software OpenGL fallback is not needed.
        "PySide6\\opengl32sw.dll",
        "PySide6\\Qt6Pdf.dll",
        "PySide6\\Qt6Qml.dll",
        "PySide6\\Qt6QmlModels.dll",
        "PySide6\\Qt6Quick.dll",
        "PySide6\\Qt6VirtualKeyboard.dll",
        "PySide6\\plugins\\generic\\*",
        "PySide6\\plugins\\iconengines\\qsvgicon.dll",
        "PySide6\\plugins\\networkinformation\\*",
        "PySide6\\plugins\\platforminputcontexts\\*",
        "PySide6\\plugins\\platforms\\qdirect2d.dll",
        "PySide6\\plugins\\platforms\\qminimal.dll",
        "PySide6\\plugins\\platforms\\qoffscreen.dll",
        # Image annotation only needs common raster formats.
        "PySide6\\plugins\\imageformats\\qicns.dll",
        "PySide6\\plugins\\imageformats\\qpdf.dll",
        "PySide6\\plugins\\imageformats\\qsvg.dll",
        "PySide6\\plugins\\imageformats\\qtga.dll",
        "PySide6\\plugins\\imageformats\\qtiff.dll",
        "PySide6\\plugins\\imageformats\\qwbmp.dll",
        "PySide6\\plugins\\imageformats\\qwebp.dll",
        "PySide6\\plugins\\tls\\*",
        # OpenCV video I/O is unused; keep cv2 core image processing.
        "cv2\\opencv_videoio_ffmpeg*.dll",
        # Pythonwin/pywin32 GUI helpers are not used by the application.
        "Pythonwin\\*",
        "pywin32_system32\\*",
        "win32\\*",
        "win32com\\*",
        "llvmlite.libs\\*",
        "scipy.libs\\*",
        # CUDA profiling helpers are optional and not required for inference.
        "torch\\lib\\cupti64_*.dll",
        "torch\\lib\\nvToolsExt64_*.dll",
    ],
)
a.datas = _drop_toc_items(
    a.datas,
    [
        "PySide6\\translations\\*",
        "Pythonwin\\*",
        "pywin32_system32\\*",
        "win32\\*",
        "win32com\\*",
        "llvmlite.libs\\*",
        "scipy.libs\\*",
    ],
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
    icon="assets/promptlabel_pl.ico",
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
