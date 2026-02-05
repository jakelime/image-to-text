import argparse
import sys
from datetime import datetime
from pathlib import Path

import pytesseract
from PIL import Image


def get_args():
    """
    Parses command-line arguments.
    """
    parser = argparse.ArgumentParser(
        description="Batch extract text from images to a timestamped text file."
    )

    # Positional argument: The Input Directory
    parser.add_argument(
        "input_dir",
        type=Path,
        help="Path to the folder containing images."
    )

    # Optional argument: Output Directory (defaults to input dir if not set)
    parser.add_argument(
        "-o", "--output-dir",
        type=Path,
        default=None,
        help="Directory to save the output file (default: same as input directory)."
    )

    # Optional argument: Language
    parser.add_argument(
        "--lang",
        type=str,
        default="eng",
        help="Tesseract language code (default: 'eng')."
    )

    return parser.parse_args()


def extract_text_from_image(image_path, lang="eng"):
    """
    Extracts text from an image file using Tesseract OCR.
    Returns None if an error occurs, printing the error to stderr.
    """
    try:
        with Image.open(image_path) as img:
            text = pytesseract.image_to_string(img, lang=lang)
            return text.strip()
    except Exception as e:
        # Print error to standard error stream so it doesn't clutter standard output
        print(f"[!] Error processing {image_path.name}: {e}", file=sys.stderr)
        return None


def main():
    args = get_args()

    # 1. Validate Input Directory
    if not args.input_dir.exists() or not args.input_dir.is_dir():
        print(f"Error: The input directory '{args.input_dir}' does not exist or is not a folder.")
        sys.exit(1)

    # 2. Configure Output Path
    # If no output dir is specified, save to the input dir
    output_dir = args.output_dir if args.output_dir else args.input_dir

    # Create output dir if it doesn't exist
    output_dir.mkdir(parents=True, exist_ok=True)

    # Generate timestamped filename
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    output_file = output_dir / f"output.{timestamp}.txt"

    # 3. Gather Image Files
    # We use a set of extensions and check case-insensitively
    valid_extensions = {".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".tif"}

    # List comprehension to find all matching files
    filepaths = [
        p for p in args.input_dir.iterdir()
        if p.is_file() and p.suffix.lower() in valid_extensions
    ]

    # Sort by modification time (oldest to newest)
    filepaths.sort(key=lambda x: x.stat().st_mtime)

    if not filepaths:
        print(f"No images found in '{args.input_dir}'.")
        sys.exit(0)

    print(f"Found {len(filepaths)} images. Processing...")
    print(f"Writing results to: {output_file}")

    # 4. Process and Write to File
    # We open the file once and append text as we loop
    with open(output_file, "w", encoding="utf-8") as f:
        # Write a header
        f.write(f"OCR Extraction Report\n")
        f.write(f"Source: {args.input_dir}\n")
        f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 40 + "\n\n")

        for fp in filepaths:
            print(f"-> Processing: {fp.name}")
            extracted_text = extract_text_from_image(fp, args.lang)

            f.write(f"--- SOURCE FILE: {fp.name} ---\n")
            if extracted_text:
                f.write(extracted_text)
            else:
                f.write("[ERROR: Could not extract text]")

            f.write("\n\n" + ("-" * 40) + "\n\n")

    print("Done.")


if __name__ == "__main__":
    main()