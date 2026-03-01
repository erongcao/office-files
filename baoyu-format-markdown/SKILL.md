---
name: baoyu-format-markdown
description: 格式化 Markdown 文件，添加 frontmatter、标题、摘要、层级标题、加粗、列表和代码块。自动处理中英文间距、全角引号等排版细节。
triggers:
  - 格式化markdown
  - 排版文章
  - 美化文章
  - 中文排版
---

# Markdown 格式化工具

基于宝玉的 baoyu-format-markdown 技能改编，用 Python 实现。

## 功能

1. **添加 YAML Frontmatter** - title、slug、summary、coverImage
2. **格式化内容** - 层级标题、加粗、列表、代码块
3. **中文排版优化** - 中英文间距、全角引号、标点符号

## 安装依赖

```bash
pip install pyyaml
```

## 使用方法

```python
from skills.baoyu-format-markdown.formatter import MarkdownFormatter

formatter = MarkdownFormatter()
result = formatter.format_file('article.md')
# 输出到 article-formatted.md
```

或直接运行脚本：

```bash
python skills/baoyu-format-markdown/scripts/format.py article.md
```

## 格式化规则

| 元素 | 格式 |
|------|------|
| 标题 | `#`、`##`、`###` 层级 |
| 重点内容 | `**加粗**` |
| 并列要点 | `-` 无序列表或 `1.` 有序列表 |
| 代码/命令 | `` `行内` `` 或 ` ```代码块``` ` |
| 引用 | `>` 引用块 |

## 中文排版优化

- ASCII 引号 `"` `'` → 全角引号 `"` `'`
- 中英文之间自动添加空格
- 中文标点符号规范化

## Frontmatter 字段

| 字段 | 处理方式 |
|------|----------|
| `title` | 使用现有、提取 H1 或生成候选 |
| `slug` | 从文件路径推断或根据标题生成 |
| `summary` | 生成吸引人的摘要（100-150 字）|
| `coverImage` | 检查同目录下 `imgs/cover.png` |
