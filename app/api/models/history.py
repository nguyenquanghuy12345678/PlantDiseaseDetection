"""
Pydantic models for history requests and responses
"""
from pydantic import BaseModel
from typing import List


class HistoryItem(BaseModel):
    """Single history entry"""
    timestamp: str
    disease: str
    confidence: float
    image_url: str


class HistoryResponse(BaseModel):
    """Response model for history endpoint"""
    history: List[HistoryItem]


class ClearHistoryResponse(BaseModel):
    """Response model for clear history endpoint"""
    success: bool = True
