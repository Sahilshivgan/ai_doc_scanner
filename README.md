# AI Document Scanner (Desktop)

A professional-looking desktop Document Scanner & OCR app built with PyQt5, OpenCV and Tesseract OCR.
This project is resume-ready and includes features:
- Open image or capture from webcam
- Auto-detect document edges and perspective-correct (auto-crop)
- Simple image enhancement (contrast/brightness)
- OCR extraction using Tesseract (pytesseract)
- Export as image or PDF with extracted text
- Multi-page PDF support (add pages then export)

## Requirements
- Python 3.8+
- Tesseract OCR binary must be installed separately:
  - Windows: https://github.com/tesseract-ocr/tesseract/wiki/Downloads
  - Ubuntu: `sudo apt install tesseract-ocr`
  - MacOS (brew): `brew install tesseract`

Install Python dependencies:
```
pip install -r requirements.txt
```

## Run
```
python src/main.py
```

## Packaging (optional)
Create a single executable using PyInstaller:
```
pip install pyinstaller
pyinstaller --onefile --add-data "assets;assets" src/main.py
```

## Notes
- The exported PDF contains the scanned image and the OCR text below it.
- For a fully searchable PDF (invisible text overlay), advanced PDF text-positioning is required; this project prioritizes clarity and portability.
