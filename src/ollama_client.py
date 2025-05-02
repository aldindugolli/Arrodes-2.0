import requests
import logging
from src.config import settings
from fastapi import HTTPException

logger = logging.getLogger(__name__)

class OllamaClient:
    def __init__(self, api_url: str = None, model: str = None):
        self.api_url = api_url or settings.OLLAMA_API_URL
        self.model = model or settings.OLLAMA_MODEL
        logger.info(f"Initialized OllamaClient with URL: {self.api_url}, Model: {self.model}")

    def chat(self, prompt: str, context: dict = None) -> str:
        try:
            url = f"{self.api_url}/api/generate"
            payload = {
                "model": self.model,
                "prompt": prompt,
                "stream": False
            }
            if context:
                payload["context"] = context

            logger.info(f"Sending request to Ollama: {url}")
            logger.debug(f"Request payload: {payload}")

            response = requests.post(url, json=payload)
            response.raise_for_status()
            data = response.json()
            
            logger.info("Successfully received response from Ollama")
            logger.debug(f"Response data: {data}")
            
            return data.get("response", "")
        except requests.exceptions.RequestException as e:
            logger.error(f"Error communicating with Ollama: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Error communicating with Ollama: {str(e)}"
            )
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Unexpected error: {str(e)}"
            )

ollama_client = OllamaClient() 