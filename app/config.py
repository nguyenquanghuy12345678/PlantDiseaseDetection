"""
FastAPI Application Configuration using Pydantic Settings
"""
from pydantic_settings import BaseSettings, SettingsConfigDict, PydanticBaseSettingsSource
from pydantic import Field
from pathlib import Path
from typing import Set, Optional, Tuple, Type
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
    
    # File upload settings - Not configurable via env vars
    MAX_FILE_SIZE: int = 16 * 1024 * 1024  # 16MB
    ALLOWED_EXTENSIONS: Set[str] = {"png", "jpg", "jpeg"}
    CORS_ORIGINS: list = ["*"]  # Override in production
    
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
    
    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: Type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> Tuple[PydanticBaseSettingsSource, ...]:
        """Customize settings sources to exclude complex types from env parsing"""
        # Filter out ALLOWED_EXTENSIONS and CORS_ORIGINS from env sources
        class FilteredEnvSettings(PydanticBaseSettingsSource):
            def __call__(self):
                data = env_settings() if callable(env_settings) else {}
                # Remove fields that shouldn't be parsed from env
                data.pop('ALLOWED_EXTENSIONS', None)
                data.pop('CORS_ORIGINS', None)
                return data
        
        return (
            init_settings,
            FilteredEnvSettings(settings_cls),
            dotenv_settings,
            file_secret_settings,
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
