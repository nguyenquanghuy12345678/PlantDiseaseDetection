"""
Prediction routes for plant disease detection
"""
from fastapi import APIRouter, UploadFile, File, HTTPException, Request
from datetime import datetime
import uuid
import base64
import os
from pathlib import Path

from app.config import settings
from app.api.models.prediction import (
    WebcamPredictRequest,
    PredictionResponse,
    PredictionItem,
    TreatmentInfo,
    ErrorResponse
)

router = APIRouter()


def allowed_file(filename: str) -> bool:
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in settings.ALLOWED_EXTENSIONS


def secure_filename(filename: str) -> str:
    """Generate secure filename"""
    # Remove any directory components
    filename = os.path.basename(filename)
    # Remove any non-alphanumeric characters except dots and dashes
    import re
    filename = re.sub(r'[^\w\s.-]', '', filename)
    return filename


@router.post("/predict/upload", response_model=PredictionResponse, responses={400: {"model": ErrorResponse}, 500: {"model": ErrorResponse}})
async def predict_upload(request: Request, file: UploadFile = File(...)):
    """
    Handle file upload prediction
    
    - **file**: Image file (PNG, JPG, JPEG) - max 16MB
    """
    temp_file = None
    
    try:
        # Validate file
        if not file.filename:
            raise HTTPException(status_code=400, detail="No file selected")
        
        if not allowed_file(file.filename):
            raise HTTPException(
                status_code=400,
                detail=f"Invalid file type. Only {', '.join(settings.ALLOWED_EXTENSIONS)} allowed"
            )
        
        # Save file with unique name
        filename = secure_filename(file.filename)
        unique_filename = f"{uuid.uuid4().hex}_{filename}"
        image_path = settings.UPLOAD_FOLDER / unique_filename
        
        # Write file
        contents = await file.read()
        with open(image_path, 'wb') as f:
            f.write(contents)
        
        temp_file = image_path
        
        # Validate image
        from app.core.ml.preprocessing import validate_image
        if not validate_image(str(image_path)):
            raise HTTPException(status_code=400, detail="Invalid image file")
        
        # Get predictions
        from app.core.ml.model_handler import get_predictions
        from app.core.data.treatment_data import get_treatment_info
        
        predictions = get_predictions(str(image_path), top_k=3)
        
        # Get treatment info for top prediction
        top_class = predictions[0]['class']
        treatment = get_treatment_info(top_class)
        
        # Build response
        result = PredictionResponse(
            success=True,
            timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            top_prediction=PredictionItem(**predictions[0]),
            all_predictions=[PredictionItem(**p) for p in predictions],
            treatment=TreatmentInfo(**treatment),
            image_url=f"/static/uploads/{unique_filename}"
        )
        
        # Add to session history
        if "history" not in request.session:
            request.session["history"] = []
        
        history_entry = {
            "timestamp": result.timestamp,
            "disease": predictions[0]["class"],
            "confidence": predictions[0]["confidence"],
            "image_url": result.image_url
        }
        
        request.session["history"].insert(0, history_entry)
        request.session["history"] = request.session["history"][:10]  # Keep last 10
        
        return result
        
    except HTTPException:
        # Clean up temp file on error
        if temp_file and temp_file.exists():
            temp_file.unlink()
        raise
    
    except Exception as e:
        # Clean up temp file on error
        if temp_file and temp_file.exists():
            temp_file.unlink()
        
        # Log the full error for debugging
        import traceback
        print(f"❌ Upload prediction error: {str(e)}")
        print(traceback.format_exc())
        
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")


@router.post("/predict/webcam", response_model=PredictionResponse, responses={400: {"model": ErrorResponse}, 500: {"model": ErrorResponse}})
async def predict_webcam(request: Request, data: WebcamPredictRequest):
    """
    Handle webcam base64 image prediction
    
    - **image**: Base64 encoded image data (with or without data URL prefix)
    """
    temp_file = None
    
    try:
        # Decode base64
        image_data = data.image
        
        # Remove data URL prefix if present
        if 'base64,' in image_data:
            image_data = image_data.split('base64,')[1]
        
        # Decode
        try:
            image_bytes = base64.b64decode(image_data)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Invalid base64 data: {str(e)}")
        
        # Save to file
        unique_filename = f"{uuid.uuid4().hex}_webcam.jpg"
        image_path = settings.UPLOAD_FOLDER / unique_filename
        
        with open(image_path, 'wb') as f:
            f.write(image_bytes)
        
        temp_file = image_path
        
        # Validate image
        from app.core.ml.preprocessing import validate_image
        if not validate_image(str(image_path)):
            raise HTTPException(status_code=400, detail="Invalid image file")
        
        # Get predictions
        from app.core.ml.model_handler import get_predictions
        from app.core.data.treatment_data import get_treatment_info
        
        predictions = get_predictions(str(image_path), top_k=3)
        
        # Get treatment info for top prediction
        top_class = predictions[0]['class']
        treatment = get_treatment_info(top_class)
        
        # Build response
        result = PredictionResponse(
            success=True,
            timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            top_prediction=PredictionItem(**predictions[0]),
            all_predictions=[PredictionItem(**p) for p in predictions],
            treatment=TreatmentInfo(**treatment),
            image_url=f"/static/uploads/{unique_filename}"
        )
        
        # Add to session history
        if "history" not in request.session:
            request.session["history"] = []
        
        history_entry = {
            "timestamp": result.timestamp,
            "disease": predictions[0]["class"],
            "confidence": predictions[0]["confidence"],
            "image_url": result.image_url
        }
        
        request.session["history"].insert(0, history_entry)
        request.session["history"] = request.session["history"][:10]  # Keep last 10
        
        return result
        
    except HTTPException:
        # Clean up temp file on error
        if temp_file and temp_file.exists():
            temp_file.unlink()
        raise
    
    except Exception as e:
        # Clean up temp file on error
        if temp_file and temp_file.exists():
            temp_file.unlink()
        
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")
