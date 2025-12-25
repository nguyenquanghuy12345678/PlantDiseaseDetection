"""
FastAPI Application Configuration using Pydantic Settings
"""
from pydantic_settings import BaseSettings
from pathlib import Path
from typing import Set


class Settings(BaseSettings):
    """Application settings with environment variable support"""
    
    # App settings
    APP_NAME: str = "Plant Disease Detection API"
    APP_VERSION: str = "2.0.0"
    SECRET_KEY: str = "dev-secret-key-change-in-production"
    DEBUG: bool = True
    
    # Server settings
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # File upload settings
    MAX_FILE_SIZE: int = 16 * 1024 * 1024  # 16MB
    ALLOWED_EXTENSIONS: Set[str] = {"png", "jpg", "jpeg"}
    
    # Paths
    BASE_DIR: Path = Path(__file__).parent.parent
    UPLOAD_FOLDER: Path = BASE_DIR / "static" / "uploads"
    MODEL_PATH: Path = BASE_DIR / "models" / "disease_model.h5"
    CLASS_INDICES_PATH: Path = BASE_DIR / "models" / "class_indices.json"
    STATIC_DIR: Path = BASE_DIR / "static"
    TEMPLATES_DIR: Path = BASE_DIR / "templates"
    
    # Image processing settings
    IMG_SIZE: tuple = (224, 224)
    
    # Session settings
    SESSION_MAX_AGE: int = 86400  # 24 hours in seconds
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
    
    def init_folders(self):
        """Create necessary folders if they don't exist"""
        self.UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)
        (self.BASE_DIR / "models").mkdir(parents=True, exist_ok=True)


# Create global settings instance
settings = Settings()

# Initialize folders on import
settings.init_folders()
