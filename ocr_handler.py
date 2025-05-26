import pytesseract
from PIL import Image
import cv2
import numpy as np

class OCRHandler:
    def __init__(self):
        """Initialize OCR Handler."""
        # For Windows, you might need to set the tesseract path
        # pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        pass

    def preprocess_image(self, image):
        """Preprocess image for better OCR results.
        
        Args:
            image (PIL.Image): Input image
            
        Returns:
            PIL.Image: Preprocessed image
        """
        # Convert to numpy array
        img_array = np.array(image)
        
        # Convert to grayscale
        gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
        
        # Apply thresholding to preprocess the image
        gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
        
        # Apply median blur to remove noise
        gray = cv2.medianBlur(gray, 3)
        
        return Image.fromarray(gray)

    def extract_text(self, image):
        """Extract text from image using OCR.
        
        Args:
            image (PIL.Image): Input image
            
        Returns:
            str: Extracted text
        """
        # Preprocess the image
        processed_image = self.preprocess_image(image)
        
        # Extract text using pytesseract
        try:
            text = pytesseract.image_to_string(processed_image)
            return text.strip()
        except Exception as e:
            return f"Error in text extraction: {str(e)}" 