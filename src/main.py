from fastapi import FastAPI, HTTPException, Security, Body, Request
from fastapi.security import APIKeyHeader
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
from dotenv import load_dotenv
import os
import logging
from pydantic import BaseModel
from src.ollama_client import ollama_client
from src.system_ops import system_ops
from src.monitoring import system_monitor
from typing import List, Dict, Optional
from pathlib import Path

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="AI Assistant MCP Server",
    description="Local AI assistant with system control capabilities",
    version="0.1.0"
)

# Configure templates
templates = Jinja2Templates(directory="src/templates")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
API_KEY_NAME = "X-API-Key"
api_key_header = APIKeyHeader(name=API_KEY_NAME)

def get_api_key(api_key_header: str = Security(api_key_header)) -> str:
    if api_key_header == os.getenv("SECRET_KEY"):
        return api_key_header
    raise HTTPException(
        status_code=403,
        detail="Invalid API Key"
    )

@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Chat endpoints
class ChatRequest(BaseModel):
    prompt: str
    context: dict = None

class ChatResponse(BaseModel):
    response: str

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(
    chat_request: ChatRequest,
    api_key: str = Security(get_api_key)
):
    try:
        logger.info(f"Received chat request with prompt: {chat_request.prompt}")
        response = ollama_client.chat(chat_request.prompt, chat_request.context)
        logger.info("Successfully processed chat request")
        return ChatResponse(response=response)
    except Exception as e:
        logger.error(f"Error processing chat request: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error processing chat request: {str(e)}"
        )

# System control endpoints
class FileOperationRequest(BaseModel):
    path: str
    content: Optional[str] = None

@app.get("/system/files/list/{path:path}")
async def list_directory(
    path: str,
    api_key: str = Security(get_api_key)
):
    return system_ops.list_directory(path)

@app.get("/system/files/read/{path:path}")
async def read_file(
    path: str,
    api_key: str = Security(get_api_key)
):
    return {"content": system_ops.read_file(path)}

@app.post("/system/files/write")
async def write_file(
    request: FileOperationRequest,
    api_key: str = Security(get_api_key)
):
    return system_ops.write_file(request.path, request.content)

@app.get("/system/processes")
async def list_processes(api_key: str = Security(get_api_key)):
    return {"processes": system_ops.list_processes()}

@app.get("/system/processes/{pid}")
async def get_process_info(pid: int, api_key: str = Security(get_api_key)):
    return system_ops.get_process_info(pid)

@app.delete("/system/processes/{pid}")
async def terminate_process(pid: int, api_key: str = Security(get_api_key)):
    return system_ops.terminate_process(pid)

# Monitoring endpoints
@app.get("/monitoring/metrics")
async def get_metrics(api_key: str = Security(get_api_key)):
    return system_monitor.get_system_metrics()

@app.get("/monitoring/history")
async def get_metrics_history(api_key: str = Security(get_api_key)):
    return system_monitor.get_metrics_history()

@app.get("/monitoring/alerts")
async def get_alerts(api_key: str = Security(get_api_key)):
    return {"alerts": system_monitor.get_alerts()}

@app.get("/monitoring")
async def monitoring_dashboard(request: Request):
    return templates.TemplateResponse("monitoring.html", {"request": request})

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )