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
    os.makedirs(video_dir, exist_ok=True)  # 如果資料夾不存在則自動建立

    # 初始化攝影機
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("無法開啟攝影機")
        return

    # 初始化錄影相關變數
    is_recording = False
    out = None

    # 使用PIL來顯示中文
    from PIL import ImageFont, ImageDraw, Image
    font_path = "C:/Windows/Fonts/msjh.ttc"  # Microsoft JhengHei (微軟正黑體)，請確認此路徑存在
    if not os.path.exists(font_path):
        print(f"字型檔案不存在: {font_path}")
        return
    # 載入指定字型（微軟正黑體），字型大小為24
    font = ImageFont.truetype(font_path, 24)

    def draw_text_on_frame(frame, text, position, font, fill_color=(255, 0, 0), clear_area=None):
        """
        在影像上繪製文字，並可選擇清除指定區域的文字內容。

        參數：
            frame (numpy.ndarray): OpenCV 的影像。
            text (str): 要顯示的文字。
            position (tuple): 文字的左上角座標 (x, y)。
            font (ImageFont.FreeTypeFont): PIL 的字型物件。
            fill_color (tuple): 文字顏色，預設為紅色 (255, 0, 0)。
            clear_area (tuple): 要清除的區域，格式為 [(x1, y1), (x2, y2)]，預設為 None。

        回傳：
            numpy.ndarray: 繪製後的影像。
        """
        # 將 OpenCV 的影像轉換為 PIL 的影像
        img_pil = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        draw = ImageDraw.Draw(img_pil)

        # 清除指定區域的文字內容（用背景色覆蓋文字區域）
        # if clear_area:
        #     draw.rectangle(clear_area, fill=(0, 0, 0, 0))  # 使用透明背景覆蓋文字區域

        # 繪製文字
        draw.text(position, text, font=font, fill=fill_color)

        # 將 PIL 的影像轉回 OpenCV 格式
        return cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)

    msg = "q鍵退出, p拍照, r錄影, s停止錄影";
    while True:
        ret, frame = cap.read()
        if not ret:
            print("無法讀取攝影機畫面")
            break

        # 在畫面左上角顯示紅色標題
        frame = draw_text_on_frame(
            frame,
            msg,
            position=(10, 5),
            font=font,
            fill_color=(255, 0, 0),
            clear_area=[(0, 0), (frame.shape[1], 40)]
        )

        # 顯示攝影機畫面
        cv2.imshow('Camera', frame)

        # 監聽鍵盤輸入
        key = cv2.waitKey(1) & 0xFF

        if key == ord('q') or (cv2.getWindowProperty('Camera', cv2.WND_PROP_VISIBLE) >= 1 and key == ord('q')):
            # 按下 'q' 鍵退出
            msg="退出程式"
            print(msg)
            break
        elif key == ord('p') or (cv2.getWindowProperty('Camera', cv2.WND_PROP_VISIBLE) >= 1 and key == ord('p')):
            # 按下 'p' 鍵拍照
            photo_name = datetime.now().strftime('%Y%m%d%H%M%S') + '.jpg'
            photo_path = os.path.join(video_dir, photo_name)
            cv2.imwrite(photo_path, frame)
            msg = f"照片已儲存至 {photo_path}"
            print(msg)
        elif key == ord('r') or (cv2.getWindowProperty('Camera', cv2.WND_PROP_VISIBLE) >= 1 and key == ord('r')):
            # 按下 'r' 鍵開始錄影
            if not is_recording:
                video_name = datetime.now().strftime('%Y%m%d%H%M%S') + '.mp4'
                video_path = os.path.join(video_dir, video_name)
                fourcc = cv2.VideoWriter_fourcc(*'mp4v')
                out = cv2.VideoWriter(video_path, fourcc, 20.0, (frame.shape[1], frame.shape[0]))
                is_recording = True
                msg = f"開始錄影，影片將儲存至 {video_path}"
                print(msg)
                
        elif key == ord('s') or (cv2.getWindowProperty('Camera', cv2.WND_PROP_VISIBLE) >= 1 and key == ord('s')):
            # 按下 's' 鍵停止錄影
            if is_recording:
                is_recording = False
                out.release()
                msg="錄影已停止"
                print(msg)

        # 如果正在錄影，將畫面寫入影片
        if is_recording and out is not None:
            out.write(frame)

    # 釋放資源
    cap.release()
    if out is not None:
        out.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()