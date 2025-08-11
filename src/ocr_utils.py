# src/ocr_utils.py
import pytesseract
import numpy as np
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.utils import ImageReader
import io

def do_ocr(cv_img, lang='eng'):
    # cv_img is BGR numpy array
    img_rgb = cv_img[:,:,::-1]
    pil = Image.fromarray(img_rgb)
    text = pytesseract.image_to_string(pil, lang=lang)
    return text

def save_pdf_with_text(pages, out_path, page_size=A4):
    """
    pages: list of (PIL.Image, text)
    Saves a PDF with image for each page and OCR text below the image.
    """
    c = canvas.Canvas(out_path, pagesize=page_size)
    width, height = page_size
    for pil, text in pages:
        # fit image to page width with margin
        img_w, img_h = pil.size
        scale = min((width-100)/img_w, (height-200)/img_h, 1.0)
        new_w = img_w * scale
        new_h = img_h * scale
        x = (width - new_w) / 2
        y = height - new_h - 100
        image_stream = ImageReader(pil)
        c.drawImage(image_stream, x, y, new_w, new_h)
        # draw OCR text below image
        text_x = 50
        text_y = y - 80
        c.setFont("Helvetica", 10)
        # wrap text
        lines = text.splitlines()
        for line in lines:
            c.drawString(text_x, text_y, line[:200])
            text_y -= 12
            if text_y < 50:
                c.showPage()
                text_y = height - 50
        c.showPage()
    c.save()
