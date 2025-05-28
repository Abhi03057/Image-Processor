import cv2
import numpy as np
from PIL import Image, ImageEnhance
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class ImageProcessor:
    @staticmethod
    def convert_to_grayscale(image):
        """Convert image to grayscale.
        
        Args:
            image (PIL.Image): Input image
            
        Returns:
            PIL.Image: Grayscale image
        """
        try:
            logger.debug(f"Converting image to grayscale. Input image mode: {image.mode}")
            if image.mode != 'RGB':
                image = image.convert('RGB')
            gray_image = image.convert('L')
            logger.debug("Grayscale conversion successful")
            return gray_image
        except Exception as e:
            logger.error(f"Error in grayscale conversion: {str(e)}")
            raise

    @staticmethod
    def add_warm_tone(image):
        """Add warm color tones to the image.
        
        Args:
            image (PIL.Image): Input image
            
        Returns:
            PIL.Image: Warm-toned image
        """
        try:
            logger.debug(f"Adding warm tone. Input image mode: {image.mode}")
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Convert to numpy array
            img_array = np.array(image)
            
            # Increase red and yellow tones
            img_array[:, :, 2] = np.clip(img_array[:, :, 2] * 1.2, 0, 255)  # Red channel
            img_array[:, :, 1] = np.clip(img_array[:, :, 1] * 1.1, 0, 255)  # Green channel
            
            result = Image.fromarray(img_array.astype('uint8'), 'RGB')
            logger.debug("Warm tone addition successful")
            return result
        except Exception as e:
            logger.error(f"Error in adding warm tone: {str(e)}")
            raise

    @staticmethod
    def enhance_sharpness(image, factor=1.5):
        """Enhance image sharpness.
        
        Args:
            image (PIL.Image): Input image
            factor (float): Sharpness enhancement factor
            
        Returns:
            PIL.Image: Sharpened image
        """
        try:
            logger.debug(f"Enhancing sharpness. Input image mode: {image.mode}")
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            enhancer = ImageEnhance.Sharpness(image)
            sharpened = enhancer.enhance(factor)
            logger.debug("Sharpness enhancement successful")
            return sharpened
        except Exception as e:
            logger.error(f"Error in enhancing sharpness: {str(e)}")
            raise

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