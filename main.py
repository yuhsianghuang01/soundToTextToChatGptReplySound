import requests

API_URL = "https://api.deepseek.com/v1/chat/completions"
API_KEY = "YOUR_DEEPSEEK_API_KEY"  # 請替換為你的 DeepSeek API 金鑰

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

data = {
    "model": "deepseek-chat",
    "messages": [
        {"role": "user", "content": "你好，DeepSeek！"}
    ]
}

response = requests.post(API_URL, headers=headers, json=data)
print(response.json())