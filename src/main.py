#!/usr/bin/env python3
"""
src/main.py
Main PyQt5 desktop app for AI Document Scanner & OCR
"""
import sys, os, tempfile
from PyQt5 import QtWidgets, QtGui, QtCore
from scanner import detect_document_edges, four_point_transform, enhance_image, load_image_cv, save_image_cv
from ocr_utils import do_ocr, save_pdf_with_text
import cv2
from PIL import Image

ASSETS_DIR = os.path.join(os.path.dirname(__file__), "..", "assets")

class ScannerApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AI Document Scanner")
        self.setGeometry(200, 100, 1000, 700)
        self.image_path = None
        self.cv_img = None
        self.cropped_img = None
        self.pages = []  # list of (PIL Image, ocr_text)
        self.init_ui()

    def init_ui(self):
        central = QtWidgets.QWidget()
        self.setCentralWidget(central)
        layout = QtWidgets.QHBoxLayout(central)

        # Left: controls
        ctrl = QtWidgets.QVBoxLayout()
        icon_dir = os.path.join(ASSETS_DIR, "icons")

        btn_open = QtWidgets.QPushButton(QtGui.QIcon(os.path.join(icon_dir, "open.png")), "Open Image")
        btn_open.clicked.connect(self.open_image)

        btn_cam = QtWidgets.QPushButton(QtGui.QIcon(os.path.join(icon_dir, "camera.png")), "Capture from Camera")
        btn_cam.clicked.connect(self.capture_camera)

        btn_autocrop = QtWidgets.QPushButton(QtGui.QIcon(os.path.join(icon_dir, "crop.png")), "Auto Crop / Detect Edges")
        btn_autocrop.clicked.connect(self.auto_crop)

        btn_ocr = QtWidgets.QPushButton(QtGui.QIcon(os.path.join(icon_dir, "ocr.png")), "Extract OCR Text")
        btn_ocr.clicked.connect(self.extract_ocr)

        btn_add_page = QtWidgets.QPushButton(QtGui.QIcon(os.path.join(icon_dir, "add_page.png")), "Add Page to Document")
        btn_add_page.clicked.connect(self.add_page)

        btn_save_img = QtWidgets.QPushButton(QtGui.QIcon(os.path.join(icon_dir, "save.png")), "Save Cropped Image")
        btn_save_img.clicked.connect(self.save_cropped_image)

        btn_save_pdf = QtWidgets.QPushButton(QtGui.QIcon(os.path.join(icon_dir, "pdf.png")), "Export PDF (images + text)")
        btn_save_pdf.clicked.connect(self.export_pdf)

        self.brightness_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.brightness_slider.setRange(-50, 50)
        self.brightness_slider.setValue(0)
        self.brightness_slider.valueChanged.connect(self.apply_enhance)

        ctrl.addWidget(btn_open)
        ctrl.addWidget(btn_cam)
        ctrl.addWidget(btn_autocrop)
        ctrl.addWidget(QtWidgets.QLabel("Brightness"))
        ctrl.addWidget(self.brightness_slider)
        ctrl.addWidget(btn_ocr)
        ctrl.addWidget(btn_add_page)
        ctrl.addWidget(btn_save_img)
        ctrl.addWidget(btn_save_pdf)
        ctrl.addStretch()

        # Right: image view + OCR text
        right = QtWidgets.QVBoxLayout()
        self.image_label = QtWidgets.QLabel("No image loaded")
        self.image_label.setAlignment(QtCore.Qt.AlignCenter)
        self.image_label.setFixedSize(700, 500)
        self.image_label.setStyleSheet("border: 1px solid #444; background: #222; color: #eee;")
        self.ocr_text = QtWidgets.QTextEdit()
        self.ocr_text.setReadOnly(True)
        right.addWidget(self.image_label)
        right.addWidget(QtWidgets.QLabel("OCR Text"))
        right.addWidget(self.ocr_text)

        layout.addLayout(ctrl, 1)
        layout.addLayout(right, 3)

    def open_image(self):
        path, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open image", "", "Images (*.png *.jpg *.jpeg)")
        if path:
            self.image_path = path
            self.cv_img = load_image_cv(path)
            self.cropped_img = None
            self.show_image(self.cv_img)

    def capture_camera(self):
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            QtWidgets.QMessageBox.critical(self, "Camera Error", "Cannot access the camera.")
            return
        ret, frame = cap.read()
        cap.release()
        if ret:
            tmp = tempfile.NamedTemporaryFile(suffix=".jpg", delete=False)
            cv2.imwrite(tmp.name, frame)
            self.image_path = tmp.name
            self.cv_img = frame
            self.cropped_img = None
            self.show_image(self.cv_img)

    def auto_crop(self):
        if self.cv_img is None:
            return
        pts = detect_document_edges(self.cv_img)
        if pts is None:
            QtWidgets.QMessageBox.information(self, "No Document", "Could not detect document edges. Try higher contrast image.")
            return
        warped = four_point_transform(self.cv_img, pts)
        self.cropped_img = warped
        self.show_image(warped)

    def apply_enhance(self):
        if self.cropped_img is None and self.cv_img is None:
            return
        target = self.cropped_img if self.cropped_img is not None else self.cv_img
        val = self.brightness_slider.value()
        enhanced = enhance_image(target, brightness=val)
        self.show_image(enhanced)
        self.cropped_img = enhanced

    def extract_ocr(self):
        if self.cropped_img is None and self.cv_img is None:
            return
        target = self.cropped_img if self.cropped_img is not None else self.cv_img
        text = do_ocr(target)
        self.ocr_text.setPlainText(text)

    def add_page(self):
        if self.cropped_img is None and self.cv_img is None:
            return
        target = self.cropped_img if self.cropped_img is not None else self.cv_img
        pil = Image.fromarray(cv2.cvtColor(target, cv2.COLOR_BGR2RGB))
        text = do_ocr(target)
        self.pages.append((pil, text))
        QtWidgets.QMessageBox.information(self, "Page Added", f"Added page. Total pages: {len(self.pages)}")

    def save_cropped_image(self):
        if self.cropped_img is None:
            QtWidgets.QMessageBox.information(self, "No Image", "No cropped image to save.")
            return
        path, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save image", "", "JPEG Image (*.jpg);;PNG Image (*.png)")
        if path:
            save_image_cv(self.cropped_img, path)
            QtWidgets.QMessageBox.information(self, "Saved", f"Image saved to {path}")

    def export_pdf(self):
        if not self.pages and (self.cropped_img is None and self.cv_img is None):
            QtWidgets.QMessageBox.information(self, "No Pages", "Add pages or scan an image first.")
            return
        path, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Export PDF", "", "PDF File (*.pdf)")
        if path:
            if self.pages:
                save_pdf_with_text(self.pages, path)
            else:
                pil = Image.fromarray(cv2.cvtColor(self.cropped_img if self.cropped_img is not None else self.cv_img, cv2.COLOR_BGR2RGB))
                save_pdf_with_text([(pil, self.ocr_text.toPlainText())], path)
            QtWidgets.QMessageBox.information(self, "Exported", f"PDF saved to {path}")

    def show_image(self, cv_img):
        rgb = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb.shape
        bytes_per_line = ch * w
        qimg = QtGui.QImage(rgb.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        pix = QtGui.QPixmap.fromImage(qimg)
        pix = pix.scaled(self.image_label.width(), self.image_label.height(), QtCore.Qt.KeepAspectRatio)
        self.image_label.setPixmap(pix)

def main():
    app = QtWidgets.QApplication(sys.argv)
    win = ScannerApp()
    win.show()

    sample_path = os.path.join(ASSETS_DIR, "sample.jpg")
    if os.path.exists(sample_path):
        win.cv_img = load_image_cv(sample_path)
        if win.cv_img is not None:
            win.image_path = sample_path
            win.show_image(win.cv_img)

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
