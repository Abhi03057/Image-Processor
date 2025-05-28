import pytesseract
from PIL import Image
import pyttsx3
from googletrans import Translator
from fpdf import FPDF
import os
import logging

logger = logging.getLogger(__name__)

class TextProcessor:
    def __init__(self):
        self.translator = Translator()
        self.engine = pyttsx3.init()

    def extract_text(self, filepath, lang='eng'):
        """Extract text from image using OCR."""
        try:
            image = Image.open(filepath)
            text = pytesseract.image_to_string(image, lang=lang)
            return {
                'success': True,
                'text': text.strip()
            }
        except Exception as e:
            logger.error(f"Error in OCR: {str(e)}")
            return {'error': str(e)}

    def text_to_speech(self, text, lang='en'):
        """Convert text to speech."""
        try:
            if not text:
                return {'error': 'No text provided'}

            # Set language
            self.engine.setProperty('voice', lang)
            
            # Generate audio file
            output_path = os.path.join('static/uploads', 'output.mp3')
            self.engine.save_to_file(text, output_path)
            self.engine.runAndWait()
            
            return {
                'success': True,
                'filepath': '/static/uploads/output.mp3'
            }
        except Exception as e:
            logger.error(f"Error in TTS: {str(e)}")
            return {'error': str(e)}

    def translate_text(self, text, target_lang='en'):
        """Translate text to target language."""
        try:
            if not text:
                return {'error': 'No text provided'}

            translation = self.translator.translate(text, dest=target_lang)
            return {
                'success': True,
                'translated_text': translation.text,
                'source_lang': translation.src,
                'target_lang': translation.dest
            }
        except Exception as e:
            logger.error(f"Error in translation: {str(e)}")
            return {'error': str(e)}

    def export_to_pdf(self, content):
        """Export images and text to PDF."""
        try:
            pdf = FPDF()
            pdf.add_page()
            
            # Add title
            pdf.set_font('Arial', 'B', 16)
            pdf.cell(0, 10, 'Image Processing Results', 0, 1, 'C')
            
            # Add images
            if 'images' in content:
                for img_path in content['images']:
                    pdf.image(img_path, x=10, y=None, w=190)
                    pdf.ln(10)
            
            # Add text
            if 'text' in content:
                pdf.set_font('Arial', '', 12)
                pdf.multi_cell(0, 10, content['text'])
            
            # Save PDF
            output_path = os.path.join('static/uploads', 'output.pdf')
            pdf.output(output_path)
            
            return output_path
        except Exception as e:
            logger.error(f"Error in PDF export: {str(e)}")
            raise 