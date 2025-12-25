"""
FastAPI Main Application
Plant Disease Detection with AI
"""
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from fastapi.responses import JSONResponse

from app.config import settings
from app.api.routes import pages, predict, history

# Initialize FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="AI-powered plant disease detection for Vietnamese agriculture",
    debug=settings.DEBUG
)

# Add session middleware (replaces Flask sessions)
app.add_middleware(
    SessionMiddleware,
    secret_key=settings.SECRET_KEY,
    max_age=settings.SESSION_MAX_AGE,
    session_cookie="plant_disease_session"
)

# Add CORS middleware (if needed for future SPA)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory=str(settings.STATIC_DIR)), name="static")

# Setup Jinja2 templates
templates = Jinja2Templates(directory=str(settings.TEMPLATES_DIR))

# Include routers
app.include_router(pages.router, tags=["Pages"])
app.include_router(predict.router, prefix="/api", tags=["Prediction"])
app.include_router(history.router, prefix="/api", tags=["History"])


# Exception handlers
@app.exception_handler(413)
async def request_entity_too_large_handler(request: Request, exc: Exception):
    """Handle file too large error"""
    return JSONResponse(
        status_code=413,
        content={"error": f"File too large. Maximum size is {settings.MAX_FILE_SIZE // (1024*1024)}MB"}
    )


@app.exception_handler(404)
async def not_found_handler(request: Request, exc: Exception):
    """Handle 404 errors - serve homepage for HTML requests"""
    if "text/html" in request.headers.get("accept", ""):
        return templates.TemplateResponse("index.html", {"request": request})
    return JSONResponse(status_code=404, content={"error": "Not found"})


# Startup event
@app.on_event("startup")
async def startup_event():
    """Initialize application on startup"""
    print("=" * 60)
    print(f"🌱 {settings.APP_NAME} v{settings.APP_VERSION}")
    print("=" * 60)
    print(f"📍 Running on: http://{settings.HOST}:{settings.PORT}")
    print(f"📁 Upload folder: {settings.UPLOAD_FOLDER}")
    print(f"🤖 Model path: {settings.MODEL_PATH}")
    print(f"📚 API docs: http://{settings.HOST}:{settings.PORT}/docs")
    print("=" * 60)
    
    # Pre-load ML model (optional optimization)
    try:
        from app.core.ml import model_handler
        print("✅ ML model handler loaded")
    except Exception as e:
        print(f"⚠️  ML model loading warning: {e}")


# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    print("🛑 Shutting down Plant Disease Detection API...")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )
