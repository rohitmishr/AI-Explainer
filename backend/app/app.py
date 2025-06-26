from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="AI Code Explainer",
    description="A FastAPI-powered backend that uses local LLMs via [Ollama](https://ollama.com) to intelligently explain your code. Upload any `.py`, `.js`, `.ts`, `.html`, `.json`, `.txt`, or even a `.zip` file of your project — and get an instant explanation with audio narration using Google Text-to-Speech (`gTTS`).",
    version="1.0"
)

# Allow requests from extension
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

