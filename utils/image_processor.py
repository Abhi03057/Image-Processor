import cv2
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter
import os
from collections import deque

class ImageProcessor:
    def __init__(self):
        self.history = {}  # Dictionary to store undo/redo history for each image
        self.max_history = 10

    def _init_history(self, filename):
        """Initialize history for a new image."""
        if filename not in self.history:
            self.history[filename] = {
                'undo': deque(maxlen=self.max_history),
                'redo': deque(maxlen=self.max_history),
                'current': None
            }

    def _save_state(self, image, filename):
        """Save current state for undo/redo."""
        self._init_history(filename)
        if self.history[filename]['current'] is not None:
            self.history[filename]['undo'].append(self.history[filename]['current'])
        self.history[filename]['current'] = image.copy()
        self.history[filename]['redo'].clear()

    def apply_filter(self, filepath, filter_type, params=None):
        """Apply various filters to the image."""
        try:
            image = Image.open(filepath)
            filename = os.path.basename(filepath)
            
            if filter_type == 'grayscale':
                processed = image.convert('L')
            
            elif filter_type == 'sepia':
                # Convert to numpy array for sepia calculation
                img_array = np.array(image)
                sepia_matrix = np.array([
                    [0.393, 0.769, 0.189],
                    [0.349, 0.686, 0.168],
                    [0.272, 0.534, 0.131]
                ])
                sepia_img = cv2.transform(img_array, sepia_matrix)
                sepia_img = np.clip(sepia_img, 0, 255)
                processed = Image.fromarray(sepia_img.astype(np.uint8))
            
            elif filter_type == 'warm':
                img_array = np.array(image)
                img_array[:, :, 2] = np.clip(img_array[:, :, 2] * 1.2, 0, 255)  # Red
                img_array[:, :, 1] = np.clip(img_array[:, :, 1] * 1.1, 0, 255)  # Green
                processed = Image.fromarray(img_array)
            
            elif filter_type == 'sharp':
                enhancer = ImageEnhance.Sharpness(image)
                factor = params.get('factor', 1.5)
                processed = enhancer.enhance(factor)
            
            elif filter_type == 'blur':
                radius = params.get('radius', 2)
                processed = image.filter(ImageFilter.GaussianBlur(radius=radius))
            
            elif filter_type == 'edge':
                # Convert to numpy array for Canny edge detection
                img_array = np.array(image)
                gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
                edges = cv2.Canny(gray, 100, 200)
                processed = Image.fromarray(edges)
            
            else:
                return {'error': 'Invalid filter type'}

            # Save state for undo/redo
            self._save_state(processed, filename)
            
            # Save processed image
            output_path = os.path.join('static/uploads', f'processed_{filename}')
            processed.save(output_path)
            
            return {
                'success': True,
                'filepath': f'/static/uploads/processed_{filename}'
            }

        except Exception as e:
            return {'error': str(e)}

    def transform_image(self, filepath, transform_type, params):
        """Apply geometric transformations to the image."""
        try:
            image = Image.open(filepath)
            filename = os.path.basename(filepath)
            
            if transform_type == 'rotate':
                angle = params.get('angle', 90)
                processed = image.rotate(angle, expand=True)
            
            elif transform_type == 'flip':
                direction = params.get('direction', 'horizontal')
                if direction == 'horizontal':
                    processed = image.transpose(Image.FLIP_LEFT_RIGHT)
                else:
                    processed = image.transpose(Image.FLIP_TOP_BOTTOM)
            
            elif transform_type == 'crop':
                left = params.get('left', 0)
                top = params.get('top', 0)
                right = params.get('right', image.width)
                bottom = params.get('bottom', image.height)
                processed = image.crop((left, top, right, bottom))
            
            elif transform_type == 'resize':
                width = params.get('width', image.width)
                height = params.get('height', image.height)
                processed = image.resize((width, height), Image.Resampling.LANCZOS)
            
            else:
                return {'error': 'Invalid transform type'}

            # Save state for undo/redo
            self._save_state(processed, filename)
            
            # Save processed image
            output_path = os.path.join('static/uploads', f'processed_{filename}')
            processed.save(output_path)
            
            return {
                'success': True,
                'filepath': f'/static/uploads/processed_{filename}'
            }

        except Exception as e:
            return {'error': str(e)}

    def undo(self, filename):
        """Undo the last operation."""
        try:
            if filename not in self.history or not self.history[filename]['undo']:
                return {'error': 'No actions to undo'}

            # Move current state to redo stack
            self.history[filename]['redo'].append(self.history[filename]['current'])
            
            # Pop the last state from undo stack
            previous_state = self.history[filename]['undo'].pop()
            self.history[filename]['current'] = previous_state
            
            # Save the image
            output_path = os.path.join('static/uploads', f'processed_{filename}')
            previous_state.save(output_path)
            
            return {
                'success': True,
                'filepath': f'/static/uploads/processed_{filename}'
            }

        except Exception as e:
            return {'error': str(e)}

    def redo(self, filename):
        """Redo the last undone operation."""
        try:
            if filename not in self.history or not self.history[filename]['redo']:
                return {'error': 'No actions to redo'}

            # Move current state to undo stack
            self.history[filename]['undo'].append(self.history[filename]['current'])
            
            # Pop the last state from redo stack
            next_state = self.history[filename]['redo'].pop()
            self.history[filename]['current'] = next_state
            
            # Save the image
            output_path = os.path.join('static/uploads', f'processed_{filename}')
            next_state.save(output_path)
            
            return {
                'success': True,
                'filepath': f'/static/uploads/processed_{filename}'
            }

        except Exception as e:
            return {'error': str(e)} 