import tkinter as tk
from tkinter import messagebox

def on_hello_button_click():
    """按下按鈕時顯示提示框"""
    messagebox.showinfo("提示", "Hello")

def main():
    """主函式，建立視窗應用程式"""
    # 建立主視窗
    root = tk.Tk()
    root.title("簡單視窗應用程式")
    root.geometry("300x200")

    # 建立按鈕
    hello_button = tk.Button(root, text="Hello", command=on_hello_button_click)
    hello_button.pack(pady=20)

    # 啟動主迴圈
    root.mainloop()

if __name__ == "__main__":
    main()
