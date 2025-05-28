import cv2
import os
import pyttsx3
import numpy as np

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
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("無法開啟攝影機")
        return

    prev_center = None
    direction_text = ""
    last_spoken_direction = ""

    while True:
        ret, frame = cap.read()
        if not ret:
            print("無法讀取攝影機畫面")
            break

        # 影像鏡像翻轉，方便手勢操作
        frame = cv2.flip(frame, 1)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # 膚色範圍遮罩（可根據實際情況調整）
        lower_skin = np.array([0, 20, 70], dtype=np.uint8)
        upper_skin = np.array([20, 255, 255], dtype=np.uint8)
        mask = cv2.inRange(hsv, lower_skin, upper_skin)
        mask = cv2.GaussianBlur(mask, (5, 5), 0)

        # 找輪廓
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        if contours:
            # 取最大輪廓（假設為手）
            max_contour = max(contours, key=cv2.contourArea)
            if cv2.contourArea(max_contour) > 3000:
                x, y, w, h = cv2.boundingRect(max_contour)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
                # 計算手勢中心點
                M = cv2.moments(max_contour)
                if M["m00"] != 0:
                    center_x = int(M["m10"] / M["m00"])
                    center_y = int(M["m01"] / M["m00"])
                    cv2.circle(frame, (center_x, center_y), 8, (0, 0, 255), -1)
                    if prev_center is not None:
                        dx = center_x - prev_center[0]
                        dy = center_y - prev_center[1]
                        threshold = 20
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
                    prev_center = (center_x, center_y)
        # 語音播報
        if direction_text and direction_text != last_spoken_direction:
            if direction_text == "up":
                text_to_speech("手勢向上")
            elif direction_text == "down":
                text_to_speech("手勢向下")
            elif direction_text == "left":
                text_to_speech("手勢向左")
            elif direction_text == "right":
                text_to_speech("手勢向右")
            last_spoken_direction = direction_text
        # 顯示方向
        if direction_text:
            cv2.putText(frame, direction_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
        cv2.imshow('Gesture Detection', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
