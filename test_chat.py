import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_URL = "http://localhost:8000/chat"
API_KEY = os.getenv("SECRET_KEY")

def send_message(prompt: str):
    headers = {
        "Content-Type": "application/json",
        "X-API-Key": API_KEY
    }
    data = {
        "prompt": prompt
    }
    
    response = requests.post(API_URL, headers=headers, json=data)
    return response.json()

if __name__ == "__main__":
    while True:
        user_input = input("You: ")
        if user_input.lower() in ['quit', 'exit', 'q']:
            break
        response = send_message(user_input)
        print(f"AI: {response['response']}") 