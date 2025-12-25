"""
Health check endpoint for monitoring
"""
from fastapi import APIRouter
from pydantic import BaseModel
from datetime import datetime
import sys
import platform

router = APIRouter()


class HealthResponse(BaseModel):
    """Health check response model"""
    status: str
    timestamp: str
    version: str
    python_version: str
    platform: str


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint for Render monitoring
    Returns 200 OK if service is running
    """
    return HealthResponse(
        status="healthy",
        timestamp=datetime.now().isoformat(),
        version="2.0.0",
        python_version=f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
        platform=platform.system()
    )
