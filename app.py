from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional, Dict, List
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from fastapi.responses import JSONResponse
from fastapi.requests import Request
from fastapi.exception_handlers import RequestValidationError
from fastapi.exceptions import HTTPException as FastAPIHTTPException
import logging

from config_project.config import settings
from users.model import User
from users.routers import router as users_router
from restaurants.routers import router as restaurant_router
from ai_assistants.restaurant_reviews import RestaurantAssistant
from users.utils import get_current_user

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include users router with prefix
app.include_router(users_router, prefix="/users", tags=["users"])
app.include_router(restaurant_router, prefix="", tags=["restaurant_reviews"])

# Setup simple chat model without Chainlit
chat_model = ChatOpenAI(
    model_name="gpt-4o",
    temperature=0.7,
)

# Simple in-memory storage for chat history
chat_history = []

class ChatResponse(BaseModel):
    content: str
    author: Optional[str] = "assistant"

class ChatHistory(BaseModel):
    messages: List[Dict]


class ChatRequest(BaseModel):
    message: str


security = HTTPBearer()
SECRET_KEY = settings.JWT_SECRET_KEY
ALGORITHM = settings.JWT_ALGORITHM

# Global exception handlers
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.error(f"Validation error: {exc.errors()}")
    return JSONResponse(
        status_code=422,
        content={"error": exc.errors(), "status_code": 422},
    )

@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    if isinstance(exc, HTTPException):
        raise exc
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error", "status_code": 500},
    )

@app.get("/")
async def root():
    return {"message": "Welcome to the Restaurant Review Assistant API"}

@app.post("/chat/start")
async def start_chat(current_user: User = Depends(get_current_user)):
    global chat_history
    chat_history = []
    return {"message": "Chat session started. You can now send messages."}

@app.post("/chat/message")
async def send_message(input: ChatRequest, current_user: User = Depends(get_current_user)):
    global chat_history
    try:
        # Add user message to history
        chat_history.append({"content": input.message, "author": "user"})
        restaurant_assistant = RestaurantAssistant(restaurant_id=current_user.restaurant_id)
        response = await restaurant_assistant.on_message(input.message)
        # Add assistant message to history
        chat_history.append({"content": response, "author": "assistant"})
        return {"response": response, "status_code": 200}
    except Exception as exc:
        logger.error(f"Error in send_message: {str(exc)}", exc_info=True)
        raise HTTPException(status_code=500, detail="An error occurred while processing your message.")

@app.get("/chat/history", response_model=ChatHistory)
async def get_chat_history(current_user: User = Depends(get_current_user)):
    return ChatHistory(messages=chat_history)
