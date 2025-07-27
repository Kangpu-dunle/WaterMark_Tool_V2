# modules/config_manager.py

import json
import os

class ConfigManager:
    """
    用于加载与保存用户配置，包括字体、字号、颜色、透明度、水印内容等。
    """

    def __init__(self, config_path="user_config.json"):
        self.config_path = config_path
        self.default_config = {
            "font_path": "assets/fonts/NotoSansSC-VariableFont_wght.ttf",
            "font_size": 36,
            "watermark_text": "示例水印",
            "color": "#FF0000",
            "opacity": 180,
            "spacing": 100,
            "angle": 0
        }
        self.config = self.load_config()

    def load_config(self):
        """加载配置，如果不存在则使用默认配置"""
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    config = json.load(f)
                    return {**self.default_config, **config}  # 合并默认配置
            except Exception as e:
                print(f"[配置加载失败] 使用默认配置: {e}")
        return self.default_config.copy()

    def save_config(self):
        """保存当前配置到文件"""
        try:
            with open(self.config_path, "w", encoding="utf-8") as f:
                json.dump(self.config, f, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"[配置保存失败] {e}")
            return False

    def update_config(self, key, value):
        """更新配置项并立即保存"""
        self.config[key] = value
        self.save_config()

    def get(self, key):
        """获取配置项"""
        return self.config.get(key, self.default_config.get(key))

    def reset_to_default(self):
        """重置配置为默认值"""
        self.config = self.default_config.copy()
        self.save_config()
