import requests
import os

API_KEY = "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"  # Replace with your actual OpenAI API key
API_URL = "https://api.openai.com/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

data = {
    "model": "gpt-3.5-turbo",
    "messages": [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello, who are you?"}
    ]
}

response = requests.post(API_URL, headers=headers, json=data)
print(response.json())