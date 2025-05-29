import pytesseract
from PIL import Image
import cv2
import numpy as np

class OCRHandler:
    def __init__(self):
        """Initialize OCR Handler."""
        # Uncomment this line for Windows and set your Tesseract path:
        # Make sure the path is correct and tesseract is installed there.
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

    def preprocess_image(self, image):
        """Preprocess image for better OCR results."""
        # Convert PIL image to numpy array
        img_array = np.array(image)

        # Convert to grayscale
        gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)

        # Apply thresholding (Otsu's method)
        gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

        # Apply median blur to reduce noise
        gray = cv2.medianBlur(gray, 3)

        # Convert back to PIL Image and return
        return Image.fromarray(gray)

    def extract_text(self, image):
        """Extract text from image using OCR."""
        processed_image = self.preprocess_image(image)
        try:
            text = pytesseract.image_to_string(processed_image)
            return text.strip()
        except Exception as e:
            return f"Error in text extraction: {str(e)}"
