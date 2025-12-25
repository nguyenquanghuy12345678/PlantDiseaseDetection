"""
Pydantic models for prediction requests and responses
"""
from pydantic import BaseModel, Field
from typing import List, Optional


class WebcamPredictRequest(BaseModel):
    """Request model for webcam prediction"""
    image: str = Field(..., description="Base64 encoded image data")


class PredictionItem(BaseModel):
    """Single prediction item"""
    class_: str = Field(..., alias="class", description="Disease class name in Vietnamese")
    class_index: str = Field(..., description="Disease class key")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score 0-1")


class TreatmentInfo(BaseModel):
    """Treatment information for a disease"""
    disease: str
    diagnosis: str
    treatment: str
    prevention: str
    severity: str


class PredictionResponse(BaseModel):
    """Response model for prediction endpoints"""
    success: bool = True
    timestamp: str
    top_prediction: PredictionItem
    all_predictions: List[PredictionItem]
    treatment: TreatmentInfo
    image_url: str
    
    class Config:
        populate_by_name = True


class ErrorResponse(BaseModel):
    """Error response model"""
    error: str
