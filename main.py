# main.py
import tkinter as tk
from ui import WatermarkApp

def main():
    root = tk.Tk()
    root.title("水印图片批处理工具 V2.0")
    root.geometry("1280x800")
    root.minsize(1024, 640)

    app = WatermarkApp(root)
    app.pack(fill="both", expand=True)

    root.mainloop()

if __name__ == '__main__':
    main()