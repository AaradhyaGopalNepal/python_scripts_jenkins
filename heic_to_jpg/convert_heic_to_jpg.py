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
    # Try opening anyway for unknown extensions
    convert_heic_to_jpg(input_path, output_dir)

print(f"All JPGs saved in: {output_dir}")
