# image-to-text

Simple python image to text processor using tesseract-ocr

## Installation instructions

1. Install Pillow (a Python imaging library):
   pip install Pillow

2. Install pytesseract (a Python wrapper for Tesseract):
   pip install pytesseract

3. Install Google's Tesseract OCR Engine:
   This is a separate application that pytesseract uses.

   - On macOS (using Homebrew):
     brew install tesseract

   - On Ubuntu/Debian:
     sudo apt update
     sudo apt install tesseract-ocr

   - On Windows:
     Download and run the installer from the official Tesseract repository.
     You can find it here: https://github.com/UB-Mannheim/tesseract/wiki
     During installation, make a note of the path where Tesseract is installed
     (e.g., C:\Program Files\Tesseract-OCR\tesseract.exe). You may need to
     add this path to your script.


## WinOS nuances

1. Windows Security - Protection History - Protected folder access blocked.
   This could have prevented you from modifying powershell profiles `$profile`
1. Windows Security: Smart App Control
   - `uv` is now blocked
   - Solution is to install python officially from python.org
   - Use pipx to install uv
   - Use `$env:UV_PYTHON_PREFERENCE = "only-system"` (you can set in `$profile`)
     to tell uv to only use the system python
