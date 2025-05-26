from openai import OpenAI
import pyttsx3

def text_to_speech(text, rate=150, volume=1.0, voice_id=None):
    """
    將文字轉換為語音並播放
    
    參數:
        text (str): 要轉換為語音的文字
        rate (int): 語音速率 (預設: 150)
        volume (float): 語音音量，範圍 0.0-1.0 (預設: 1.0)
        voice_id (str): 語音ID，如果為None則使用預設語音
    """
    # 初始化語音引擎
    engine = pyttsx3.init()
    
    # 設定語音屬性
    engine.setProperty('rate', rate)  # 語速
    engine.setProperty('volume', volume)  # 音量
    
    # 列出可用的語音
    voices = engine.getProperty('voices')
    
    # 如果指定了語音ID，則設定語音
    if voice_id is not None:
        engine.setProperty('voice', voice_id)
    
    # 轉換文字為語音並播放
    engine.say(text)
    engine.runAndWait()

def call_llm_api(prompt, client):
    """
    Call the LLM API with the given prompt.
    
    參數:
        prompt (str): 發送給 AI 的提示文字
        client: OpenAI 客戶端實例
    
    回傳:
        str: AI 的回應內容
    """
    try:
        response = client.chat.completions.create(
            # qwen-qwq-32b
            # deepseek-r1-distill-llama-70b
            # gemma2-9b-it
            # compound-beta
            # compound-beta-mini
            # distil-whisper-large-v3-en
            # llama-3.1-8b-instant
            # llama-3.3-70b-versatile
            # llama-guard-3-8b
            # llama3-70b-8192
            # llama3-8b-8192
            # meta-llama/llama-4-maverick-17b-128e-instruct
            # meta-llama/llama-4-scout-17b-16e-instruct
            # meta-llama/llama-guard-4-12b
            # mistral-saba-24b
            # whisper-large-v3
            # whisper-large-v3-turbo
            # playai-tts
            # playai-tts-arabic
            model="qwen-qwq-32b",
            messages=[
                {"role": "system", "content": "回覆的內容請永遠使用繁體中文，我問你的問題會是五言绝句或七言絕句的開頭部份幾個字，請回答我時使用五言绝句或七言絕句回覆我，不要回覆<think>的內容，只要回覆五言绝句或七言絕句即可，不需要再多給我其他文字內容"},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"發生錯誤: {e}")
        return f"抱歉，發生錯誤: {e}"

def setup_voice():
    """設置最適合的語音"""
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    
    # 尋找中文語音，如果沒有則使用預設語音
    chinese_voice = None
    for voice in voices:
        # 檢查語音是否支援中文
        if any('zh' in lang.lower() or 'chi' in lang.lower() or 'tw' in lang.lower() for lang in voice.languages):
            chinese_voice = voice.id
            break
    
    print("語音設定完成！使用以下語音：")
    if chinese_voice:
        print(f"已找到中文語音: {chinese_voice}")
        return chinese_voice
    else:
        default_voice = voices[0].id if voices else None
        print(f"未找到中文語音，使用預設語音: {default_voice}")
        return default_voice

def interactive_chat():
    """互動式對話主函數"""
    # 初始化 OpenAI 客戶端
    client = OpenAI(
        api_key="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", 
        base_url="https://api.groq.com/openai/v1"
    )
    
    # 設置語音
    voice_id = setup_voice()
    
    print("=" * 50)
    print("歡迎使用 AI 語音助手！")
    print("您可以輸入任何問題，AI 將回應並用語音播放。")
    print("輸入 'q' 結束對話。")
    print("=" * 50)
    
    # 對話歷史記錄，用於上下文理解
    conversation_history = []
    
    while True:
        # 獲取用戶輸入
        user_input = input("\n請輸入您的問題 (輸入 q 退出): ")
        
        # 檢查是否退出
        if user_input.strip().lower() == 'q':
            print("感謝使用，再見！")
            break
        
        # 將用戶輸入添加到對話歷史
        conversation_history.append({"role": "user", "content": user_input})
        
        # 顯示處理中訊息
        print("AI思考中...")
        
        # 呼叫 AI API 獲取回應
        ai_response = call_llm_api(user_input, client)
        
        # 將 AI 回應添加到對話歷史
        conversation_history.append({"role": "assistant", "content": ai_response})
        
        # 顯示回應文字
        print("\nAI回應:")
        print(ai_response)
        
        # 將回應轉換為語音
        print("\n播放語音回應中...")
        text_to_speech(ai_response, rate=150, voice_id=voice_id)

if __name__ == "__main__":
    interactive_chat()




