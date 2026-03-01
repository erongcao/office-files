#!/usr/bin/env python3
"""
Markdown 转微信公众号 HTML
改编自 baoyu-post-to-wechat
"""

import re
import sys
import argparse
from pathlib import Path


def markdown_to_wechat_html(markdown_text: str) -> str:
    """将 Markdown 转换为微信公众号 HTML"""
    
    html = markdown_text
    
    # 转义 HTML 特殊字符（代码块内的稍后处理）
    # 先保存代码块
    code_blocks = []
    def save_code_block(match):
        lang = match.group(1) or ''
        code = match.group(2)
        code_blocks.append((lang, code))
        return f'<!--CODEBLOCK{len(code_blocks)-1}-->'
    
    html = re.sub(r'```(\w*)?\n(.*?)```', save_code_block, html, flags=re.DOTALL)
    
    # 转义 HTML
    html = html.replace('&', '&amp;')
    html = html.replace('<', '&lt;')
    html = html.replace('>', '&gt;')
    
    # 恢复代码块并格式化
    for i, (lang, code) in enumerate(code_blocks):
        escaped_code = code.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        formatted_code = f'''<pre style="background-color: #f5f5f5; padding: 12px; border-radius: 4px; overflow-x: auto; font-family: monospace; font-size: 14px; line-height: 1.5; color: #333;">
<code>{escaped_code}</code>
</pre>'''
        html = html.replace(f'<!--CODEBLOCK{i}-->', formatted_code)
    
    # 标题
    html = re.sub(r'^###### (.*?)$', r'<h6 style="font-size: 14px; font-weight: bold; margin: 16px 0 8px; color: #333;">\1</h6>', html, flags=re.MULTILINE)
    html = re.sub(r'^##### (.*?)$', r'<h5 style="font-size: 15px; font-weight: bold; margin: 18px 0 9px; color: #333;">\1</h5>', html, flags=re.MULTILINE)
    html = re.sub(r'^#### (.*?)$', r'<h4 style="font-size: 16px; font-weight: bold; margin: 20px 0 10px; color: #333;">\1</h4>', html, flags=re.MULTILINE)
    html = re.sub(r'^### (.*?)$', r'<h3 style="font-size: 17px; font-weight: bold; margin: 22px 0 11px; color: #333;">\1</h3>', html, flags=re.MULTILINE)
    html = re.sub(r'^## (.*?)$', r'<h2 style="font-size: 19px; font-weight: bold; margin: 24px 0 12px; color: #333; border-bottom: 1px solid #eee; padding-bottom: 8px;">\1</h2>', html, flags=re.MULTILINE)
    html = re.sub(r'^# (.*?)$', r'<h1 style="font-size: 22px; font-weight: bold; margin: 28px 0 14px; color: #333; text-align: center;">\1</h1>', html, flags=re.MULTILINE)
    
    # 粗体
    html = re.sub(r'\*\*(.*?)\*\*', r'<strong style="font-weight: bold;">\1</strong>', html)
    html = re.sub(r'__(.*?)__', r'<strong style="font-weight: bold;">\1</strong>', html)
    
    # 斜体
    html = re.sub(r'\*(.*?)\*', r'<em style="font-style: italic;">\1</em>', html)
    html = re.sub(r'_(.*?)_', r'<em style="font-style: italic;">\1</em>', html)
    
    # 删除线
    html = re.sub(r'~~(.*?)~~', r'<span style="text-decoration: line-through;">\1</span>', html)
    
    # 行内代码
    html = re.sub(r'`([^`]+)`', r'<code style="background-color: #f0f0f0; padding: 2px 6px; border-radius: 3px; font-family: monospace; font-size: 14px; color: #c7254e;">\1</code>', html)
    
    # 图片
    html = re.sub(r'!\[([^\]]*)\]\(([^\)]+)\)', 
                  r'<img src="\2" alt="\1" style="max-width: 100%; height: auto; display: block; margin: 16px auto; border-radius: 4px;">', html)
    
    # 链接
    html = re.sub(r'\[([^\]]+)\]\(([^\)]+)\)', 
                  r'<a href="\2" style="color: #576b95; text-decoration: none;">\1</a>', html)
    
    # 无序列表
    def format_ul(match):
        items = match.group(0)
        item_list = re.findall(r'^[\*\-] (.+)$', items, re.MULTILINE)
        li_html = ''.join([f'<li style="margin: 8px 0; line-height: 1.6;">{item}</li>' for item in item_list])
        return f'<ul style="margin: 12px 0; padding-left: 24px;">{li_html}</ul>'
    
    # 处理连续的无序列表项
    html = re.sub(r'((?:^[\*\-] .+\n?)+)', format_ul, html, flags=re.MULTILINE)
    
    # 有序列表
    def format_ol(match):
        items = match.group(0)
        item_list = re.findall(r'^\d+\. (.+)$', items, re.MULTILINE)
        li_html = ''.join([f'<li style="margin: 8px 0; line-height: 1.6;">{item}</li>' for item in item_list])
        return f'<ol style="margin: 12px 0; padding-left: 24px;">{li_html}</ol>'
    
    html = re.sub(r'((?:^\d+\. .+\n?)+)', format_ol, html, flags=re.MULTILINE)
    
    # 引用块
    def format_blockquote(match):
        content = match.group(1)
        # 处理引用块内的换行
        content = content.replace('\n> ', '<br>')
        content = content.replace('\n>', '')
        return f'<blockquote style="margin: 16px 0; padding: 12px 16px; background-color: #f7f7f7; border-left: 4px solid #576b95; color: #666; font-style: italic;">{content}</blockquote>'
    
    html = re.sub(r'^> (.+(?:\n> .*)*)', format_blockquote, html, flags=re.MULTILINE)
    
    # 分隔线
    html = re.sub(r'^---+$', '<hr style="border: none; border-top: 1px solid #eee; margin: 24px 0;">', html, flags=re.MULTILINE)
    
    # 段落
    paragraphs = html.split('\n\n')
    formatted_paragraphs = []
    for p in paragraphs:
        p = p.strip()
        if not p:
            continue
        # 如果已经包裹在 HTML 标签中，不再添加 p 标签
        if p.startswith('<') and not p.startswith('<code>'):
            formatted_paragraphs.append(p)
        else:
            formatted_paragraphs.append(f'<p style="margin: 16px 0; line-height: 1.8; color: #333; font-size: 16px;">{p}</p>')
    
    html = '\n\n'.join(formatted_paragraphs)
    
    # 包裹在内容容器中
    html = f'''<div style="max-width: 100%; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', sans-serif; line-height: 1.8; color: #333;">
{html}
</div>'''
    
    return html


def extract_frontmatter(content: str) -> tuple:
    """提取 frontmatter"""
    if not content.startswith('---'):
        return {}, content
    
    try:
        import yaml
        match = re.match(r'^---\s*\n(.*?)\n---\s*\n?(.*)$', content, re.DOTALL)
        if match:
            frontmatter = yaml.safe_load(match.group(1)) or {}
            body = match.group(2)
            return frontmatter, body
    except ImportError:
        pass
    
    return {}, content


def convert_file(input_path: str, output_path: str = None) -> str:
    """转换文件"""
    with open(input_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 提取 frontmatter
    frontmatter, body = extract_frontmatter(content)
    
    # 转换
    html = markdown_to_wechat_html(body)
    
    # 构建完整 HTML
    title = frontmatter.get('title', '无标题')
    full_html = f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        body {{ margin: 0; padding: 20px; background: #f5f5f5; }}
        .container {{ max-width: 677px; margin: 0 auto; background: white; padding: 20px; }}
    </style>
</head>
<body>
    <div class="container">
        {html}
    </div>
</body>
</html>'''
    
    # 确定输出路径
    if not output_path:
        base, _ = Path(input_path).stem, Path(input_path).suffix
        output_path = str(Path(input_path).parent / f'{base}_wechat.html')
    
    # 保存
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(full_html)
    
    return output_path, frontmatter


def main():
    parser = argparse.ArgumentParser(description='Markdown 转微信公众号 HTML')
    parser.add_argument('input', help='输入 Markdown 文件')
    parser.add_argument('-o', '--output', help='输出 HTML 文件')
    parser.add_argument('--preview', action='store_true', help='仅预览，不保存')
    
    args = parser.parse_args()
    
    if not Path(args.input).exists():
        print(f"❌ 文件不存在: {args.input}")
        sys.exit(1)
    
    try:
        output_path, frontmatter = convert_file(args.input, args.output)
        
        print(f"✅ 转换完成!")
        print(f"   输出文件: {output_path}")
        
        if frontmatter.get('title'):
            print(f"   标题: {frontmatter['title']}")
        if frontmatter.get('author'):
            print(f"   作者: {frontmatter['author']}")
        if frontmatter.get('cover'):
            print(f"   封面: {frontmatter['cover']}")
        
        # 读取并显示部分内容
        with open(output_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print(f"\n📄 HTML 大小: {len(content)} 字符")
        print("\n💡 使用提示:")
        print("   1. 打开 HTML 文件预览效果")
        print("   2. 复制 <body> 内的内容到公众号编辑器")
        print("   3. 或使用 publish.py 通过 API/浏览器发布")
        
    except Exception as e:
        print(f"❌ 转换失败: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
