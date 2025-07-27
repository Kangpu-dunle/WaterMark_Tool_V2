# image_previewer.py
from PIL import Image, ImageTk
#from PIL import Image, ImageTk, ImageResampling  # ✅ 加入这个 import
class ImagePreviewer:
    def __init__(self, original_canvas, watermarked_canvas):
        self.original_canvas = original_canvas
        self.watermarked_canvas = watermarked_canvas
        self.original_image_on_canvas = None
        self.watermarked_image_on_canvas = None

    def update_preview(self, original_img, watermarked_img):
        if original_img:
            self._show_image_on_canvas(original_img, self.original_canvas, is_watermarked=False)
        if watermarked_img:
            self._show_image_on_canvas(watermarked_img, self.watermarked_canvas, is_watermarked=True)

    def _show_image_on_canvas(self, img, canvas, is_watermarked):
        canvas.delete("all")
        canvas_width = canvas.winfo_width()
        canvas_height = canvas.winfo_height()
        if canvas_width <= 1 or canvas_height <= 1:
            canvas.update()
            canvas_width = canvas.winfo_width()
            canvas_height = canvas.winfo_height()

        img_ratio = img.width / img.height
        canvas_ratio = canvas_width / canvas_height

        if img_ratio > canvas_ratio:
            new_width = canvas_width
            new_height = int(canvas_width / img_ratio)
        else:
            new_height = canvas_height
            new_width = int(canvas_height * img_ratio)
        resized = img.resize((new_width, new_height), Image.LANCZOS)

        #resized = img.resize((new_width, new_height), ImageResampling.LANCZOS)
        tk_img = ImageTk.PhotoImage(resized)
        canvas.create_image(canvas_width // 2, canvas_height // 2, image=tk_img, anchor="center")

        if is_watermarked:
            self.watermarked_image_on_canvas = tk_img
        else:
            self.original_image_on_canvas = tk_img

    def bind_double_click_to_popup(self):
        def show_popup(event, is_watermarked):
            img = self.watermarked_image_on_canvas if is_watermarked else self.original_image_on_canvas
            if img:
                popup = tk.Toplevel()
                popup.title("查看大图")
                label = tk.Label(popup, image=img)
                label.image = img
                label.pack()
        self.original_canvas.bind("<Double-Button-1>", lambda e: show_popup(e, False))
        self.watermarked_canvas.bind("<Double-Button-1>", lambda e: show_popup(e, True))
