from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from marketplace_ai import MarketplaceAI
from pydantic import BaseModel
import os
from dotenv import load_dotenv
import logging
from typing import List, Optional

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Marketplace AI API",
    description="API for AI-powered marketplace assistant",
    version="1.0.0"
)

# Updated CORS (allows both localhost and production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",           # For local development
        "https://eco-finds-sigma.vercel.app"  # For production
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Initialize AI
try:
    marketplace_ai = MarketplaceAI()
    logger.info("✅ Marketplace AI initialized successfully!")
except Exception as e:
    logger.error(f"❌ Error initializing Marketplace AI: {str(e)}")
    marketplace_ai = None

# Request/Response Models
class ChatRequest(BaseModel):
    message: str
    user_id: Optional[str] = "default"
    images: Optional[List[dict]] = []

class ChatResponse(BaseModel):
    success: bool
    response: str
    needs_images: Optional[bool] = False
    error: Optional[str] = None

class HealthResponse(BaseModel):
    status: str
    ai_initialized: bool
    version: str

# API Endpoints
@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Main chat endpoint - send message, get AI response"""
    
    if not marketplace_ai:
        raise HTTPException(
            status_code=500, 
            detail="AI system not initialized"
        )
    
    if not request.message.strip():
        raise HTTPException(
            status_code=400, 
            detail="Message cannot be empty"
        )
    
    try:
        # Create context for images if provided
        context = {}
        if request.images:
            context['images'] = request.images
            context['has_images'] = True
        
        # Get AI response
        response = marketplace_ai.run(
            request.message, 
            request.user_id, 
            context
        )
        
        return ChatResponse(
            success=True,
            response=response.content,
            needs_images=getattr(response, 'needs_images', False)
        )
        
    except Exception as e:
        logger.error(f"Error in chat: {str(e)}")
        return ChatResponse(
            success=False,
            response="",
            error=str(e)
        )

@app.get("/api/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        ai_initialized=marketplace_ai is not None,
        version="1.0.0"
    )

@app.post("/api/clear")
async def clear_conversation(request: Request):
    """Clear conversation history for a user"""
    data = await request.json()
    user_id = data.get("user_id", "default")
    
    if marketplace_ai:
        marketplace_ai.clear_history(user_id)
    
    return {"success": True, "message": "Conversation cleared"}

@app.get("/")
async def root():
    """Root endpoint with API info"""
    return {
        "name": "Marketplace AI API",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "chat": "/api/chat",
            "health": "/api/health", 
            "clear": "/api/clear",
            "docs": "/docs"
        }
    }

if __name__ == "__main__":
    import uvicorn
    
    print("🚀 Starting Marketplace AI API...")
    print("📚 API Documentation: http://localhost:8000/docs")
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
