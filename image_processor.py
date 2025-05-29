# image_processor.py

from PIL import Image, ImageEnhance, ImageFilter, ImageOps
import cv2
import numpy as np

class ImageProcessor:
    def convert_to_grayscale(self, image):
        return ImageOps.grayscale(image)

    def add_warm_tone(self, image):
        # Simple warm filter using ImageEnhance.Color
        enhancer = ImageEnhance.Color(image)
        image = enhancer.enhance(1.5)
        r, g, b = image.split()
        r = r.point(lambda i: i * 1.1)
        g = g.point(lambda i: i * 1.05)
        return Image.merge('RGB', (r, g, b))

    def enhance_sharpness(self, image):
        enhancer = ImageEnhance.Sharpness(image)
        return enhancer.enhance(2.0)

    def apply_gaussian_blur(self, image, radius=2):
        return image.filter(ImageFilter.GaussianBlur(radius))

    def apply_median_blur(self, image, radius=3):
        # Convert PIL Image to OpenCV format
        img_array = np.array(image)
        img_array = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
        blurred = cv2.medianBlur(img_array, radius)
        blurred = cv2.cvtColor(blurred, cv2.COLOR_BGR2RGB)
        return Image.fromarray(blurred)

    def apply_sepia(self, image):
        width, height = image.size
        pixels = image.load()  # create the pixel map

        for py in range(height):
            for px in range(width):
                r, g, b = image.getpixel((px, py))

                tr = int(0.393 * r + 0.769 * g + 0.189 * b)
                tg = int(0.349 * r + 0.686 * g + 0.168 * b)
                tb = int(0.272 * r + 0.534 * g + 0.131 * b)

                tr = min(255, tr)
                tg = min(255, tg)
                tb = min(255, tb)

                pixels[px, py] = (tr, tg, tb)

        return image

    def adjust_brightness_contrast(self, image, brightness=1.0, contrast=1.0):
        enhancer_b = ImageEnhance.Brightness(image)
        image = enhancer_b.enhance(brightness)
        enhancer_c = ImageEnhance.Contrast(image)
        image = enhancer_c.enhance(contrast)
        return image

    def rotate_image(self, image, angle):
        return image.rotate(angle, expand=True)

    def flip_horizontal(self, image):
        return ImageOps.mirror(image)

    def flip_vertical(self, image):
        return ImageOps.flip(image)

    def edge_detection(self, image):
        # Convert to grayscale then detect edges using Canny
        img_array = np.array(image.convert('L'))
        edges = cv2.Canny(img_array, 100, 200)
        return Image.fromarray(edges)

    def crop_image(self, image, left, upper, right, lower):
        return image.crop((left, upper, right, lower))

    def resize_image(self, image, new_width, new_height):
        return image.resize((new_width, new_height))
