import os
from flask import Flask, render_template, request, jsonify, send_file
from PIL import Image
import io
import base64
from image_processor import ImageProcessor
from ocr_handler import OCRHandler

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

image_processor = ImageProcessor()
ocr_handler = OCRHandler()

def save_image(image_data):
    """Save the image data and return the filename"""
    if not image_data:
        return None
    
    # Remove header of base64 string if present
    if 'base64,' in image_data:
        image_data = image_data.split('base64,')[1]
    
    image_bytes = base64.b64decode(image_data)
    image = Image.open(io.BytesIO(image_bytes))
    
    # Generate unique filename
    filename = f"image_{os.urandom(8).hex()}.png"
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    
    image.save(filepath)
    return filename

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_image', methods=['POST'])
def process_image():
    try:
        data = request.get_json()
        image_data = data.get('image')
        action = data.get('action')
        
        if not image_data or not action:
            return jsonify({'error': 'Missing image data or action'}), 400

        # Save the uploaded image
        filename = save_image(image_data)
        if not filename:
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
            return jsonify({'error': 'Invalid action'}), 400

        # Save and return the processed image
        output_buffer = io.BytesIO()
        processed_image.save(output_buffer, format='PNG')
        processed_image_data = base64.b64encode(output_buffer.getvalue()).decode()

        return jsonify({
            'processed_image': f'data:image/png;base64,{processed_image_data}',
            'original_image': f'/static/uploads/{filename}'
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True) 