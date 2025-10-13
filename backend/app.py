"""
Electrical Component Classification - Flask Web Application
Professional-grade web application for electrical component classification.
"""

import os
import logging
from datetime import datetime
from flask import Flask, request, jsonify, render_template, redirect, url_for, flash
from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge
import uuid

from dep import create_predictor

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'electrical-component-classifier-2025'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Configuration
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'static', 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff', 'webp'}

# Ensure upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Initialize predictor (lazy loading)
predictor = None

def get_predictor():
    """Get or create predictor instance (singleton pattern)."""
    global predictor
    if predictor is None:
        try:
            predictor = create_predictor()
            logger.info("Predictor initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize predictor: {str(e)}")
            raise
    return predictor

def allowed_file(filename):
    """Check if file extension is allowed."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def cleanup_old_files():
    """Clean up files older than 1 hour to manage storage."""
    try:
        current_time = datetime.now().timestamp()
        for filename in os.listdir(UPLOAD_FOLDER):
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            if os.path.isfile(file_path):
                file_age = current_time - os.path.getmtime(file_path)
                if file_age > 3600:  # 1 hour
                    os.remove(file_path)
                    logger.info(f"Cleaned up old file: {filename}")
    except Exception as e:
        logger.warning(f"Error during cleanup: {str(e)}")

@app.route('/')
def index():
    """Serve the main application page."""
    try:
        # Get class information for display
        predictor = get_predictor()
        class_info = predictor.get_class_info()
        
        return render_template('index.html', 
                             num_classes=class_info['num_classes'],
                             classes=class_info['classes'])
    except Exception as e:
        logger.error(f"Error serving index page: {str(e)}")
        return render_template('index.html', 
                             num_classes=0,
                             classes=[],
                             error="Service temporarily unavailable")

@app.route('/documentation')
def documentation():
    """Serve the documentation page."""
    return render_template('documentation.html')

@app.route('/about')
def about():
    """Serve the about designer page."""
    return render_template('about.html')

@app.route('/predict', methods=['POST'])
def predict():
    """
    Handle image upload and prediction.
    
    Returns:
        JSON response with prediction results
    """
    try:
        # Check if file was uploaded
        if 'file' not in request.files:
            return jsonify({
                'success': False,
                'error': 'No file uploaded'
            }), 400
        
        file = request.files['file']
        
        # Check if file was selected
        if file.filename == '':
            return jsonify({
                'success': False,
                'error': 'No file selected'
            }), 400
        
        # Validate file
        if not allowed_file(file.filename):
            return jsonify({
                'success': False,
                'error': f'Invalid file type. Allowed types: {", ".join(ALLOWED_EXTENSIONS)}'
            }), 400
        
        # Generate unique filename
        file_extension = file.filename.rsplit('.', 1)[1].lower()
        unique_filename = f"{uuid.uuid4()}.{file_extension}"
        file_path = os.path.join(UPLOAD_FOLDER, unique_filename)
        
        # Save file
        file.save(file_path)
        logger.info(f"File saved: {unique_filename}")
        
        # Clean up old files
        cleanup_old_files()
        
        # Make prediction
        predictor = get_predictor()
        result = predictor.predict(file_path)
        
        # Add file info to result
        result['filename'] = unique_filename
        result['original_filename'] = secure_filename(file.filename)
        
        # Clean up uploaded file after prediction
        try:
            os.remove(file_path)
            logger.info(f"Cleaned up uploaded file: {unique_filename}")
        except Exception as e:
            logger.warning(f"Failed to clean up file {unique_filename}: {str(e)}")
        
        return jsonify(result)
        
    except RequestEntityTooLarge:
        return jsonify({
            'success': False,
            'error': 'File too large. Maximum size is 16MB.'
        }), 413
    
    except Exception as e:
        logger.error(f"Error in predict endpoint: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Internal server error. Please try again.'
        }), 500

@app.route('/health')
def health():
    """Health check endpoint."""
    try:
        predictor = get_predictor()
        class_info = predictor.get_class_info()
        
        return jsonify({
            'status': 'healthy',
            'model_loaded': True,
            'num_classes': class_info['num_classes'],
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return jsonify({
            'status': 'unhealthy',
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

@app.route('/classes')
def get_classes():
    """Get available classes information."""
    try:
        predictor = get_predictor()
        class_info = predictor.get_class_info()
        
        return jsonify({
            'success': True,
            'num_classes': class_info['num_classes'],
            'classes': class_info['classes'],
            'class_mapping': class_info['class_mapping']
        })
    except Exception as e:
        logger.error(f"Error getting classes: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.errorhandler(413)
def too_large(e):
    """Handle file too large error."""
    return jsonify({
        'success': False,
        'error': 'File too large. Maximum size is 16MB.'
    }), 413

@app.errorhandler(404)
def not_found(e):
    """Handle 404 errors."""
    return jsonify({
        'success': False,
        'error': 'Endpoint not found'
    }), 404

@app.errorhandler(500)
def internal_error(e):
    """Handle internal server errors."""
    logger.error(f"Internal server error: {str(e)}")
    return jsonify({
        'success': False,
        'error': 'Internal server error'
    }), 500

if __name__ == '__main__':
    # Development server configuration
    logger.info("Starting Electrical Component Classification App")
    logger.info(f"Upload folder: {UPLOAD_FOLDER}")
    logger.info(f"Allowed extensions: {ALLOWED_EXTENSIONS}")
    
    # Test predictor initialization
    try:
        predictor = get_predictor()
        class_info = predictor.get_class_info()
        logger.info(f"Model loaded with {class_info['num_classes']} classes")
    except Exception as e:
        logger.error(f"Failed to initialize predictor: {str(e)}")
        logger.error("Please ensure model files are in the correct location")
    
    # Run the application
    app.run(
        host='127.0.0.1',
        port=5000,
        debug=False,
        threaded=True
    )
