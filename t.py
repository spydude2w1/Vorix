import pytesseract
import os

tesseract_path = os.path.join(os.getcwd(), "tesseract", "tesseract.exe")
pytesseract.pytesseract.tesseract_cmd = tesseract_path

print(pytesseract.get_tesseract_version())  # Should print the Tesseract version
