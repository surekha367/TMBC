from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.routes import whatsapp
from app.models import Base
from app.config import engine, settings
from app.exceptions import WhatsAppAPIException, InvalidPhoneNumberException, ConfigurationException, DatabaseException

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for FastAPI
    Sets up database tables and performs startup operations
    """
    # Create database tables
    Base.metadata.create_all(bind=engine)
    print("Database tables created or verified")
    yield
    # Shutdown operations can go here
    print("Application shutting down")

# Initialize FastAPI app with lifespan
app = FastAPI(
    title=settings.app_name,
    description="FastAPI application to send messages via WhatsApp Business API",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(whatsapp.router, prefix="/api/v1")

# Exception handlers
@app.exception_handler(WhatsAppAPIException)
async def whatsapp_api_exception_handler(request: Request, exc: WhatsAppAPIException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"success": False, "message": exc.detail}
    )

@app.exception_handler(InvalidPhoneNumberException)
async def invalid_phone_exception_handler(request: Request, exc: InvalidPhoneNumberException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"success": False, "message": exc.detail}
    )

@app.exception_handler(ConfigurationException)
async def config_exception_handler(request: Request, exc: ConfigurationException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"success": False, "message": exc.detail}
    )

@app.exception_handler(DatabaseException)
async def database_exception_handler(request: Request, exc: DatabaseException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"success": False, "message": exc.detail}
    )

@app.get("/", tags=["Root"])
async def root():
    """
    Root endpoint for health check and basic info
    """
    return {
        "message": f"{settings.app_name} is running in {settings.environment} mode",
        "documentation": "/docs",
        "send_message_endpoint": "/api/v1/whatsapp/send_message",
        "logs_endpoint": "/api/v1/whatsapp/logs"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="localhost", port=8000, reload=settings.debug)