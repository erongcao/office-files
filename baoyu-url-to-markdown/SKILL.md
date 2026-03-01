---
name: baoyu-url-to-markdown
description: 抓取网页并转换为 Markdown 格式。支持静态页面和需要登录的动态页面。
triggers:
  - 网页转markdown
  - 抓取网页
  - 保存网页
  - url转markdown
---

# URL to Markdown 工具

基于宝玉的 baoyu-url-to-markdown 技能改编。

## 功能

- 抓取网页内容并转换为 Markdown
- 支持静态页面和动态内容
- 保留文章结构（标题、段落、列表等）

## 安装依赖

```bash
pip install requests beautifulsoup4 html2text
```

## 使用方法

```python
from skills.baoyu-url-to-markdown.converter import UrlToMarkdown

converter = UrlToMarkdown()
md_content = converter.convert('https://example.com/article')
```

或命令行：

```bash
python skills/baoyu-url-to-markdown/scripts/convert.py https://example.com/article -o output.md
```

## 支持的模式

| 模式 | 说明 | 适用场景 |
|------|------|----------|
| 自动（默认） | 页面加载后立即抓取 | 公开页面、静态内容 |
| 等待模式 | 等待用户信号后抓取 | 需登录页面、动态内容 |

## 选项

| 选项 | 说明 |
|------|------|
| `<url>` | 要抓取的 URL |
| `-o <path>` | 输出文件路径 |
| `--wait` | 等待用户信号后抓取 |
