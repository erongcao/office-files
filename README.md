# 宝玉技能集 - OpenClaw 适配版

基于 [JimLiu/baoyu-skills](https://github.com/JimLiu/baoyu-skills) 改编，用 Python 实现，适用于 OpenClaw 环境。

## 已适配技能 (5个)

| 技能 | 用途 | 原始技能 |
|------|------|----------|
| **baoyu-format-markdown** | Markdown 格式化 + 中文排版 | ✓ 完整适配 |
| **baoyu-url-to-markdown** | 网页转 Markdown | ✓ 完整适配 |
| **baoyu-compress-image** | 图片压缩 | ✓ 完整适配 |
| **baoyu-xhs-images** | 小红书信息图生成 | ⚠️ 简化版（生成提示词） |
| **baoyu-post-to-wechat** | 微信公众号发布 | ⚠️ 简化版（API + 浏览器） |

## 快速开始

### 安装依赖

```bash
# Markdown 格式化
pip install pyyaml

# URL 转 Markdown
pip install requests beautifulsoup4 html2text

# 图片压缩
pip install Pillow

# 公众号发布
pip install requests pyyaml markdown
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

#### 5. 微信公众号发布

```bash
# 方式一：转换为公众号 HTML
python baoyu-post-to-wechat/scripts/convert.py article.md -o article.html

# 方式二：浏览器发布（推荐）
python baoyu-post-to-wechat/scripts/publish.py article.md --method browser
# 生成 HTML，手动复制到公众号后台

# 方式三：API 发布（需要配置 AppID/AppSecret）
export WECHAT_APP_ID=你的AppID
export WECHAT_APP_SECRET=你的AppSecret
python baoyu-post-to-wechat/scripts/publish.py article.md --method api
```

微信公众号发布功能：
- Markdown 转公众号 HTML（自动处理样式）
- 支持 frontmatter（title、author、cover、summary）
- API 发布（需要认证公众号）
- 浏览器发布（手动复制粘贴）

## 与原版对比

| 特性 | 原版 (Claude Code) | OpenClaw 版 |
|------|-------------------|-------------|
| 运行环境 | Bun/Node.js | Python 3 |
| 安装方式 | `/plugin install` | 直接运行脚本 |
| 图片生成 | 内置集成 | 生成提示词 |
| 公众号发布 | 浏览器自动化 | API + 手动 |
| 可修改 | ❌ | ✅ |
| 依赖 | 复杂 | 简单 |

## 待适配技能

- baoyu-image-gen - 需要图像生成 API 集成
- baoyu-danger-x-to-markdown - 需要 X API 认证
- baoyu-slide-deck - PPT 生成，可用 office-pptx 替代

## 许可证

与原项目一致，遵循 MIT 许可证。

原始项目: https://github.com/JimLiu/baoyu-skills
