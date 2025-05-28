import os
from flask import Flask, render_template, request, jsonify, send_file
from PIL import Image
import io
import base64
import logging
from image_processor import ImageProcessor
from ocr_handler import OCRHandler

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

image_processor = ImageProcessor()
ocr_handler = OCRHandler()

def save_image(image_data):
    """Save the image data and return the filename"""
    try:
        if not image_data:
            logger.error("No image data provided")
            return None
        
        # Remove header of base64 string if present
        if 'base64,' in image_data:
            image_data = image_data.split('base64,')[1]
        
        image_bytes = base64.b64decode(image_data)
        image = Image.open(io.BytesIO(image_bytes))
        
        # Generate unique filename
        filename = f"image_{os.urandom(8).hex()}.png"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        # Ensure image is in RGB mode before saving
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        image.save(filepath)
        logger.debug(f"Image saved successfully as {filename}")
        return filename
    except Exception as e:
        logger.error(f"Error saving image: {str(e)}")
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_image', methods=['POST'])
def process_image():
    try:
        data = request.get_json()
        if not data:
            logger.error("No JSON data received")
            return jsonify({'error': 'No data received'}), 400

        image_data = data.get('image')
        action = data.get('action')
        
        logger.debug(f"Processing image with action: {action}")
        
        if not image_data or not action:
            logger.error("Missing image data or action")
            return jsonify({'error': 'Missing image data or action'}), 400

        # Save the uploaded image
        filename = save_image(image_data)
        if not filename:
            logger.error("Failed to save image")
            return jsonify({'error': 'Failed to save image'}), 400

        image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        image = Image.open(image_path)

        # Process the image based on the action
        if action == 'grayscale':
            processed_image = image_processor.convert_to_grayscale(image)
        elif action == 'warm':
            processed_image = image_processor.add_warm_tone(image)
        elif action == 'sharp':
            processed_image = image_processor.enhance_sharpness(image)
        elif action == 'ocr':
            text = ocr_handler.extract_text(image)
            return jsonify({'text': text})
        else:
            logger.error(f"Invalid action: {action}")
            return jsonify({'error': 'Invalid action'}), 400

        # Save and return the processed image
        output_buffer = io.BytesIO()
        processed_image.save(output_buffer, format='PNG')
        processed_image_data = base64.b64encode(output_buffer.getvalue()).decode()

        response_data = {
            'processed_image': f'data:image/png;base64,{processed_image_data}',
            'original_image': f'/static/uploads/{filename}'
        }
        logger.debug("Image processing completed successfully")
        return jsonify(response_data)

    except Exception as e:
        logger.error(f"Error processing image: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True) 