# 宝玉技能集 - OpenClaw 适配版

基于 [JimLiu/baoyu-skills](https://github.com/JimLiu/baoyu-skills) 改编，用 Python 实现，适用于 OpenClaw 环境。

## 已适配技能

| 技能 | 用途 | 原始技能 |
|------|------|----------|
| **baoyu-format-markdown** | Markdown 格式化 + 中文排版 | ✓ 完整适配 |
| **baoyu-url-to-markdown** | 网页转 Markdown | ✓ 完整适配 |
| **baoyu-compress-image** | 图片压缩 | ✓ 完整适配 |
| **baoyu-xhs-images** | 小红书信息图生成 | ⚠️ 简化版（生成提示词） |

## 快速开始

### 安装依赖

```bash
# Markdown 格式化
pip install pyyaml

# URL 转 Markdown
pip install requests beautifulsoup4 html2text

# 图片压缩
pip install Pillow
```

### 使用示例

#### 1. Markdown 格式化

```bash
python baoyu-format-markdown/scripts/format.py article.md
# 输出: article-formatted.md
```

功能：
- 自动添加 YAML frontmatter（title、slug、summary）
- 中英文之间自动加空格
- ASCII 引号转全角引号
- 规范化标题层级

#### 2. 网页转 Markdown

```bash
python baoyu-url-to-markdown/scripts/convert.py https://example.com/article -o output.md
```

#### 3. 图片压缩

```bash
# 单张图片
python baoyu-compress-image/scripts/compress.py image.png --quality 85

# 批量压缩
python baoyu-compress-image/scripts/compress.py ./images/ --quality 80
```

#### 4. 小红书信息图

```bash
python baoyu-xhs-images/scripts/generate.py article.md --style notion --layout dense
```

生成图像生成提示词，复制到 DALL-E/Midjourney 使用。

## 与原版对比

| 特性 | 原版 (Claude Code) | OpenClaw 版 |
|------|-------------------|-------------|
| 运行环境 | Bun/Node.js | Python 3 |
| 安装方式 | `/plugin install` | 直接运行脚本 |
| 图片生成 | 内置集成 | 生成提示词 |
| 可修改 | ❌ | ✅ |
| 依赖 | 复杂 | 简单 |

## 待适配技能

- baoyu-image-gen - 需要图像生成 API 集成
- baoyu-post-to-wechat - 需要微信公众号 API
- baoyu-slide-deck - PPT 生成，可用 office-pptx 替代
- baoyu-danger-x-to-markdown - 需要 X API 认证

## 许可证

与原项目一致，遵循 MIT 许可证。

原始项目: https://github.com/JimLiu/baoyu-skills
