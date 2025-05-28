from openai import OpenAI
import pyttsx3
import speech_recognition as sr
from vosk import Model, KaldiRecognizer
import os
import json

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
            # 以下為常用模型名稱參考（僅供註解說明，實際使用請設定 model 參數）
            # 排名	模型名稱
            # 1	llama-guard-3-8b
            # 2	gemma2-9b-it
            # 3	llama3-70b-8192
            # 4	llama3-8b-8192
            # 5	meta-llama/llama-guard-4-12b
            # 6	llama-3.1-8b-instant
            # 7	llama-3.3-70b-versatile
            # 8	mistral-saba-24b
            # 9	meta-llama/llama-4-scout-17b-16e-instruct
            # 10	deepseek-r1-distill-llama-70b
            # 11	qwen-qwq-32b
            # 12	meta-llama/llama-4-maverick-17b-128e-instruct
            # 13	compound-beta
            # 14	compound-beta-mini
            # 15	allam-2-7b
            model="deepseek-r1-distill-llama-70b",
            messages=[
                {"role": "system", "content": "回覆的內容請永遠使用繁體中文，不要回覆<think>的內容，只要回覆重要的10~20字即可"},
                {"role": "system", "content": "請忽略 <think> 標籤及其內容，回覆時不要包含任何 <think> 標籤的內容，只需回覆重要的10~20字即可。"},
                {"role": "user", "content": prompt}
            ]
        )
        raw_response = response.choices[0].message.content
        return clean_response(raw_response)
        #return response.choices[0].message.content
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

# 初始化 Vosk 模型
vosk_model_path = "vosk-model-small-cn-0.22"  # 請確保下載並解壓縮模型到此路徑
if not os.path.exists(vosk_model_path):
    raise FileNotFoundError(f"Vosk 模型未找到，請下載並解壓縮到 {vosk_model_path}")
model = Model(vosk_model_path)

def recognize_speech_from_mic():
    """使用 Vosk 和 SpeechRecognition 從麥克風接收語音並轉換為文字"""
    # 列出可用的麥克風裝置，幫助診斷問題
    print("可用的麥克風裝置:")
    for index, name in enumerate(sr.Microphone.list_microphone_names()):
        print(f"麥克風 #{index}: {name}")
    
    print("準備麥克風中...")
    recognizer = sr.Recognizer()
    
    try:
        with sr.Microphone() as source:
            print("請開始說話 (大聲且清晰地說)...")
            # 更長時間的環境噪音調整，以提高準確度
            recognizer.adjust_for_ambient_noise(source, duration=2)
            print("正在聆聽...")
            # 增加超時和語音時間限制，確保能夠捕獲完整句子
            audio = recognizer.listen(source, timeout=12, phrase_time_limit=12)
            print("接收到音訊，處理中...")
            
            # 輸出音訊資訊以診斷問題
            print(f"音訊樣本率: {audio.sample_rate}Hz, 樣本寬度: {audio.sample_width}位元")
            
    except sr.WaitTimeoutError:
        print("未檢測到語音，請重試。")
        return ""
    except Exception as e:
        print(f"麥克風錯誤: {e}")
        return ""

    try:
        # 使用 Google 語音識別嘗試識別（如果有網絡連接）
        try:
            google_result = recognizer.recognize_google(audio, language="zh-TW")
            print(f"Google 識別結果: {google_result}")
            return google_result
        except:
            print("Google 語音識別失敗，嘗試使用 Vosk...")
        
        # 使用 Vosk 進行本地語音識別
        print("開始 Vosk 識別...")
        recognizer_vosk = KaldiRecognizer(model, 16000)
        # 將音訊轉換為原始數據
        raw_data = audio.get_raw_data()
        print(f"原始音訊數據長度: {len(raw_data)} 位元組")
        
        # 處理音訊數據
        if recognizer_vosk.AcceptWaveform(raw_data):
            result = recognizer_vosk.Result()
            print(f"Vosk 原始結果: {result}")
            # 嘗試解析 JSON 結果
            import json
            parsed_result = json.loads(result)
            text = parsed_result.get("text", "")
            if text:
                print(f"Vosk 識別結果: {text}")
                return text.strip()
            else:
                print("Vosk 未能識別語音內容，請重試。")
                return ""
        else:
            vosk_partial = recognizer_vosk.PartialResult()
            print(f"Vosk 部分結果: {vosk_partial}")
            print("語音輸入不完整或無法處理，請重試。")
            return ""
    except Exception as e:
        print(f"語音識別失敗: {e}")
        return ""

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
        #print("\n播放語音回應中...")
        #text_to_speech(ai_response, rate=150, voice_id=voice_id)

def clean_response(response):
    """
    移除回應中的 <think> 標籤及其內容
    """
    import re
    # 使用正則表達式移除 <think> 標籤及其內容
    cleaned_response = re.sub(r"<think>.*?</think>", "", response, flags=re.DOTALL)
    return cleaned_response.strip()

def interactive_chat_with_speech():
    """互動式對話主函數，支援語音輸入"""
    # 讀取組態檔
    config_path = "config.json"
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"組態檔未找到，請確保 {config_path} 存在並包含必要的設定。")

    with open(config_path, "r", encoding="utf-8") as config_file:
        config = json.load(config_file)

    api_key = config.get("api_key")
    base_url = config.get("base_url")

    if not api_key or not base_url:
        raise ValueError("組態檔中缺少 api_key 或 base_url 設定。")

    # 初始化 OpenAI 客戶端時使用組態檔中的設定
    client = OpenAI(
        api_key=api_key,
        base_url=base_url
    )

    # 設置語音
    voice_id = setup_voice()

    print("=" * 50)
    print("歡迎使用 AI 語音助手！")
    print("您可以使用語音或文字輸入問題，AI 將回應並用語音播放。")
    print("輸入 'q' 結束對話。")
    print("=" * 50)

    while True:
        # 獲取用戶輸入（語音或文字）
        print("請選擇輸入方式：1. 語音 2. 文字 (輸入 q 退出): ")
        mode = input("選擇模式: ").strip()

        if mode.lower() == 'q':
            print("感謝使用，再見！")
            break

        if mode == '1':
            user_input = recognize_speech_from_mic()
            if not user_input:
                print("未能識別語音，請重試。")
                continue
        elif mode == '2':
            user_input = input("請輸入您的問題: ").strip()
        else:
            print("無效的選擇，請重試。")
            continue

        # 呼叫 AI API 獲取回應
        print("AI思考中...")
        ai_response = call_llm_api(user_input, client)

        # 顯示回應文字
        print("\nAI回應:")
        print(ai_response)

        # 將回應轉換為語音
        print("\n播放語音回應中...")
        text_to_speech(ai_response, rate=150, voice_id=voice_id)

if __name__ == "__main__":
    interactive_chat_with_speech()




