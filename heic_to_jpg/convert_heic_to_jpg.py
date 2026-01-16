import os
import sys
from pathlib import Path
from PIL import Image
import zipfile

# Input arguments
input_file = sys.argv[1]  # single file or zip
output_dir = Path(sys.argv[2])
output_dir.mkdir(parents=True, exist_ok=True)

def convert_heic_to_jpg(heic_path, out_dir):
    try:
        with Image.open(heic_path) as img:
            jpg_path = out_dir / (heic_path.stem + ".jpg")
            img.convert("RGB").save(jpg_path, "JPEG")
            print(f"Converted: {heic_path.name} -> {jpg_path}")
    except Exception as e:
        print(f"Failed to convert {heic_path}: {e}")

input_path = Path(input_file)

if input_path.suffix.lower() == ".zip":
    with zipfile.ZipFile(input_path, 'r') as zip_ref:
        zip_ref.extractall(output_dir / "temp")
    for heic_file in (output_dir / "temp").rglob("*.heic"):
        convert_heic_to_jpg(heic_file, output_dir)
else:
    convert_heic_to_jpg(input_path, output_dir)

print(f"All JPGs saved in: {output_dir}")

