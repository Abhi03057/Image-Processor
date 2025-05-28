import os
from flask import Flask, render_template, request, jsonify, send_file
from werkzeug.utils import secure_filename
import logging
from utils.image_processor import ImageProcessor
from utils.text_processor import TextProcessor
from utils.ai_processor import AIProcessor

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.secret_key = os.urandom(24)

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize processors
image_processor = ImageProcessor()
text_processor = TextProcessor()
ai_processor = AIProcessor()

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            return jsonify({
                'success': True,
                'filename': filename,
                'filepath': f'/static/uploads/{filename}'
            })
        
        return jsonify({'error': 'Invalid file type'}), 400
    
    except Exception as e:
        logger.error(f"Error in upload: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/process', methods=['POST'])
def process_image():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data received'}), 400

        filename = data.get('filename')
        action = data.get('action')
        params = data.get('params', {})

        if not filename or not action:
            return jsonify({'error': 'Missing filename or action'}), 400

        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        # Process based on action type
        if action in ['grayscale', 'sepia', 'warm', 'sharp', 'blur', 'edge']:
            result = image_processor.apply_filter(filepath, action, params)
        elif action in ['rotate', 'flip', 'crop', 'resize']:
            result = image_processor.transform_image(filepath, action, params)
        elif action == 'ocr':
            result = text_processor.extract_text(filepath, params.get('lang', 'eng'))
        elif action == 'tts':
            result = text_processor.text_to_speech(params.get('text'), params.get('lang', 'en'))
        elif action == 'translate':
            result = text_processor.translate_text(params.get('text'), params.get('target_lang', 'en'))
        elif action in ['face_detect', 'face_blur', 'remove_bg', 'caption']:
            result = ai_processor.process_image(filepath, action, params)
        else:
            return jsonify({'error': 'Invalid action'}), 400

        return jsonify(result)

    except Exception as e:
        logger.error(f"Error in processing: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/export', methods=['POST'])
def export_results():
    try:
        data = request.get_json()
        export_type = data.get('type', 'pdf')
        content = data.get('content', {})
        
        if export_type == 'pdf':
            pdf_path = text_processor.export_to_pdf(content)
            return send_file(pdf_path, as_attachment=True)
        else:
            return jsonify({'error': 'Invalid export type'}), 400

    except Exception as e:
        logger.error(f"Error in export: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/undo', methods=['POST'])
def undo_action():
    try:
        data = request.get_json()
        filename = data.get('filename')
        
        if not filename:
            return jsonify({'error': 'No filename provided'}), 400
            
        result = image_processor.undo(filename)
        return jsonify(result)

    except Exception as e:
        logger.error(f"Error in undo: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/redo', methods=['POST'])
def redo_action():
    try:
        data = request.get_json()
        filename = data.get('filename')
        
        if not filename:
            return jsonify({'error': 'No filename provided'}), 400
            
        result = image_processor.redo(filename)
        return jsonify(result)

    except Exception as e:
        logger.error(f"Error in redo: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True) 