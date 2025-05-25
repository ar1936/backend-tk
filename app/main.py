import time
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import Callable

from app.api import auth, users, documents, ingestion
from app.core.config import settings
from app.core.logger import get_logger, setup_logger

# Setup root logger
logger = setup_logger(log_level=settings.LOG_LEVEL)

app = FastAPI(
    title="Document Management System",
    description="Backend service for user and document management",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(users.router, prefix="/api/users", tags=["Users"])
app.include_router(documents.router, prefix="/api/documents", tags=["Documents"])
app.include_router(ingestion.router, prefix="/api/ingestion", tags=["Ingestion"])

@app.middleware("http")
async def log_requests(request: Request, call_next: Callable):
    """Middleware to log all incoming requests and their processing time."""
    start_time = time.time()
    
    # Log request
    logger.info(
        "Request started",
        extra={
            "method": request.method,
            "path": request.url.path,
            "query_params": dict(request.query_params),
            "client": request.client.host if request.client else "unknown"
        }
    )
    
    try:
        response = await call_next(request)
        process_time = (time.time() - start_time) * 1000
        
        # Log response
        logger.info(
            "Request completed",
            extra={
                "method": request.method,
                "path": request.url.path,
                "status_code": response.status_code,
                "process_time_ms": round(process_time, 2)
            }
        )
        
        return response
        
    except Exception as e:
        process_time = (time.time() - start_time) * 1000
        logger.error(
            "Request failed",
            extra={
                "method": request.method,
                "path": request.url.path,
                "process_time_ms": round(process_time, 2),
                "error": str(e),
                "error_type": type(e).__name__
            },
            exc_info=True
        )
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "Internal Server Error"}
        )

@app.get("/")
async def root():
    """Root endpoint that returns a welcome message."""
    logger.info("Root endpoint accessed")
    return {"message": "Welcome to Document Management System API"}
