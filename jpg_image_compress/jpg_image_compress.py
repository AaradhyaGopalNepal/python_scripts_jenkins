from pathlib import Path
from PIL import Image
import sys, zipfile

input_file = sys.argv[1]
output_dir = Path(sys.argv[2])
output_dir.mkdir(parents=True, exist_ok=True)

TARGET_SIZE = 950 * 1024  # 950 KB

def compress_image(file_path):
    img = Image.open(file_path)
    img = img.convert("RGB")
    quality = 95
    output_path = output_dir / file_path.name
    img.save(output_path, "JPEG", quality=quality)
    
    while output_path.stat().st_size > TARGET_SIZE and quality > 10:
        quality -= 5
        img.save(output_path, "JPEG", quality=quality)
    
    final_size = output_path.stat().st_size / 1024
    print(f"Compressed {file_path.name} to {final_size:.1f} KB at quality={quality}")

path = Path(input_file)
if path.suffix.lower() == ".zip":
    with zipfile.ZipFile(path, 'r') as z:
        z.extractall(output_dir / "temp")
    for f in (output_dir / "temp").rglob("*.jpg"):
        compress_image(f)
else:
    compress_image(path)

