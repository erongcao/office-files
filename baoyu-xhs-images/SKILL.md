---
name: baoyu-xhs-images
description: 生成小红书风格的信息图系列。将内容拆解为 1-10 张图片，支持多种风格和布局组合。
triggers:
  - 小红书图片
  - xhs图片
  - 信息图
  - 小红书风格
  - 社交媒体配图
---

# 小红书信息图生成器

基于宝玉的 baoyu-xhs-images 技能改编。

## 功能

- 将长文内容拆解为多张信息图
- 支持 10 种视觉风格 × 8 种布局组合
- 自动优化文字排版和视觉层次

## 风格选择

| 风格 | 描述 |
|------|------|
| cute | 甜美可爱，经典小红书风格 |
| fresh | 清新自然 |
| warm | 温馨亲切 |
| bold | 高冲击力，吸引眼球 |
| minimal | 极简精致 |
| retro | 复古怀旧 |
| pop | 活力四射 |
| notion | 手绘线稿，知性风格 |
| chalkboard | 黑板彩色粉笔风格 |
| study-notes | 真实手写笔记风格 |

## 布局选择

| 布局 | 描述 |
|------|------|
| sparse | 极简信息，1-2个要点 |
| balanced | 标准布局，3-4个要点 |
| dense | 高信息密度，知识卡片风格 |
| list | 列表枚举格式 |
| comparison | 并排对比布局 |
| flow | 流程时间线布局 |
| mindmap | 中心放射思维导图 |
| quadrant | 四象限布局 |

## 使用方法

```bash
# 从文件生成
python skills/baoyu-xhs-images/scripts/generate.py article.md

# 指定风格和布局
python skills/baoyu-xhs-images/scripts/generate.py article.md --style notion --layout dense

# 限制图片数量
python skills/baoyu-xhs-images/scripts/generate.py article.md --max-images 5
```

## 输出

生成图片保存在 `output/<timestamp>/` 目录下，包含：
- `cover.png` - 封面图
- `page_01.png` ~ `page_N.png` - 内容页
- `prompts.json` - 使用的提示词记录

## 依赖

需要配合图像生成工具使用：
- Coze Image Gen
- DALL-E
- Midjourney API
- 或其他图像生成服务
