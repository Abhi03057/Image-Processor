# Image Processing Application

A Python-based image processing application that allows users to apply various filters to images and extract text using OCR.

## Features

- Image filtering:
  - Grayscale conversion
  - Warm tone adjustment
  - Sharpness enhancement
- OCR (Optical Character Recognition) for text extraction
- User-friendly GUI interface

## Requirements

- Python 3.x
- OpenCV
- Pillow (PIL)
- pytesseract
- numpy

## Installation

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Install Tesseract OCR:
   - Windows: Download and install from https://github.com/UB-Mannheim/tesseract/wiki
   - Make sure to add Tesseract to your system PATH

## Usage

Run the application:
```bash
python main.py
```

## How to Use

1. Click "Open Image" to select an image file
2. Use the buttons to apply different filters:
   - Convert to Grayscale
   - Add Warm Tone
   - Enhance Sharpness
3. Use "Extract Text" to perform OCR on the image
4. Click "Save Image" to save the processed image 