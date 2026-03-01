#!/usr/bin/env python3
"""
URL to Markdown 转换器
改编自 baoyu-url-to-markdown
"""

import sys
import re
import argparse
from urllib.parse import urljoin, urlparse

try:
    import requests
    from bs4 import BeautifulSoup
    import html2text
except ImportError:
    print("请先安装依赖: pip install requests beautifulsoup4 html2text")
    sys.exit(1)


class UrlToMarkdown:
    """网页转 Markdown 转换器"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        self.h2t = html2text.HTML2Text()
        self.h2t.ignore_links = False
        self.h2t.ignore_images = False
        self.h2t.body_width = 0  # 不限制行宽
    
    def fetch(self, url: str) -> str:
        """获取网页内容"""
        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            response.encoding = response.apparent_encoding
            return response.text
        except Exception as e:
            raise Exception(f"获取页面失败: {e}")
    
    def extract_main_content(self, html: str, url: str) -> str:
        """提取主要内容"""
        soup = BeautifulSoup(html, 'html.parser')
        
        # 移除脚本和样式
        for script in soup(['script', 'style', 'nav', 'footer', 'header']):
            script.decompose()
        
        # 尝试查找文章主体
        article = None
        
        # 常见的文章容器选择器
        selectors = [
            'article',
            'main',
            '.article-content',
            '.post-content',
            '.entry-content',
            '.content',
            '#content',
            '[role="main"]',
        ]
        
        for selector in selectors:
            article = soup.select_one(selector)
            if article:
                break
        
        # 如果没找到，使用 body
        if not article:
            article = soup.find('body')
        
        if not article:
            return soup.get_text()
        
        return str(article)
    
    def clean_markdown(self, md: str) -> str:
        """清理 Markdown"""
        # 移除多余的空行
        md = re.sub(r'\n{3,}', '\n\n', md)
        
        # 移除行首空格
        lines = []
        for line in md.split('\n'):
            if line.strip():
                lines.append(line.rstrip())
            else:
                lines.append('')
        
        return '\n'.join(lines).strip()
    
    def add_frontmatter(self, md: str, url: str, title: str = '') -> str:
        """添加 frontmatter"""
        from datetime import datetime
        
        frontmatter = f"""---
title: "{title or 'Untitled'}"
source: "{url}"
date: "{datetime.now().strftime('%Y-%m-%d')}"
---

"""
        return frontmatter + md
    
    def convert(self, url: str, output_file: str = None, add_fm: bool = True) -> str:
        """转换 URL 到 Markdown"""
        # 获取网页
        html = self.fetch(url)
        
        # 提取标题
        soup = BeautifulSoup(html, 'html.parser')
        title_tag = soup.find('title')
        title = title_tag.get_text().strip() if title_tag else ''
        
        # 提取主要内容
        content_html = self.extract_main_content(html, url)
        
        # 转换为 Markdown
        md = self.h2t.handle(content_html)
        
        # 清理
        md = self.clean_markdown(md)
        
        # 添加 frontmatter
        if add_fm:
            md = self.add_frontmatter(md, url, title)
        
        # 保存或返回
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(md)
            return output_file
        
        return md


def main():
    parser = argparse.ArgumentParser(description='URL to Markdown 转换器')
    parser.add_argument('url', help='要抓取的 URL')
    parser.add_argument('-o', '--output', help='输出文件路径')
    parser.add_argument('--no-frontmatter', action='store_true', help='不添加 frontmatter')
    parser.add_argument('--wait', action='store_true', help='等待模式（需手动确认）')
    
    args = parser.parse_args()
    
    if args.wait:
        print("等待模式：请在浏览器中完成登录等操作，然后按 Enter 继续...")
        print("（提示：此模式需要配合浏览器使用，当前版本为简化实现）")
        input()
    
    converter = UrlToMarkdown()
    
    try:
        result = converter.convert(
            args.url,
            output_file=args.output,
            add_fm=not args.no_frontmatter
        )
        
        if args.output:
            print(f"✅ 已保存: {result}")
        else:
            print(result)
            
    except Exception as e:
        print(f"❌ 转换失败: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
