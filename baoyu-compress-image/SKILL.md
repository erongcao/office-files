---
name: baoyu-compress-image
description: 压缩图片以减小文件大小，同时保持质量。支持批量处理和自定义压缩质量。
triggers:
  - 压缩图片
  - 图片压缩
  - 减小图片大小
  - 优化图片
---

# 图片压缩工具

基于宝玉的 baoyu-compress-image 技能改编。

## 功能

- 压缩 JPG/PNG/WebP 图片
- 批量处理目录
- 自定义压缩质量
- 保持原图比例

## 安装依赖

```bash
pip install Pillow
```

## 使用方法

```bash
# 压缩单张图片
python skills/baoyu-compress-image/scripts/compress.py image.png

# 指定质量
python skills/baoyu-compress-image/scripts/compress.py image.png --quality 80

# 批量压缩目录
python skills/baoyu-compress-image/scripts/compress.py ./images/ --quality 85
```

## 参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `path` | 图片路径或目录 | - |
| `--quality` | 压缩质量 (1-100) | 85 |
| `--output` | 输出路径 | 原文件名-compressed |
| `--max-width` | 最大宽度 | 原尺寸 |
| `--max-height` | 最大高度 | 原尺寸 |
