import cv2
import numpy as np
from PIL import Image
import torch
from rembg import remove
from transformers import pipeline
import os
import logging

logger = logging.getLogger(__name__)

class AIProcessor:
    def __init__(self):
        # Initialize face detection
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        
        # Initialize image captioning
        try:
            self.caption_generator = pipeline("image-to-text", model="Salesforce/blip-image-captioning-base")
        except Exception as e:
            logger.error(f"Error loading caption model: {str(e)}")
            self.caption_generator = None

    def process_image(self, filepath, action, params=None):
        """Process image with AI-based operations."""
        try:
            if action == 'face_detect':
                return self._detect_faces(filepath, blur=False)
            elif action == 'face_blur':
                return self._detect_faces(filepath, blur=True)
            elif action == 'remove_bg':
                return self._remove_background(filepath)
            elif action == 'caption':
                return self._generate_caption(filepath)
            else:
                return {'error': 'Invalid AI action'}
        except Exception as e:
            logger.error(f"Error in AI processing: {str(e)}")
            return {'error': str(e)}

    def _detect_faces(self, filepath, blur=False):
        """Detect faces in image and optionally blur them."""
        try:
            # Read image
            image = cv2.imread(filepath)
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # Detect faces
            faces = self.face_cascade.detectMultiScale(gray, 1.1, 4)
            
            if len(faces) == 0:
                return {
                    'success': True,
                    'message': 'No faces detected',
                    'faces': []
                }
            
            # Process faces
            face_data = []
            for (x, y, w, h) in faces:
                if blur:
                    # Apply blur to face region
                    face_roi = image[y:y+h, x:x+w]
                    blurred_face = cv2.GaussianBlur(face_roi, (99, 99), 30)
                    image[y:y+h, x:x+w] = blurred_face
                else:
                    # Draw rectangle around face
                    cv2.rectangle(image, (x, y), (x+w, y+h), (255, 0, 0), 2)
                
                face_data.append({
                    'x': int(x),
                    'y': int(y),
                    'width': int(w),
                    'height': int(h)
                })
            
            # Save processed image
            filename = os.path.basename(filepath)
            output_path = os.path.join('static/uploads', f'processed_{filename}')
            cv2.imwrite(output_path, image)
            
            return {
                'success': True,
                'filepath': f'/static/uploads/processed_{filename}',
                'faces': face_data
            }
        
        except Exception as e:
            logger.error(f"Error in face detection: {str(e)}")
            return {'error': str(e)}

    def _remove_background(self, filepath):
        """Remove background from image."""
        try:
            # Read image
            input_image = Image.open(filepath)
            
            # Remove background
            output_image = remove(input_image)
            
            # Save processed image
            filename = os.path.basename(filepath)
            output_path = os.path.join('static/uploads', f'processed_{filename}')
            output_image.save(output_path, 'PNG')
            
            return {
                'success': True,
                'filepath': f'/static/uploads/processed_{filename}'
            }
        
        except Exception as e:
            logger.error(f"Error in background removal: {str(e)}")
            return {'error': str(e)}

    def _generate_caption(self, filepath):
        """Generate caption for image."""
        try:
            if not self.caption_generator:
                return {'error': 'Caption generator not initialized'}
            
            # Generate caption
            result = self.caption_generator(filepath)
            caption = result[0]['generated_text'] if result else "Could not generate caption"
            
            return {
                'success': True,
                'caption': caption
            }
        
        except Exception as e:
            logger.error(f"Error in caption generation: {str(e)}")
            return {'error': str(e)} 