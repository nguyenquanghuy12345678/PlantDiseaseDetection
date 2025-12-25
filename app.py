from flask import Flask, render_template, request, jsonify, session
from werkzeug.utils import secure_filename
import os
import json
import uuid
import base64
from datetime import datetime
from config import Config
from utils import model_handler
from utils.preprocessing import preprocess_image, validate_image
from utils.treatment_data import get_treatment_info

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)
Config.init_app(app)

# Model handler available as module functions
# No class initialization needed

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


@app.route('/')
def index():
    """Render homepage"""
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    """
    Handle image prediction from file upload or webcam
    Returns JSON with prediction results
    """
    try:
        image_path = None
        temp_file = None
        
        # Handle file upload
        if 'file' in request.files:
            file = request.files['file']
            
            if file.filename == '':
                return jsonify({'error': 'No file selected'}), 400
            
            if not allowed_file(file.filename):
                return jsonify({'error': 'Invalid file type. Only PNG, JPG, JPEG allowed'}), 400
            
            # Save file with unique name
            filename = secure_filename(file.filename)
            unique_filename = f"{uuid.uuid4().hex}_{filename}"
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
            file.save(image_path)
            temp_file = image_path
            
        # Handle webcam base64 data
        elif request.is_json and 'image' in request.json:
            image_data = request.json['image']
            
            # Remove data URL prefix if present
            if 'base64,' in image_data:
                image_data = image_data.split('base64,')[1]
            
            # Decode and save
            image_bytes = base64.b64decode(image_data)
            unique_filename = f"{uuid.uuid4().hex}_webcam.jpg"
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
            
            with open(image_path, 'wb') as f:
                f.write(image_bytes)
            temp_file = image_path
            
        else:
            return jsonify({'error': 'No image data provided'}), 400
        
        # Validate image
        if not validate_image(image_path):
            if temp_file and os.path.exists(temp_file):
                os.remove(temp_file)
            return jsonify({'error': 'Invalid image file'}), 400
        
        # Get predictions using smart inference
        predictions = model_handler.get_predictions(image_path, top_k=3)
        
        # Get treatment info for top prediction
        top_class = predictions[0]['class']
        treatment = get_treatment_info(top_class)
        
        # Build response
        result = {
            'success': True,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'top_prediction': predictions[0],
            'all_predictions': predictions,
            'treatment': treatment,
            'image_url': f'/static/uploads/{os.path.basename(image_path)}'
        }
        
        # Add to session history
        if 'history' not in session:
            session['history'] = []
        
        history_entry = {
            'timestamp': result['timestamp'],
            'disease': predictions[0]['class'],
            'confidence': predictions[0]['confidence'],
            'image_url': result['image_url']
        }
        
        session['history'].insert(0, history_entry)
        session['history'] = session['history'][:10]  # Keep only last 10
        session.modified = True
        
        return jsonify(result)
        
    except Exception as e:
        # Clean up temp file on error
        if temp_file and os.path.exists(temp_file):
            os.remove(temp_file)
        
        return jsonify({'error': f'Prediction failed: {str(e)}'}), 500


@app.route('/history', methods=['GET'])
def get_history():
    """Get prediction history from session"""
    history = session.get('history', [])
    return jsonify({'history': history})


@app.route('/clear-history', methods=['POST'])
def clear_history():
    """Clear prediction history"""
    session['history'] = []
    session.modified = True
    return jsonify({'success': True})


@app.errorhandler(413)
def request_entity_too_large(error):
    """Handle file too large error"""
    return jsonify({'error': 'File too large. Maximum size is 16MB'}), 413


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return render_template('index.html'), 404


if __name__ == '__main__':
    print("=" * 60)
    print("🌱 Plant Disease Detection App")
    print("=" * 60)
    print(f"📍 Running on: http://localhost:5000")
    print(f"📁 Upload folder: {app.config['UPLOAD_FOLDER']}")
    print(f"🤖 Model path: {app.config['MODEL_PATH']}")
    print("=" * 60)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
