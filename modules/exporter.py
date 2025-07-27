# modules/exporter.py

import os
from PIL import Image

class Exporter:
    """
    图像导出模块：负责将图像统一保存到目标目录，可自定义格式和重命名策略。
    """

    def __init__(self, export_config):
        """
        :param export_config: dict 配置项，如 { output_dir: "", format: "png", overwrite: False }
        """
        self.config = export_config

    def export_images(self, image_list, filename_list):
        """
        将图像对象列表导出为指定目录文件
        :param image_list: PIL.Image 对象列表
        :param filename_list: 对应输出文件名列表（不含路径）
        :return: 成功保存的路径列表
        """
        saved_paths = []

        for img, name in zip(image_list, filename_list):
            try:
                ext = self.config.get("format", "png").lower()
                out_dir = self.config.get("output_dir", "./output")
                overwrite = self.config.get("overwrite", False)

                # 确保目录存在
                os.makedirs(out_dir, exist_ok=True)

                # 修改扩展名
                filename_base, _ = os.path.splitext(name)
                out_path = os.path.join(out_dir, f"{filename_base}.{ext}")

                # 若文件已存在且不允许覆盖，则重命名保存
                if os.path.exists(out_path) and not overwrite:
                    count = 1
                    while True:
                        new_name = f"{filename_base}_{count}.{ext}"
                        out_path = os.path.join(out_dir, new_name)
                        if not os.path.exists(out_path):
                            break
                        count += 1

                img.save(out_path, format=ext.upper())
                saved_paths.append(out_path)

            except Exception as e:
                print(f"[导出失败] {name} -> {e}")

        return saved_paths
