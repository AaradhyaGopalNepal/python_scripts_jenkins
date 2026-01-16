# Jenkins Freestyle Job: Images to PDF

## Bash Script and Setup

```bash
#!/bin/bash
set -e

# Pull the latest Python scripts from GitHub
if [ -d "$WORKSPACE/python_scripts" ]; then
    cd "$WORKSPACE/python_scripts"
    git fetch --all
    git reset --hard origin/main
else
    git clone -b main https://github.com/AaradhyaGopalNepal/python_scripts_jenkins.git "$WORKSPACE/python_scripts"
    cd "$WORKSPACE/python_scripts/images_to_pdf"
fi

# Create virtualenv and install dependencies
python3 -m venv "$WORKSPACE/venv"
. "$WORKSPACE/venv/bin/activate"
pip install --upgrade pip pillow

# Make output folder
mkdir -p "$WORKSPACE/output"

# Copy uploaded file to workspace (Freestyle job automatically puts it as input_file)
cp "$WORKSPACE/input_file" "$WORKSPACE/python_scripts/images_to_pdf/uploaded.zip"

# Run the Python script
python "$WORKSPACE/python_scripts/images_to_pdf/images_to_pdf.py" "$WORKSPACE/python_scripts/images_to_pdf/uploaded.zip" "$WORKSPACE/output/result.pdf"

echo "PDF created: $WORKSPACE/output/result.pdf"

# Output files
# All PDFs will be saved to: output/*.pdf
# Jenkins will archive these files for download
```

## Jenkins Freestyle Job Setup

1. Go to **Jenkins → New Item → Freestyle project**, give it a name, click OK.  
2. Enable **This project is parameterized**, click **Add Parameter → File Parameter**:  
   - Name: `input_file`  
   - Description: `Upload a ZIP of images`  
3. Add **Build Step → Execute shell**, paste the bash script above.  
4. Add **Post-build Action → Archive the artifacts**, set **Files to archive:** `output/*.pdf`.  
5. Save the job.

## How to Use

1. Click **Build with Parameters**, upload your ZIP of images.  
2. Jenkins will:  
   - Pull latest scripts from GitHub  
   - Create virtualenv and install Pillow  
   - Convert images to PDF  
   - Save PDF in `output/result.pdf`  
3. After build completion, scroll to **Archived Artifacts**, click `result.pdf` to download.

## Notes

- The Python script should ignore hidden macOS files (`__MACOSX` / `._`)  
- You can upload **single images or ZIP of images**  
- The job automatically pulls the latest scripts each build
