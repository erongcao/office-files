---
name: baoyu-post-to-wechat
description: 发布内容到微信公众号。支持 Markdown 转公众号 HTML、准备发布元数据、通过 API 或浏览器方式发布。
triggers:
  - 发布公众号
  - 微信公众号
  - 公众号文章
  - 贴图
  - 图文
  - 发公众号
---

# 微信公众号发布工具

基于宝玉的 baoyu-post-to-wechat 技能改编，用 Python 实现。

## 功能

1. **Markdown 转公众号 HTML** - 转换为微信支持的格式
2. **准备发布数据** - 标题、封面图、摘要等
3. **API 发布** - 通过微信公众号 API 发布
4. **浏览器发布** - 生成内容用于手动复制粘贴

## 前置要求

### 方式一：API 发布（推荐）

需要在 `.baoyu-skills/.env` 中配置：

```
WECHAT_APP_ID=你的AppID
WECHAT_APP_SECRET=你的AppSecret
```

获取方式：
1. 登录 https://mp.weixin.qq.com
2. 开发 → 基本配置 → 复制 AppID 和 AppSecret

### 方式二：浏览器发布

需要登录微信公众号后台，手动复制粘贴内容。

## 安装依赖

```bash
pip install requests pyyaml markdown
```

## 使用方法

### 1. Markdown 转公众号 HTML

```bash
python baoyu-post-to-wechat/scripts/convert.py article.md -o article_wechat.html
```

转换特性：
- 保留标题层级
- 图片自动添加微信样式
- 代码块格式化
- 引用块样式

### 2. 准备发布

```bash
python baoyu-post-to-wechat/scripts/publish.py article.md --title "文章标题" --cover cover.jpg
```

### 3. 通过 API 发布

```bash
# 先设置环境变量
export WECHAT_APP_ID=你的AppID
export WECHAT_APP_SECRET=你的AppSecret

# 发布
python baoyu-post-to-wechat/scripts/publish.py article.md --method api --publish
```

### 4. 仅生成发布数据

```bash
python baoyu-post-to-wechat/scripts/publish.py article.md --method browser
# 输出用于手动复制的内容
```

## Frontmatter 支持

文章支持 YAML frontmatter：

```yaml
---
title: 文章标题
author: 作者名
cover: ./cover.jpg
summary: 文章摘要
---
```

## 注意事项

- 微信公众号需要认证后才能使用 API
- 未认证账号只能使用浏览器方式手动发布
- 图片需要先上传到微信服务器获取 URL
