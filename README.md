# 專案 Python 程式與功能對照表

| 檔案名稱              | 主要功能/用途                                                                 |
|----------------------|------------------------------------------------------------------------------|
| main.py              | 呼叫 Groq LLM API，取得 AI 回應（繁體中文），可作為 GPT API 呼叫範例。         |
| call_llm_api.py      | 呼叫本地或遠端 LLM API，取得 AI 回應（gpt-4o-mini），可作為 API 測試。         |
| libSizeCalc.py       | 查詢 PyPI 套件及其相依套件的總大小（MB），適合分析 Python 套件體積。           |
| test_cv2.py          | 測試 OpenCV GUI 功能（顯示空白視窗），驗證 cv2.imshow 是否可用。              |
| winApp.py            | 簡單 Tkinter 視窗應用程式，按下按鈕顯示 Hello 訊息。                         |
| camera.py            | 攝影機即時畫面顯示、拍照、錄影（含中文訊息顯示），支援 mp4 錄影與照片存檔。   |
| faceCamera.py        | 人臉與眼睛偵測，並以語音播報眼睛移動方向，支援即時視訊顯示。                 |
| faceMarkCamera.py    | 人臉偵測與標記，支援拍照、錄影、停止錄影等功能。                             |
| gesture.py           | 手勢偵測（膚色遮罩），偵測手勢方向並語音播報（上/下/左/右）。                |
| say.py               | 文字轉語音（TTS）功能，支援多語音、語速、音量切換，並可列出所有語音。         |
| translatation.py     | 使用 Groq API 進行多語言翻譯（可自訂來源與目標語言）。                        |
| textAndReplay.py     | AI 語音助手：可用文字或語音輸入，AI 回應並語音播放，支援互動式對話。         |

---

## 安裝與執行說明

1. **安裝 Python 相關套件**（建議使用 uv，或 pip）：
   ```sh
   uv pip install -r requirements.txt
   ```
   如無 requirements.txt，請依需求安裝：
   ```sh
   uv pip install opencv-python pyttsx3 pillow openai speechrecognition vosk requests python-dotenv
   ```

2. **執行程式**：
   - 一般執行（以 `textAndReplay.py` 為例）：
     ```sh
     python textAndReplay.py
     ```
   - 使用 uv 執行：
     ```sh
     uv run textAndReplay.py
     ```

3. **常見功能說明**：
   - `camera.py`、`faceCamera.py`、`faceMarkCamera.py`、`gesture.py` 需有攝影機設備。
   - `faceCamera.py`、`faceMarkCamera.py` 需放置 `haarcascade_frontalface_default.xml`、`haarcascade_eye.xml` 於同目錄。
   - `textAndReplay.py` 需 `config.json` 設定 API 金鑰與 base_url，vosk 語音模型需下載解壓於 `vosk-model-small-cn-0.22`。
   - `say.py`、`gesture.py`、`faceCamera.py` 皆可語音播報，支援多語音。
   - `libSizeCalc.py` 需網路連線查詢 PyPI。

---

## 各程式詳細功能摘要

- **main.py**：呼叫 Groq LLM API，取得 AI 回應（繁體中文），可作為 GPT API 呼叫範例。
- **call_llm_api.py**：呼叫本地或遠端 LLM API，取得 AI 回應（gpt-4o-mini），可作為 API 測試。
- **libSizeCalc.py**：查詢 PyPI 套件及其相依套件的總大小（MB），適合分析 Python 套件體積。
- **test_cv2.py**：測試 OpenCV GUI 功能（顯示空白視窗），驗證 cv2.imshow 是否可用。
- **winApp.py**：簡單 Tkinter 視窗應用程式，按下按鈕顯示 Hello 訊息。
- **camera.py**：攝影機即時畫面顯示、拍照、錄影（含中文訊息顯示），支援 mp4 錄影與照片存檔。
- **faceCamera.py**：人臉與眼睛偵測，並以語音播報眼睛移動方向，支援即時視訊顯示。
- **faceMarkCamera.py**：人臉偵測與標記，支援拍照、錄影、停止錄影等功能。
- **gesture.py**：手勢偵測（膚色遮罩），偵測手勢方向並語音播報（上/下/左/右）。
- **say.py**：文字轉語音（TTS）功能，支援多語音、語速、音量切換，並可列出所有語音。
- **translatation.py**：使用 Groq API 進行多語言翻譯（可自訂來源與目標語言）。
- **textAndReplay.py**：AI 語音助手：可用文字或語音輸入，AI 回應並語音播放，支援互動式對話。

---

## 常見問題與注意事項

- 如遇 OpenCV GUI 問題，請確認安裝 `opencv-python` 而非 `opencv-python-headless`。
- 如遇語音播報問題，請確認 pyttsx3 安裝正確，且系統有可用語音。
- 如需語音辨識，請下載並解壓 vosk 中文模型至 `vosk-model-small-cn-0.22`。
- API 金鑰與 base_url 請於 `config.json` 設定。
