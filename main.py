# Python script to extract text from an image using Tesseract OCR.

# --- Installation (Run these commands in your terminal) ---
# 1. Install Pillow (a Python imaging library):
#    pip install Pillow
#
# 2. Install pytesseract (a Python wrapper for Tesseract):
#    pip install pytesseract
#
# 3. Install Google's Tesseract OCR Engine:
#    This is a separate application that pytesseract uses.
#
#    - On macOS (using Homebrew):
#      brew install tesseract
#
#    - On Ubuntu/Debian:
#      sudo apt update
#      sudo apt install tesseract-ocr
#
#    - On Windows:
#      Download and run the installer from the official Tesseract repository.
#      You can find it here: https://github.com/UB-Mannheim/tesseract/wiki
#      During installation, make a note of the path where Tesseract is installed
#      (e.g., C:\Program Files\Tesseract-OCR\tesseract.exe). You may need to
#      add this path to your script.

import os
from pathlib import Path



try:
    from PIL import Image
except ImportError:
    print("Pillow library not found. Please install it using: pip install Pillow")
    exit()

try:
    import pytesseract
    # C:\Program Files\Tesseract-OCR
    pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'
except ImportError:
    print(
        "pytesseract library not found. Please install it using: pip install pytesseract"
    )
    exit()


def extract_text_from_image(image_path):
    """
    Extracts text from an image file using Tesseract OCR.

    Args:
        image_path (str): The file path to the image.

    Returns:
        str: The extracted text from the image. Returns an error message
             if the file is not found or an OCR error occurs.
    """
    try:
        # On Windows, you might need to explicitly point to the Tesseract executable.
        # Uncomment the line below and update the path if you installed Tesseract
        # in a non-standard location.
        # pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

        # Open the image file using Pillow
        with Image.open(image_path) as img:
            # Use pytesseract to extract text. The 'lang' parameter can be changed
            # to support other languages (e.g., 'fra' for French, 'spa' for Spanish).
            # You might need to install the language packs for Tesseract separately.
            text = pytesseract.image_to_string(img, lang="eng")
            return text

    except FileNotFoundError:
        return f"Error: The file '{image_path}' was not found."
    except Exception as e:
        # This will catch other potential errors from pytesseract
        return f"An error occurred during OCR processing: {e}"


# --- Example Usage ---
if __name__ == "__main__":
    # Replace 'path/to/your/image.png' with the actual path to your image file.
    # Supported formats include PNG, JPEG, TIFF, BMP, etc.
    screenshot_folder = Path(r"C:\Users\huili\Pictures\Screenshots")
    images = [fp for fp in screenshot_folder.glob("*.png")]
    images.sort(key=os.path.getmtime)
    image_file = images[-1]
    # [print(i) for i in images]
    # image_file = 'path/to/your/image.png'

    # Check if the placeholder path has been changedC:\Users\huili\venv\Scripts\python.exe
    if image_file == 'path/to/your/image.png':
        print("="*50)
        print("Please update the 'image_file' variable with the path to your image.")
        print("="*50)
    else:
        # Call the function to extract text
        extracted_text = extract_text_from_image(image_file)

        # Print the results
        print("--- Extracted Text ---")
        if extracted_text and "Error:" not in extracted_text:
            print(extracted_text)
        else:
            print("No text could be extracted or an error occurred.")
            print(extracted_text) # Print the specific error message
        print("----------------------")
