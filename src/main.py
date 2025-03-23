from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
from src.middleware.http_logger import http_logger_middleware
from src.middleware.correlation import correlation_middleware, get_correlation_id
import httpx

# Load environment variables
load_dotenv()

# Get environment variables with defaults
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "5000"))
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*").split(",")

# Create FastAPI app
app = FastAPI(
    title="FastAPI Boilerplate",
    description="A modern FastAPI boilerplate with best practices",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS if CORS_ORIGINS != ["*"] else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add middlewares - order matters! Correlation should be before logging
app.middleware("http")(correlation_middleware)
app.middleware("http")(http_logger_middleware)

@app.get("/")
async def root():
    return {"message": "Welcome to FastAPI Boilerplate"}

@app.get("/health")
async def health_check():
    return {"status": "OK"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=HOST, port=PORT)
