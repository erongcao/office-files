#!/usr/bin/env python3
"""
Markdown 格式化工具
改编自 baoyu-format-markdown
"""

import re
import os
import sys
from pathlib import Path
from typing import Optional, Dict, Any


def add_cjk_spacing(text: str) -> str:
    """在中英文之间添加空格"""
    # CJK 字符范围
    cjk_pattern = r'[\u4e00-\u9fff\u3000-\u303f\uff00-\uffef]'
    
    # 英文/数字
    eng_pattern = r'[a-zA-Z0-9]'
    
    # CJK 后面跟英文/数字，中间加空格
    text = re.sub(f'({cjk_pattern})({eng_pattern})', r'\1 \2', text)
    # 英文/数字后面跟 CJK，中间加空格
    text = re.sub(f'({eng_pattern})({cjk_pattern})', r'\1 \2', text)
    
    return text


def convert_quotes(text: str) -> str:
    """转换引号为全角"""
    # 双引号
    text = re.sub(r'"([^"]*)"', r'"\1"', text)
    # 单引号
    text = re.sub(r"'([^']*)'", r"'\1'", text)
    return text


def extract_title(content: str) -> Optional[str]:
    """从内容中提取标题"""
    # 查找 H1
    h1_match = re.search(r'^# (.+)$', content, re.MULTILINE)
    if h1_match:
        return h1_match.group(1).strip()
    
    # 查找第一行非空文本
    lines = content.strip().split('\n')
    for line in lines:
        line = line.strip()
        if line and not line.startswith('#') and not line.startswith('-'):
            # 限制长度
            if len(line) <= 50:
                return line
            return line[:50] + '...'
    
    return None


def generate_summary(content: str) -> str:
    """生成摘要"""
    # 移除 markdown 标记
    text = re.sub(r'#+ ', '', content)  # 标题
    text = re.sub(r'\*\*', '', text)     # 加粗
    text = re.sub(r'`[^`]*`', '', text) # 代码
    text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text)  # 链接
    
    # 提取纯文本（前300字符）
    text = ' '.join(text.split())
    if len(text) > 150:
        return text[:150] + '...'
    return text


def generate_slug(title: str) -> str:
    """从标题生成 slug"""
    # 移除标点
    slug = re.sub(r'[^\w\s-]', '', title)
    # 替换空格为连字符
    slug = re.sub(r'\s+', '-', slug.strip())
    # 转小写
    return slug.lower()[:50]


def format_content(content: str) -> str:
    """格式化内容结构"""
    lines = content.split('\n')
    formatted_lines = []
    
    in_code_block = False
    
    for line in lines:
        # 代码块处理
        if line.strip().startswith('```'):
            in_code_block = not in_code_block
            formatted_lines.append(line)
            continue
        
        if in_code_block:
            formatted_lines.append(line)
            continue
        
        # 普通文本处理
        stripped = line.strip()
        
        # 跳过空行
        if not stripped:
            formatted_lines.append('')
            continue
        
        # 标题行保持原样
        if stripped.startswith('#'):
            formatted_lines.append(stripped)
            continue
        
        # 列表行保持原样
        if stripped.startswith('- ') or stripped.startswith('* ') or re.match(r'^\d+\. ', stripped):
            formatted_lines.append(stripped)
            continue
        
        # 引用行保持原样
        if stripped.startswith('>'):
            formatted_lines.append(stripped)
            continue
        
        # 普通段落：应用中文排版
        formatted = stripped
        formatted = add_cjk_spacing(formatted)
        formatted = convert_quotes(formatted)
        formatted_lines.append(formatted)
    
    return '\n'.join(formatted_lines)


def has_frontmatter(content: str) -> bool:
    """检查是否已有 frontmatter"""
    return content.strip().startswith('---')


def parse_frontmatter(content: str) -> tuple:
    """解析 frontmatter，返回 (frontmatter_dict, content_without_frontmatter)"""
    if not has_frontmatter(content):
        return {}, content
    
    try:
        import yaml
        # 找到第二个 ---
        match = re.match(r'^---\s*\n(.*?)\n---\s*\n?(.*)$', content, re.DOTALL)
        if match:
            frontmatter = yaml.safe_load(match.group(1)) or {}
            body = match.group(2)
            return frontmatter, body
    except ImportError:
        pass
    
    return {}, content


def build_frontmatter(data: Dict[str, Any]) -> str:
    """构建 frontmatter 字符串"""
    try:
        import yaml
        yaml_str = yaml.dump(data, allow_unicode=True, default_flow_style=False, sort_keys=False)
        return f'---\n{yaml_str}---\n\n'
    except ImportError:
        # 手动构建简单的 frontmatter
        lines = ['---']
        for key, value in data.items():
            if isinstance(value, str):
                lines.append(f'{key}: "{value}"')
            else:
                lines.append(f'{key}: {value}')
        lines.append('---')
        return '\n'.join(lines) + '\n\n'


def format_markdown_file(file_path: str, output_path: Optional[str] = None) -> str:
    """格式化 Markdown 文件"""
    # 读取文件
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 解析现有 frontmatter
    frontmatter, body = parse_frontmatter(content)
    
    # 提取或更新标题
    title = frontmatter.get('title') or extract_title(body)
    if title and 'title' not in frontmatter:
        frontmatter['title'] = title
    
    # 生成 slug
    if title and 'slug' not in frontmatter:
        frontmatter['slug'] = generate_slug(title)
    
    # 生成摘要
    if 'summary' not in frontmatter:
        frontmatter['summary'] = generate_summary(body)
    
    # 检查封面图
    cover_path = os.path.join(os.path.dirname(file_path), 'imgs', 'cover.png')
    if os.path.exists(cover_path) and 'coverImage' not in frontmatter:
        frontmatter['coverImage'] = './imgs/cover.png'
    
    # 格式化内容
    formatted_body = format_content(body)
    
    # 组合最终内容
    final_content = build_frontmatter(frontmatter) + formatted_body
    
    # 确定输出路径
    if not output_path:
        base, ext = os.path.splitext(file_path)
        output_path = f'{base}-formatted{ext}'
    
    # 写入文件
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(final_content)
    
    return output_path


def main():
    """命令行入口"""
    if len(sys.argv) < 2:
        print("用法: python format.py <markdown文件> [输出文件]")
        print("示例: python format.py article.md")
        print("      python format.py article.md output.md")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    if not os.path.exists(input_file):
        print(f"❌ 文件不存在: {input_file}")
        sys.exit(1)
    
    try:
        result = format_markdown_file(input_file, output_file)
        print(f"✅ 格式化完成: {result}")
        
        # 显示摘要
        with open(result, 'r', encoding='utf-8') as f:
            content = f.read()
        fm, body = parse_frontmatter(content)
        if fm.get('title'):
            print(f"   标题: {fm['title']}")
        if fm.get('summary'):
            print(f"   摘要: {fm['summary'][:80]}...")
            
    except Exception as e:
        print(f"❌ 格式化失败: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
