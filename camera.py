import cv2
import os
from datetime import datetime

def main():
    # 創建存放影片的資料夾
    video_dir = os.path.join('demo', 'videos')
    os.makedirs(video_dir, exist_ok=True)

    # 初始化攝影機
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("無法開啟攝影機")
        return

    # 初始化錄影相關變數
    is_recording = False
    out = None

    while True:
        ret, frame = cap.read()
        if not ret:
            print("無法讀取攝影機畫面")
            break

        # 顯示攝影機畫面
        cv2.imshow('Camera', frame)

        # 監聽鍵盤輸入
        key = cv2.waitKey(1) & 0xFF

        if key == ord('q'):
            # 按下 'q' 鍵退出
            break
        elif key == ord('p'):
            # 按下 'p' 鍵拍照
            photo_name = datetime.now().strftime('%Y%m%d%H%M%S') + '.jpg'
            photo_path = os.path.join(video_dir, photo_name)
            cv2.imwrite(photo_path, frame)
            print(f"照片已儲存至 {photo_path}")
        elif key == ord('r'):
            # 按下 'r' 鍵開始錄影
            if not is_recording:
                video_name = datetime.now().strftime('%Y%m%d%H%M%S') + '.mp4'
                video_path = os.path.join(video_dir, video_name)
                fourcc = cv2.VideoWriter_fourcc(*'mp4v')
                out = cv2.VideoWriter(video_path, fourcc, 20.0, (frame.shape[1], frame.shape[0]))
                is_recording = True
                print(f"開始錄影，影片將儲存至 {video_path}")
        elif key == ord('s'):
            # 按下 's' 鍵停止錄影
            if is_recording:
                is_recording = False
                out.release()
                print("錄影已停止")

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
