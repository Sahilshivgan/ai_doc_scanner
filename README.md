# 📄 AI Document Scanner & OCR (Desktop App)

## 🚀 Overview
The **AI Document Scanner & OCR** is a Python-based desktop application built with **PyQt5**, **OpenCV**, and **Tesseract OCR**.  
It allows users to:
- Scan documents from **images or webcam**  
- Automatically **detect & crop** documents  
- Enhance image quality (brightness control)  
- Extract **editable text** from documents  
- Save as **image** or **searchable PDF**  

---

## ✨ Features
✅ Open images from file explorer  
✅ Capture from webcam in real-time  
✅ Automatic edge detection & perspective correction  
✅ Brightness adjustment slider  
✅ OCR text extraction using Tesseract  
✅ Save cropped images in JPG/PNG format  
✅ Export as **searchable PDF** (text + images)  

---

## 🖼 Screenshots
*(Place your screenshots inside the `assets/` folder and update paths below)*

### Main Interface
![Main UI](assets/main_ui.png)

### OCR Extraction
![OCR Text](assets/ocr_text.png)

---

## 📂 Project Structure
ai_doc_scanner/
│── src/
│ ├── main.py # Main application
│ ├── scanner.py # Image processing functions
│ ├── ocr_utils.py # OCR utilities
│── assets/
│ ├── icons/ # App icons
│ ├── sample.jpg # Sample document
│── requirements.txt
│── README.md


---

## ⚙️ Installation

### 1️⃣ Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/ai_doc_scanner.git
cd ai_doc_scanner

2️⃣ Create a virtual environment & install dependencies
python -m venv venv
venv\Scripts\activate   # Windows
pip install -r requirements.txt
3️⃣ Install Tesseract OCR

make a file
Install to:C:\Program Files\Tesseract-OCR\


Add to PATH or set in code:
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

▶️ Running the App

python src/main.py


💡 Future Improvements
📑 Batch scanning for multiple images

🤖 AI-based document classification

☁️ Cloud sync for scanned files

🌙 Dark mode toggle

📝 License
This project is licensed under the MIT License. Feel free to use and modify it.

📌 Author: sahil shivgan
⭐ If you like this project, consider giving it a star!




