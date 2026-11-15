
import os
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# Project folder
BASE_DIR = Path(__file__).resolve().parent

# Groq API connection
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY is missing from .env file")

client = Groq(api_key=api_key)


# Serve CSS
@app.get("/style.css")
def get_css():
    return FileResponse(BASE_DIR / "style.css", media_type="text/css")


# Display chatbot homepage
@app.get("/")
def home():
    return FileResponse(BASE_DIR / "index.html")


# Chat request
class ChatRequest(BaseModel):
    message: str


# Chat endpoint
@app.post("/chat")
def chat(request: ChatRequest):
    try:
        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {
                    "role": "system",
                    "content": "You are a friendly AI assistant."
                },
                {
                    "role": "user",
                    "content": request.message
                }
            ]
        )

        return {
            "reply": response.choices[0].message.content
        }

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Something went wrong while contacting the AI service."
        )
