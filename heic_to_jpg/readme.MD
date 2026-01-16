# HEIC to JPG Conversion - Jenkins Automation

## Overview

This project converts HEIC/HEIF images to JPG using Python and Jenkins.
It supports:

* Single `.heic` or `.heif` file
* Multiple images in a `.zip` file
* Case-insensitive extensions (`.HEIC`, `.HEIF`)

All outputs are saved to `$WORKSPACE/output` and ready for Jenkins artifact archiving.

---

## Folder Structure

```
heic_to_jpg/
├─ convert_heic_to_jpg.py    # Python conversion script
└─ run_heic_to_jpg.sh        # Bash wrapper for Jenkins
```

---

## Python Script: `convert_heic_to_jpg.py`

**Purpose:** Converts HEIC/HEIF images to JPG.
**Dependencies:** `pillow`, `pillow-heif`

```python
import sys
from pathlib import Path
from PIL import Image, UnidentifiedImageError
from pillow_heif import register_heif_opener
import zipfile

register_heif_opener()

input_file = sys.argv[1]
output_dir = Path(sys.argv[2])
output_dir.mkdir(parents=True, exist_ok=True)

def convert_heic_to_jpg(path, out_dir):
    try:
        with Image.open(path) as img:
            jpg_path = out_dir / (path.stem + ".jpg")
            img.convert("RGB").save(jpg_path, "JPEG")
            print(f"Converted: {path.name} -> {jpg_path.name}")
    except UnidentifiedImageError:
        print(f"ERROR: {path} is not a valid HEIC/HEIF image")
    except Exception as e:
        print(f"Failed to convert {path}: {e}")

input_path = Path(input_file)

if input_path.suffix.lower() == ".zip":
    with zipfile.ZipFile(input_path, 'r') as zip_ref:
        zip_ref.extractall(output_dir / "temp")
    heic_files = list((output_dir / "temp").rglob("*.[hH][eE][iI][cFf]"))
    if not heic_files:
        print("ERROR: ZIP contains no HEIC/HEIF images!")
    for f in heic_files:
        convert_heic_to_jpg(f, output_dir)
elif input_path.suffix.lower() in [".heic", ".heif"]:
    convert_heic_to_jpg(input_path, output_dir)
else:
    convert_heic_to_jpg(input_path, output_dir)

print(f"All JPGs saved in: {output_dir}")
```

---

## Bash Wrapper: `run_heic_to_jpg.sh`

**Purpose:** Pulls latest scripts, sets up Python environment, and runs the converter.

```bash
#!/bin/bash
set -e

# Pull latest Python scripts
if [ -d "$WORKSPACE/python_scripts" ]; then
    cd "$WORKSPACE/python_scripts"
    git fetch --all
    git reset --hard origin/main
else
    git clone -b main https://github.com/AaradhyaGopalNepal/python_scripts_jenkins.git "$WORKSPACE/python_scripts"
fi

cd "$WORKSPACE/python_scripts/heic_to_jpg"

# Setup virtualenv and install dependencies
python3 -m venv "$WORKSPACE/venv"
. "$WORKSPACE/venv/bin/activate"
pip install --upgrade pip pillow pillow-heif

# Prepare output folder
mkdir -p "$WORKSPACE/output"

# Copy uploaded file
cp "$WORKSPACE/input_file" "$WORKSPACE/python_scripts/heic_to_jpg/uploaded_input"

# Run Python script
python convert_heic_to_jpg.py "$WORKSPACE/python_scripts/heic_to_jpg/uploaded_input" "$WORKSPACE/output"

echo "JPGs created: $WORKSPACE/output/*.jpg"
```

---

## Jenkins Setup

1. Create a Freestyle Jenkins job.
2. Add a **File Parameter** named `input_file`.
3. Copy the above Bash wrapper as the build step.
4. Ensure workspace has `$WORKSPACE/python_scripts` cloned from GitHub.
5. Configure **Post-build Actions** to archive artifacts:

   ```
   output/*.jpg
   ```

---

## Artifact Location

```
$WORKSPACE/output/*.jpg
```

---

## Common Pitfalls

1. Uploaded file must be `.heic`, `.HEIC`, `.heif`, `.HEIF`, or a `.zip` of HEIC/HEIF images.
2. Jenkins may rename uploaded files; the script handles any extension but ensures Pillow can read it.
3. If `output/*.jpg` is empty, check file type and that `pillow-heif` is installed.
4. ZIP files must contain `.heic` or `.heif` images (case-insensitive).

