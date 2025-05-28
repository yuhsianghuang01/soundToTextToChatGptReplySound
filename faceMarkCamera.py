import cv2
import os
from datetime import datetime
import ctypes
import numpy as np

# 解決 OpenCV 中文亂碼問題
ctypes.windll.kernel32.SetConsoleOutputCP(65001)

def main():
    # 創建存放影片的資料夾
    video_dir = 'CameraFiles'
    os.makedirs(video_dir, exist_ok=True)

    # 初始化攝影機
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("無法開啟攝影機")
        return

    # 載入人臉偵測分類器（不用 DNN，只用 OpenCV 內建的 Haar Cascade）
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    if face_cascade.empty():
        print("無法載入人臉偵測模型，請確認 haarcascade_frontalface_default.xml 存在於程式目錄")
        return

    msg = "q鍵退出, p拍照, r錄影, s停止錄影"
    is_recording = False
    out = None

    while True:
        ret, frame = cap.read()
        if not ret:
            print("無法讀取攝影機畫面")
            break

        # 轉為灰階以利人臉偵測
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5, minSize=(60, 60))

        # 用紅框標註所有人臉
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)

        # 顯示提示訊息
        cv2.putText(frame, msg, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

        # 顯示攝影機畫面
        cv2.imshow('Face Mark Camera', frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            print("退出程式")
            break
        elif key == ord('p'):
            photo_name = datetime.now().strftime('%Y%m%d%H%M%S') + '.jpg'
            photo_path = os.path.join(video_dir, photo_name)
            cv2.imwrite(photo_path, frame)
            print(f"照片已儲存至 {photo_path}")
        elif key == ord('r'):
            if not is_recording:
                video_name = datetime.now().strftime('%Y%m%d%H%M%S') + '.mp4'
                video_path = os.path.join(video_dir, video_name)
                fourcc = cv2.VideoWriter_fourcc(*'mp4v')
                out = cv2.VideoWriter(video_path, fourcc, 20.0, (frame.shape[1], frame.shape[0]))
                is_recording = True
                print(f"開始錄影，影片將儲存至 {video_path}")
        elif key == ord('s'):
            if is_recording:
                is_recording = False
                out.release()
                print("錄影已停止")
        if is_recording and out is not None:
            out.write(frame)

    cap.release()
    if out is not None:
        out.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
