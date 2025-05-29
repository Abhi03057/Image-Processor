from PIL import ImageEnhance

class ImageProcessor:
    def convert_to_grayscale(self, image):
        """Convert image to grayscale."""
        return image.convert('L')

    def add_warm_tone(self, image):
        """Add a warm tone to the image."""
        r, g, b = image.split()
        r = r.point(lambda i: min(255, i + 30))  # Boost red
        b = b.point(lambda i: max(0, i - 30))    # Reduce blue
        return image.merge('RGB', (r, g, b))

    def enhance_sharpness(self, image):
        """Enhance sharpness of the image."""
        enhancer = ImageEnhance.Sharpness(image)
        return enhancer.enhance(2.0)
