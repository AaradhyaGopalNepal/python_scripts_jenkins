import sys
import zipfile
import tempfile
from pathlib import Path
from PIL import Image

# Usage: python images_to_pdf.py <input_path> <output_pdf>
# input_path: single image OR zip of images

def extract_images(input_path: Path, workdir: Path):
    images = []
    if input_path.suffix.lower() == ".zip":
        with zipfile.ZipFile(input_path, "r") as z:
            z.extractall(workdir)
        images = sorted(
            p for p in workdir.rglob("*")
            if p.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp"}
            and not p.name.startswith("._")  # <- ignore macOS resource forks
            and "__MACOSX" not in str(p)     # <- ignore __MACOSX folder
        )
    else:
        images = [input_path]
    return images


def main():
    if len(sys.argv) != 3:
        print("Usage: python images_to_pdf.py <input_path> <output_pdf>")
        sys.exit(1)

    input_path = Path(sys.argv[1])
    output_pdf = Path(sys.argv[2])
    output_pdf.parent.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory() as tmp:
        workdir = Path(tmp)
        image_paths = extract_images(input_path, workdir)
        if not image_paths:
            raise RuntimeError("No images found")

        pil_images = []
        for p in image_paths:
            img = Image.open(p).convert("RGB")
            pil_images.append(img)

        first, rest = pil_images[0], pil_images[1:]
        first.save(output_pdf, save_all=True, append_images=rest)

    print(f"PDF created: {output_pdf}")

if __name__ == "__main__":
    main()

