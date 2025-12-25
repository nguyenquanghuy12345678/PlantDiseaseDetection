import os

class Config:
    """Configuration for Flask app"""
    
    # Flask config
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Upload config
    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'static', 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
    
    # Model config
    MODEL_PATH = os.path.join(os.path.dirname(__file__), 'models', 'disease_model.h5')
    CLASS_INDICES_PATH = os.path.join(os.path.dirname(__file__), 'models', 'class_indices.json')
    
    # Image preprocessing config
    IMG_SIZE = (224, 224)
    
    @staticmethod
    def init_app(app):
        """Initialize application"""
        # Create upload folder if not exists
        os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
        os.makedirs(os.path.join(os.path.dirname(__file__), 'models'), exist_ok=True)
