# file_loader.py
import os
from PIL import Image

class FileLoader:
    def __init__(self):
        self.loaded_images = []  # 存储 (文件路径, 原始图像, 应用水印后的图像)

    def load_images_from_paths(self, file_paths):
        self.loaded_images.clear()
        for path in file_paths:
            if os.path.isfile(path) and path.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')):
                try:
                    image = Image.open(path).convert("RGBA")
                    self.loaded_images.append((path, image, None))
                except Exception as e:
                    print(f"[加载失败] {path}: {e}")
        return self.loaded_images

    def apply_watermarks(self, watermark_function):
        updated = []
        for i, (path, original_img, _) in enumerate(self.loaded_images):
            try:
                watermarked = watermark_function(original_img)
                updated.append((path, original_img, watermarked))
            except Exception as e:
                print(f"[水印处理失败] {path}: {e}")
                updated.append((path, original_img, None))
        self.loaded_images = updated
        return updated

    def get_file_names(self):
        return [os.path.basename(p) for p, _, _ in self.loaded_images]

    def get_original_image_by_index(self, index):
        return self.loaded_images[index][1] if 0 <= index < len(self.loaded_images) else None

    def get_watermarked_image_by_index(self, index):
        return self.loaded_images[index][2] if 0 <= index < len(self.loaded_images) else None

    def get_file_path_by_index(self, index):
        return self.loaded_images[index][0] if 0 <= index < len(self.loaded_images) else ""

    def has_watermarked_images(self):
        return any(w is not None for _, _, w in self.loaded_images)

    def clear(self):
        self.loaded_images.clear()
