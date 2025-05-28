import cv2
import os
import pyttsx3

# 檢查文件是否存在的輔助函數
def check_cascade_file(file_path):
    if not os.path.exists(file_path):
        print(f"錯誤: 找不到文件 {file_path}")
        return False
    return True

# 文字轉語音函式
speech_engine = None
def text_to_speech(text, rate=150, volume=1.0, voice_id=None):
    global speech_engine
    if speech_engine is None:
        speech_engine = pyttsx3.init()
    speech_engine.setProperty('rate', rate)
    speech_engine.setProperty('volume', volume)
    voices = speech_engine.getProperty('voices')
    # 嘗試選擇中文語音
    if voice_id is not None:
        speech_engine.setProperty('voice', voice_id)
    else:
        for voice in voices:
            if any('zh' in lang.lower() or 'chi' in lang.lower() or 'tw' in lang.lower() for lang in voice.languages):
                speech_engine.setProperty('voice', voice.id)
                break
    speech_engine.say(text)
    speech_engine.runAndWait()

def main():
    print(cv2.data.haarcascades)

    # 嘗試使用腳本目錄中的 XML 文件
    script_dir = os.path.dirname(os.path.abspath(__file__))
    face_cascade_path = os.path.join(script_dir, 'haarcascade_frontalface_default.xml')
    eye_cascade_path = os.path.join(script_dir, 'haarcascade_eye.xml')

    # face_cascade_path = r"D:\fly_data\projects\雜事\250522 AI_KEY_sk-HZ-ShOnh8z3VdiJmSe9wjQ(宗霖)\demo\haarcascade_frontalface_default.xml"
    # eye_cascade_path = r"D:\fly_data\projects\雜事\250522 AI_KEY_sk-HZ-ShOnh8z3VdiJmSe9wjQ(宗霖)\demo\haarcascade_eye.xml"

    # 檢查文件是否存在
    if not check_cascade_file(face_cascade_path) or not check_cascade_file(eye_cascade_path):
        return

    # 載入分類器
    face_cascade = cv2.CascadeClassifier(face_cascade_path)
    eye_cascade = cv2.CascadeClassifier(eye_cascade_path)

    # 檢查分類器是否正確加載
    if face_cascade.empty():
        print("錯誤: 無法加載人臉分類器")
        return
    if eye_cascade.empty():
        print("錯誤: 無法加載眼睛分類器")
        return

    # 初始化攝影機
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("無法開啟攝影機")
        return

    prev_eye_centers = []  # 儲存上一幀眼睛中心點
    direction_text = ""   # 目前方向
    last_spoken_direction = ""  # 上次語音播報方向

    while True:
        ret, frame = cap.read()
        if not ret:
            print("無法讀取攝影機畫面")
            break

        # 將影像轉為灰階，提升偵測效率
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # 偵測人臉
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        for (x, y, w, h) in faces:
            # 繪製藍色框在人臉周圍
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            # 在左上角顯示人臉座標
            cv2.putText(frame, f"Face: ({x},{y},{x+w},{y+h})", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)

            # 偵測人臉區域內的眼睛
            roi_gray = gray[y:y + h, x:x + w]
            roi_color = frame[y:y + h, x:x + w]
            eyes = eye_cascade.detectMultiScale(roi_gray, scaleFactor=1.1, minNeighbors=10, minSize=(15, 15))

            eye_centers = []
            for (ex, ey, ew, eh) in eyes:
                # 繪製紅色框在眼睛周圍
                cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 0, 255), 2)
                # 在左上角顯示眼睛座標
                cv2.putText(frame, f"Eye: ({x+ex},{y+ey},{x+ex+ew},{y+ey+eh})", (x + ex, y + ey - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)

                # 計算眼睛中心點
                center_x = x + ex + ew // 2
                center_y = y + ey + eh // 2
                eye_centers.append((center_x, center_y))

            # 判斷眼睛移動方向（僅當偵測到2隻眼睛且有上一幀資料時）
            if len(eye_centers) == 2 and len(prev_eye_centers) == 2:
                # 取平均中心點
                prev_cx = (prev_eye_centers[0][0] + prev_eye_centers[1][0]) // 2
                prev_cy = (prev_eye_centers[0][1] + prev_eye_centers[1][1]) // 2
                curr_cx = (eye_centers[0][0] + eye_centers[1][0]) // 2
                curr_cy = (eye_centers[0][1] + eye_centers[1][1]) // 2
                dx = curr_cx - prev_cx
                dy = curr_cy - prev_cy
                threshold = 5  # 移動門檻
                if abs(dx) > abs(dy):
                    if dx > threshold:
                        direction_text = "right"
                    elif dx < -threshold:
                        direction_text = "left"
                else:
                    if dy > threshold:
                        direction_text = "down"
                    elif dy < -threshold:
                        direction_text = "up"
            prev_eye_centers = eye_centers

        # 在畫面左上角顯示方向前，語音播報（僅方向變化時）
        if direction_text and direction_text != last_spoken_direction:
            if direction_text == "up":
                text_to_speech("眼睛向上")
            elif direction_text == "down":
                text_to_speech("眼睛向下")
            elif direction_text == "left":
                text_to_speech("眼睛向左")
            elif direction_text == "right":
                text_to_speech("眼睛向右")
            last_spoken_direction = direction_text

        if direction_text:
            cv2.putText(frame, direction_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

        # 顯示攝影機畫面
        cv2.imshow('Face and Eye Detection', frame)

        # 按下 'q' 鍵退出
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # 釋放資源
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
