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

def list_available_voices():
    """列出所有可用的語音選項"""
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    
    print("可用語音列表:")
    for i, voice in enumerate(voices):
        print(f"語音 #{i}")
        print(f"  ID: {voice.id}")
        print(f"  名稱: {voice.name}")
        print(f"  語言: {voice.languages}")
        print(f"  性別: {voice.gender}")
        print(f"  年齡: {voice.age}")
        print("------------------------")
    
    return voices

def main():
    # 列出所有可用語音
    voices = list_available_voices()
    
    # 播放中文語音範例
    print("\n播放中文語音範例...")
    text_to_speech("你好，這是一個文字轉語音的範例。")
    
    # 播放英文語音範例
    print("\n播放英文語音範例...")
    text_to_speech("Hello, this is a text-to-speech example.")
    
    # 如果有多個語音可用，嘗試使用第二個語音
    if len(voices) > 1:
        print("\n使用不同語音播放...")
        text_to_speech("這是使用不同語音的範例。", voice_id=voices[1].id)
    
    # 嘗試不同語速
    print("\n使用較慢的語速播放...")
    text_to_speech("這是慢速語音的範例。", rate=100)
    
    print("\n使用較快的語速播放...")
    text_to_speech("這是快速語音的範例。", rate=200)

if __name__ == "__main__":
    main()
