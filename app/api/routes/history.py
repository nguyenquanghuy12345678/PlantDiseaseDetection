"""
History routes for managing prediction history
"""
from fastapi import APIRouter, Request
from app.api.models.history import HistoryResponse, HistoryItem, ClearHistoryResponse

router = APIRouter()


@router.get("/history", response_model=HistoryResponse)
async def get_history(request: Request):
    """Get prediction history from session"""
    history = request.session.get("history", [])
    return HistoryResponse(history=history)


@router.post("/clear-history", response_model=ClearHistoryResponse)
async def clear_history(request: Request):
    """Clear all prediction history"""
    request.session["history"] = []
    return ClearHistoryResponse(success=True)
