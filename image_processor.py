import cv2
import numpy as np
from PIL import Image, ImageEnhance

class ImageProcessor:
    @staticmethod
    def convert_to_grayscale(image):
        """Convert image to grayscale.
        
        Args:
            image (PIL.Image): Input image
            
        Returns:
            PIL.Image: Grayscale image
        """
        return image.convert('L')

    @staticmethod
    def add_warm_tone(image):
        """Add warm color tones to the image.
        
        Args:
            image (PIL.Image): Input image
            
        Returns:
            PIL.Image: Warm-toned image
        """
        # Convert to numpy array
        img_array = np.array(image)
        
        # Increase red and yellow tones
        img_array[:, :, 2] = np.clip(img_array[:, :, 2] * 1.2, 0, 255)  # Red channel
        img_array[:, :, 1] = np.clip(img_array[:, :, 1] * 1.1, 0, 255)  # Green channel
        
        return Image.fromarray(img_array)

    @staticmethod
    def enhance_sharpness(image, factor=1.5):
        """Enhance image sharpness.
        
        Args:
            image (PIL.Image): Input image
            factor (float): Sharpness enhancement factor
            
        Returns:
            PIL.Image: Sharpened image
        """
        enhancer = ImageEnhance.Sharpness(image)
        return enhancer.enhance(factor)

    @staticmethod
    def pil_to_cv2(pil_image):
        """Convert PIL image to CV2 format.
        
        Args:
            pil_image (PIL.Image): Input PIL image
            
        Returns:
            numpy.ndarray: OpenCV format image
        """
        return cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)

    @staticmethod
    def cv2_to_pil(cv2_image):
        """Convert CV2 image to PIL format.
        
        Args:
            cv2_image (numpy.ndarray): Input OpenCV image
            
        Returns:
            PIL.Image: PIL format image
        """
        return Image.fromarray(cv2.cvtColor(cv2_image, cv2.COLOR_BGR2RGB)) 