# 🖼️ WaterMark Tool V2 - 本地图像批量加水印工具
# 🖼️ WaterMark Tool V2 - 图像批量加水印工具

> 本项目是一个基于 Python + Tkinter + Pillow 的本地图像批处理工具，支持批量添加文本水印、图片预览、导出保存等操作。适用于电商卖家、自媒体创作者、摄影工作者在本地对大量图片进行快速加水印处理，无需联网，绿色安全。

本工具支持以下功能：

- ✅ 支持批量导入 PNG/JPG 图片
- ✅ 支持中文水印文字（默认使用开源字体 NotoSansSC）
- ✅ 支持原图与加水印图实时预览
- ✅ 支持缩放适配画布自动居中显示
- ✅ 一键导出所有带水印图片至指定目录
- ✅ 所有处理均为本地离线执行，保障隐私与安全

## 🗂️ 项目结构

WaterMark_Tool_V2/
├── assets/ # 静态资源目录（字体、图标等）
│ └── fonts/
│ └── static/ # 字体文件（如 NotoSansSC）
│ ├── NotoSansSC-VariableFont_wght.ttf
│ ├── OFL.txt
│ └── README.txt
├── modules/ # 核心功能模块
│ ├── config_manager.py # 配置管理（字体、默认参数）
│ ├── exporter.py # 图片导出模块（含压缩/保存）
│ ├── file_loader.py # 文件批量加载器
│ └── image_previewer.py # 图像预览模块（原图与水印图）
├── 导出文件/ # 水印生成图片的默认导出目录
├── main.py # 主程序入口（含 UI 控制）
├── README.md # 本文件（项目说明）
├── test001.png ~ test007.png# 示例测试图片

---

## 🖥️ 项目界面预览

| 启动界面 | 水印预览 |
|----------|-----------|
| ![界面预览](./test001.png) | ![处理效果](./test003.png) |

（*你可上传图片到 GitHub，再替换为链接*）

---

## 🔧 安装运行说明

### ✅ 环境要求

- Python 3.8+
- 推荐虚拟环境中使用

### ✅ 安装依赖

```bash
pip install -r requirements.txt
若无 requirements.txt，可参考以下手动安装：
pip install pillow
✅ 运行方式
python main.py
程序会自动打开图形界面，点击按钮即可选择文件、查看预览、批量导出。

💾 功能说明
预览功能：原图 & 加水印图实时对比显示；

字体管理：默认使用 assets/fonts/static/NotoSansSC 中文字体，可替换；

导出路径：默认保存到 导出文件/ 文件夹中；

支持格式：PNG、JPG，自动保持原图比例；

异常处理：支持空图检测、尺寸校准、异常提示弹窗。
🔐 隐私与安全
本工具为完全离线运行；

所有图像处理在本地进行，不涉及云端上传；

安全可靠，适用于企业或私密环境。

