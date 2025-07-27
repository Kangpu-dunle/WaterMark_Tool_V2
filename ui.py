# ui.py
import os
import tkinter as tk
from tkinter import filedialog, colorchooser, messagebox, ttk
from PIL import ImageColor, Image, ImageTk, ImageDraw, ImageFont
from modules.image_previewer import ImagePreviewer
from pypinyin import lazy_pinyin
import math
import threading

class WatermarkApp(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.selected_files = []
        self.image_preview = None
        self.preview_canvas_img = None
        self.image_previewer = None
        self.font_path = None
        self.pinyin_sort_asc = True  # 排序标记
        self.final_watermarks = {}   # 存储加水印后的图

        self.init_ui()
        self.load_font()

    def load_font(self):
        try:
            possible_fonts = [
                "C:/Windows/Fonts/simhei.ttf",
                "C:/Windows/Fonts/simsun.ttc",
                "/System/Library/Fonts/STHeiti Medium.ttc",
                "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc"
            ]
            for font in possible_fonts:
                if os.path.exists(font):
                    self.font_path = font
                    return
            self.font_path = None
        except Exception as e:
            print(f"字体加载失败: {e}")
            self.font_path = None

    def init_ui(self):
        self.init_top_buttons()
        self.init_main_layout()
        self.init_bottom_controls()

    def init_top_buttons(self):
        top_frame = tk.Frame(self, height=40)
        top_frame.pack(side="top", fill="x", padx=5, pady=5)
        tk.Button(top_frame, text="📁 文件上传", command=self.upload_files).pack(side="left", padx=4)
        tk.Button(top_frame, text="📤 导出水印图", command=self.export_images).pack(side="left", padx=4)

    def init_main_layout(self):
        main_pane = tk.PanedWindow(self, orient=tk.HORIZONTAL, sashrelief=tk.RAISED)
        main_pane.pack(fill=tk.BOTH, expand=True)

        file_list_frame = tk.Frame(main_pane)
        header_frame = tk.Frame(file_list_frame)
        header_frame.pack(fill="x")
        header = tk.Label(header_frame, text="文件列表 (点击排序)", bg="lightgrey")
        header.pack(side="left", fill="x", expand=True)
        header.bind("<Button-1>", self.toggle_pinyin_sort)
        tk.Button(header_frame, text="全选", width=6, command=self.select_all).pack(side="right")
        tk.Button(header_frame, text="取消", width=6, command=self.clear_selection).pack(side="right")

        self.file_listbox = tk.Listbox(file_list_frame, width=30, selectmode=tk.MULTIPLE)
        self.file_listbox.pack(fill="both", expand=True)
        self.file_listbox.bind("<Double-Button-1>", self.on_file_select)
        self.file_list_footer = tk.Label(file_list_frame, text="一共 0 个文件", bg="lightgrey")
        self.file_list_footer.pack(fill="x")
        main_pane.add(file_list_frame)

        preview_pane = tk.PanedWindow(main_pane, orient=tk.VERTICAL, sashrelief=tk.RAISED)
        self.original_preview = tk.Canvas(preview_pane, bg="#f0f0f0")
        self.watermarked_preview = tk.Canvas(preview_pane, bg="#e0e0e0")
        preview_pane.add(self.original_preview)
        preview_pane.add(self.watermarked_preview)
        main_pane.add(preview_pane)

        self.image_previewer = ImagePreviewer(self.original_preview, self.watermarked_preview)
        self.image_previewer.bind_double_click_to_popup()

    def select_all(self):
        self.file_listbox.select_set(0, tk.END)

    def clear_selection(self):
        self.file_listbox.select_clear(0, tk.END)

    def init_bottom_controls(self):
        bottom_frame = tk.Frame(self, height=50)
        bottom_frame.pack(side="bottom", fill="x", padx=5, pady=5)

        tk.Label(bottom_frame, text="水印颜色:").pack(side="left")
        self.color_btn = tk.Button(bottom_frame, bg="red", width=3, command=self.choose_color)
        self.color_btn.pack(side="left", padx=4)

        tk.Label(bottom_frame, text="透明度:").pack(side="left")
        self.opacity_slider = tk.Scale(bottom_frame, from_=0, to=255, orient="horizontal")
        self.opacity_slider.set(128)
        self.opacity_slider.pack(side="left", padx=4)

        tk.Label(bottom_frame, text="字号:").pack(side="left")
        self.fontsize_slider = tk.Scale(bottom_frame, from_=10, to=300, orient="horizontal")
        self.fontsize_slider.set(48)
        self.fontsize_slider.pack(side="left", padx=4)

        tk.Label(bottom_frame, text="间距倍数:").pack(side="left")
        self.spacing_slider = tk.Scale(bottom_frame, from_=100, to=300, orient="horizontal")
        self.spacing_slider.set(150)
        self.spacing_slider.pack(side="left", padx=4)

        tk.Label(bottom_frame, text="倾斜角度:").pack(side="left")
        self.angle_slider = tk.Scale(bottom_frame, from_=-90, to=90, orient="horizontal")
        self.angle_slider.set(45)
        self.angle_slider.pack(side="left", padx=4)

        tk.Label(bottom_frame, text="水印文字:").pack(side="left")
        self.watermark_entry = tk.Entry(bottom_frame, width=30)
        self.watermark_entry.pack(side="left", padx=4)

        tk.Button(bottom_frame, text="预览水印", command=self.preview_watermark).pack(side="left", padx=8)
        tk.Button(bottom_frame, text="确认添加", command=self.apply_watermark).pack(side="left", padx=4)

    def toggle_pinyin_sort(self, event=None):
        files = self.selected_files.copy()
        files.sort(key=lambda name: lazy_pinyin(os.path.basename(name)), reverse=not self.pinyin_sort_asc)
        self.selected_files = files
        self.pinyin_sort_asc = not self.pinyin_sort_asc
        self.refresh_file_list()

    def upload_files(self):
        files = filedialog.askopenfilenames(filetypes=[("Image files", "*.png *.jpg *.jpeg *.webp *.bmp")])
        if files:
            self.selected_files = list(files)
            self.refresh_file_list()

    def refresh_file_list(self):
        self.file_listbox.delete(0, tk.END)
        for file in self.selected_files:
            self.file_listbox.insert(tk.END, os.path.basename(file))
        self.file_list_footer.config(text=f"一共 {len(self.selected_files)} 个文件")

    def on_file_select(self, event):
        index = self.file_listbox.curselection()
        if not index:
            return
        file_path = self.selected_files[index[0]]
        self.show_preview(file_path)

    def show_preview(self, file_path):
        try:
            img = Image.open(file_path)
            self.image_preview = img
            self.image_previewer.update_preview(img, None)
        except Exception as e:
            messagebox.showerror("预览错误", str(e))

    def choose_color(self):
        color = colorchooser.askcolor()[1]
        if color:
            self.color_btn.config(bg=color)

    def create_watermark(self, img, text, color, opacity, font_size, spacing_ratio=1.5, angle=30):
        try:
            watermark = Image.new("RGBA", img.size, (0, 0, 0, 0))
            draw = ImageDraw.Draw(watermark)
            font = ImageFont.truetype(self.font_path, font_size) if self.font_path else ImageFont.load_default()
            text_bbox = draw.textbbox((0, 0), text, font=font)
            text_width = text_bbox[2] - text_bbox[0]
            text_height = text_bbox[3] - text_bbox[1]

            spacing_x = int(max(text_width + 20, text_width * spacing_ratio * self.spacing_slider.get() / 100))
            spacing_y = int(max(text_height + 20, text_height * spacing_ratio * self.spacing_slider.get() / 100))

            r, g, b = self.hex_to_rgb(color)
            fill_color = (r, g, b, opacity)

            tile = Image.new("RGBA", (spacing_x, spacing_y), (0, 0, 0, 0))
            tile_draw = ImageDraw.Draw(tile)
            tile_draw.text((0, 0), text, font=font, fill=fill_color)
            tile = tile.rotate(angle, expand=True, resample=Image.BICUBIC)

            for y in range(-img.height // 2, int(img.height * 1.2), spacing_y):
                for x in range(-img.width // 2, int(img.width * 1.2), spacing_x):
                    watermark.paste(tile, (x, y), tile)

            return watermark
        except Exception as e:
            print(f"创建水印失败: {e}")
            return None

    def preview_watermark(self):
        index = self.file_listbox.curselection()
        if not index:
            messagebox.showinfo("提示", "请先双击左侧列表选择图片")
            return
        path = self.selected_files[index[0]]
        img = Image.open(path).convert("RGBA")
        text = self.watermark_entry.get()
        color = self.color_btn.cget("bg")
        opacity = self.opacity_slider.get()
        font_size = self.fontsize_slider.get()
        angle = self.angle_slider.get()
        spacing = self.spacing_slider.get()
        watermark = self.create_watermark(img, text, color, opacity, font_size, spacing_ratio=spacing / 100, angle=angle)

        if watermark:
            watermarked = Image.alpha_composite(img, watermark).convert("RGB")
            self.final_watermarks[path] = watermarked
            self.image_previewer.update_preview(img, watermarked)  # ← 只在成功后调用

    def apply_watermark(self):
        self.final_watermarks = {}
        indices = self.file_listbox.curselection()
        if not indices:
            messagebox.showinfo("提示", "请至少选择一张图片")
            return
        text = self.watermark_entry.get()
        color = self.color_btn.cget("bg")
        opacity = self.opacity_slider.get()
        font_size = self.fontsize_slider.get()
        angle = self.angle_slider.get()
        spacing = self.spacing_slider.get()
        for i in indices:
            path = self.selected_files[i]
            img = Image.open(path).convert("RGBA")
            watermark = self.create_watermark(img, text, color, opacity, font_size, spacing_ratio=spacing / 100, angle=angle)
            if watermark:
                watermarked = Image.alpha_composite(img, watermark).convert("RGB")
                self.final_watermarks[path] = watermarked
        if indices:
            self.image_previewer.update_preview(img, watermarked)
        messagebox.showinfo("成功", "水印已成功添加")

    def export_images(self):
        if not self.final_watermarks:
            messagebox.showinfo("提示", "请先添加水印")
            return
        output_dir = filedialog.askdirectory(title="选择导出目录")
        if not output_dir:
            return

        def do_export():
            progress = tk.Toplevel(self)
            progress.title("正在导出")
            tk.Label(progress, text="导出进度：").pack(padx=10, pady=5)
            pbar = ttk.Progressbar(progress, orient="horizontal", length=300, mode="determinate")
            pbar.pack(padx=10, pady=10)
            pbar["maximum"] = len(self.final_watermarks)

            try:
                for i, (path, img) in enumerate(self.final_watermarks.items()):
                    filename = os.path.basename(path)
                    output_path = os.path.join(output_dir, filename)
                    img.convert("RGB").save(output_path)
                    pbar["value"] = i + 1
                    progress.update()
                progress.destroy()
                messagebox.showinfo("成功", f"已导出 {len(self.final_watermarks)} 张水印图到 {output_dir}")
            except Exception as e:
                progress.destroy()
                messagebox.showerror("导出失败", str(e))

        threading.Thread(target=do_export).start()

    @staticmethod
    def hex_to_rgb(color_str):
        try:
            return ImageColor.getrgb(color_str)
        except Exception as e:
            print(f"[颜色解析错误] {color_str} → {e}")
            return (255, 0, 0)
