# PromptLabel

**Language**: [中文](README.md) | English

<p align="center">
  <img src="assets/promptlabel_pl.png" alt="PromptLabel icon" width="96">
</p>

PromptLabel is an image annotation workbench adapted from [LabelPaw](https://github.com/luohuabuxiema/LabelPaw). This branch is not an official version from the original author. Its focus is not adding another annotation format, but adjusting the interface and small workflow details for practical labeling work.

## Core Highlights

### One Class, Multiple Prompts

This is the most important change in PromptLabel.

In the original tool, the relationship between classes and prompts is not ideal for workflows where different phrases may refer to the same target. PromptLabel allows one YOLO class to bind multiple prompt aliases, for example:

```text
helmet
├─ helmet
├─ hard hat
└─ safety helmet
```

When using SAM text prompts, you can search for targets with any alias. Saving and exporting still write only the same YOLO class, such as `helmet`. This keeps prompt wording flexible without polluting the training dataset classes.

### Fewer Mouse Clicks, Faster Shortcuts

PromptLabel moves frequent actions in continuous annotation to the keyboard: `A` / `D` switch images, `1` - `9` switch the active class, `Q` / `Space` toggle SAM, and `R` submits the prompt. Combined with auto-save, status-bar feedback, and the annotation list on the right, common workflows can be completed with fewer mouse clicks and fewer interruptions.

### Left-Side Image Gallery

After opening a directory, images in the current folder are shown as an image queue on the left. Thumbnails, file names, and the total image count are visible directly. Continuous annotation no longer requires repeatedly opening the file picker, making it easier to scan through a whole folder quickly.

### Compact Annotation Workbench

The interface is reorganized into a left image queue, central canvas, right class/annotation management panel, and bottom SAM workflow. Compared with the original interface, PromptLabel emphasizes canvas space, information density, and fewer interruptions.

### Screenshots

The main interface is organized around "image queue - canvas - management panel - SAM workflow", suitable for continuous image switching, annotation, and review:

![PromptLabel main interface](assets/readme_main_ui.png)

### Smaller Quality-of-Life Improvements

- Scrolling the prompt combo box only switches its content and does not accidentally submit a SAM prompt.
- The label combo box supports smooth mouse-wheel switching of the active class.
- Annotation boxes support optional breathing highlight, making existing annotations easier to identify quickly.
- The class tree directly manages prompt aliases, colors, and show/hide state.
- The annotation list is grouped by rectangle, polygon, point, and rotated box, with selection, batch relabeling, and deletion support.
- Canvas right-click supports switching the active label, batch-changing selected annotation classes, and toggling SAM.
- Common actions have keyboard paths, reducing mouse clicks when switching images, modes, classes, and submitting prompts.
- The status bar shows the total annotation count and per-class counts for the current annotation mode.
- Image switching debounces SAM analysis, so continuously pressing `A` / `D` does not run the model immediately for every image.
- Fewer toast messages are used; more information is placed in the status bar to avoid covering the canvas.
- Small triangle styles for combo boxes and tree controls are unified and visible in both dark and light themes.

## Preserved Features

- Annotation formats: `JSON` / `YOLO` / `XML`
- Annotation types: rectangle, polygon, point, rotated box
- SAM3 assistance: point selection, text prompts, reference search
- Class management: add, edit, delete, color, show/hide, prompt aliases
- Image directory: thumbnail queue, image count statistics, previous/next image, right-click image and annotation deletion
- Common operations: auto-save, undo, redo, delete, batch selection, batch annotation class changes, current mode and annotation count statistics
- Dataset processing: train/validation/test split, JSON/XML to YOLO, JSON to U-Net Mask

## Model Notes

Release packages do not include `models/sam3.pt`. When the model is missing, the main interface can still open, and manual annotation plus dataset processing remain available. SAM assistance is unavailable. On startup, you can also click "I have downloaded it" to select an existing `sam3.pt` file directly; the program remembers the path and does not require copying it into the project directory.

Prefer downloading from official sources:

- [facebook/sam3 on Hugging Face](https://huggingface.co/facebook/sam3/tree/main)
- [facebookresearch/sam3](https://github.com/facebookresearch/sam3)

Backup download:

- [Baidu Netdisk sam3.pt](https://pan.baidu.com/s/11rKzO6W5b_i8aOFcd9xOzA?pwd=6666), extraction code: `6666`

`sam3.pt` belongs to SAM Materials and is governed by `SAM_LICENSE.txt`. The backup download is only provided for convenience. Confirm compliance with Meta's SAM License before use or redistribution.

After downloading, select the file directly in the startup dialog, or place it at the default path:

```text
models/sam3.pt
```

## How to Run

### Beta Portable Package

1. Download the `PromptLabel-vX.X.X` portable package from the Release page.
2. Extract it into one directory.
3. Put `sam3.pt` at `models/sam3.pt`.
4. Double-click `PromptLabel.exe` to start.

### Run from Source

Recommended environment: Windows + Python 3.11 + NVIDIA CUDA.

```powershell
python -m venv .venv311
.\.venv311\Scripts\pip install -r requirements.txt
.\.venv311\Scripts\python main.py
```

### Local Packaging

The repository includes `PromptLabel.spec`. Before packaging, make sure dependencies and PyInstaller are installed in `.venv311`:

```powershell
.\.venv311\Scripts\pip install pyinstaller
.\.venv311\Scripts\pyinstaller.exe --clean --noconfirm PromptLabel.spec
```

The output directory is `dist\PromptLabel\`. Release packages should not include `models\sam3.pt`, `.sam3_tmp\`, logs, caches, or local test images. Users can select an existing model file on first launch or place it at `models\sam3.pt`.

## Shortcuts

| Shortcut | Function |
| -------- | -------- |
| `A` / `←` | Previous image |
| `D` / `→` | Next image |
| `R` | Submit SAM prompt |
| `B` / `P` / `T` / `O` | Rectangle / polygon / point / rotated box |
| `Q` / `Space` | Toggle SAM |
| `F` / `0` / `Del` / `Backspace` | Delete selected annotation |
| `Ctrl + Z` | Undo |
| `Ctrl + Y` / `Ctrl + Shift + Z` | Redo |
| `Ctrl + A` | Select all annotations in the current annotation-type group |
| `1` - `9` | Switch active class |
| `↑` / `W` | Select previous annotation in the current annotation-type list |
| `↓` / `S` | Select next annotation in the current annotation-type list |
| `E` | Change selected annotation label |
| `F1` | Open help |

## Context Menus

- Canvas right-click: toggle SAM, submit SAM prompt, switch active label, create label; when the cursor is on selected annotations, batch-change selected annotation classes.
- Right annotation list right-click: batch-change annotation classes and batch-delete annotations.
- Left image queue right-click: copy file name, open containing folder, delete image and same-name annotation files.

## Auto-Save and Status Bar

PromptLabel uses auto-save as the primary workflow and no longer treats "Save" as a high-frequency button. Switching images, editing annotations, deleting annotations, and similar operations are automatically saved to the current format.

The status bar shows statistics for the current annotation mode, for example:

```text
Stats: Rectangle | Total: 12 | helmet: 5, vest: 7
```

## License

This project follows the original project license and keeps `SAM_LICENSE.txt` for SAM3-related license information.
