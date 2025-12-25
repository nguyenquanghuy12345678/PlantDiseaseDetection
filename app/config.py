"""
FastAPI Application Configuration using Pydantic Settings
"""
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from pathlib import Path
from typing import Set, Optional
import os


class Settings(BaseSettings):
    """Application settings with environment variable support"""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )
    
    # App settings
    APP_NAME: str = "Plant Disease Detection API"
    APP_VERSION: str = "2.0.0"
    SECRET_KEY: str = "dev-secret-key-change-in-production-min-32-chars"
    DEBUG: bool = True
    
    # Server settings
    HOST: str = "0.0.0.0"
    PORT: int = int(os.getenv("PORT", "8000"))  # Render uses PORT env var
    
    # File upload settings
    MAX_FILE_SIZE: int = 16 * 1024 * 1024  # 16MB
    ALLOWED_EXTENSIONS: Set[str] = Field(
        default={"png", "jpg", "jpeg"},
        json_schema_extra={"env_ignore": True}
    )
    
    # Paths
    BASE_DIR: Path = Path(__file__).parent.parent
    UPLOAD_FOLDER: Path = BASE_DIR / "static" / "uploads"
    MODEL_PATH: Path = BASE_DIR / "models" / "disease_model.h5"
    CLASS_INDICES_PATH: Path = BASE_DIR / "models" / "class_indices.json"
    STATIC_DIR: Path = BASE_DIR / "static"
    TEMPLATES_DIR: Path = BASE_DIR / "templates"
    
    # Image processing settings
    IMG_HEIGHT: int = 224
    IMG_WIDTH: int = 224
    
    @property
    def IMG_SIZE(self) -> tuple:
        """Return image size as tuple"""
        return (self.IMG_HEIGHT, self.IMG_WIDTH)
    
    # Session settings
    SESSION_MAX_AGE: int = 86400  # 24 hours in seconds
    
    # CORS settings (for production)
    CORS_ORIGINS: list = Field(
        default=["*"],
        json_schema_extra={"env_ignore": True}
    )
        
    def get_env_info(self) -> dict:
        """Get current environment info for debugging"""
        return {
            "app_name": self.APP_NAME,
            "version": self.APP_VERSION,
            "debug": self.DEBUG,
            "port": self.PORT,
            "environment": "development" if self.DEBUG else "production"
        }
    
    def init_folders(self):
        """Create necessary folders if they don't exist"""
        self.UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)
        (self.BASE_DIR / "models").mkdir(parents=True, exist_ok=True)


# Create global settings instance
settings = Settings()

# Initialize folders on import
settings.init_folders()
