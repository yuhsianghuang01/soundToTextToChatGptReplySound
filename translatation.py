

import os
from dotenv import load_dotenv

# 載入 .env 檔案中的環境變數
load_dotenv(dotenv_path=os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))

def translate_text(text, source_lang, target_lang):
    from openai import OpenAI
    client = OpenAI(
        api_key=os.environ.get("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"),
        base_url=os.environ.get("https://api.groq.com/openai/v1"),
    )
    messages = [
        {"role": "system", "content": f"You are a translation assistant. Translate from {source_lang} to {target_lang}."},
        {"role": "user", "content": text}
    ]
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # 可根據你的帳號權限調整模型名稱
            messages=messages,
            temperature=0.3
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error: {e}")
        return None


def main():
    text = "Hello, how are you?"
    source_lang = "English"
    target_lang = "Chinese"
    translation = translate_text(text, source_lang, target_lang)
    print("原文:", text)
    print("翻譯:", translation)


if __name__ == "__main__":
    main()



