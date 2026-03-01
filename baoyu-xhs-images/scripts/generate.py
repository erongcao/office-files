#!/usr/bin/env python3
"""
小红书信息图生成器
改编自 baoyu-xhs-images
"""

import os
import sys
import json
import argparse
from datetime import datetime
from pathlib import Path


# 风格定义
STYLES = {
    'cute': {
        'name': '甜美可爱',
        'colors': ['FFB6C1', 'FFC0CB', 'FFE4E1', 'FF69B4'],
        'desc': '柔和粉色系，圆润线条，可爱贴纸元素'
    },
    'fresh': {
        'name': '清新自然',
        'colors': ['98FB98', '90EE90', '87CEEB', 'E0FFFF'],
        'desc': '薄荷绿和天蓝色，自然植物元素'
    },
    'warm': {
        'name': '温馨亲切',
        'colors': ['FFE4B5', 'FFDAB9', 'F4A460', 'DEB887'],
        'desc': '暖橙色调，柔和阴影'
    },
    'bold': {
        'name': '高冲击力',
        'colors': ['FF4500', 'FF6347', 'FFD700', '00CED1'],
        'desc': '高对比度配色，粗体文字'
    },
    'minimal': {
        'name': '极简精致',
        'colors': ['FFFFFF', 'F5F5F5', '333333', '666666'],
        'desc': '黑白灰为主，大量留白'
    },
    'retro': {
        'name': '复古怀旧',
        'colors': ['D2691E', 'CD853F', 'DEB887', 'F5DEB3'],
        'desc': '棕褐色调，做旧质感'
    },
    'pop': {
        'name': '活力四射',
        'colors': ['FF1493', '00FF7F', 'FFD700', '00BFFF'],
        'desc': '鲜艳撞色，波普艺术风格'
    },
    'notion': {
        'name': '手绘线稿',
        'colors': ['FFFFFF', 'F7F6F3', '37352F', 'E9E9E7'],
        'desc': '简约线条，类似 Notion 风格'
    },
    'chalkboard': {
        'name': '黑板粉笔',
        'colors': ['2F4F4F', 'FF6B6B', '4ECDC4', 'FFE66D'],
        'desc': '深色背景，彩色粉笔效果'
    },
    'study-notes': {
        'name': '手写笔记',
        'colors': ['F0F8FF', '4169E1', 'DC143C', 'FFD700'],
        'desc': '蓝笔+红批注+黄高亮'
    }
}

# 布局定义
LAYOUTS = {
    'sparse': {
        'name': '极简',
        'points': '1-2个要点',
        'desc': '大量留白，突出重点'
    },
    'balanced': {
        'name': '平衡',
        'points': '3-4个要点',
        'desc': '标准内容布局'
    },
    'dense': {
        'name': '密集',
        'points': '5-8个要点',
        'desc': '知识卡片风格'
    },
    'list': {
        'name': '列表',
        'points': '4-7个条目',
        'desc': '枚举排名格式'
    },
    'comparison': {
        'name': '对比',
        'points': '2-3个对比项',
        'desc': '并排对比布局'
    },
    'flow': {
        'name': '流程',
        'points': '3-6个步骤',
        'desc': '时间线流程图'
    },
    'mindmap': {
        'name': '思维导图',
        'points': '4-8个分支',
        'desc': '中心放射布局'
    },
    'quadrant': {
        'name': '四象限',
        'points': '4个象限',
        'desc': '矩阵分类布局'
    }
}


class XHSImageGenerator:
    """小红书信息图生成器"""
    
    def __init__(self, style='cute', layout='balanced', max_images=10):
        self.style = style
        self.layout = layout
        self.max_images = max_images
        self.style_config = STYLES.get(style, STYLES['cute'])
        self.layout_config = LAYOUTS.get(layout, LAYOUTS['balanced'])
    
    def parse_content(self, content: str) -> list:
        """解析内容，拆分为多个页面"""
        lines = content.strip().split('\n')
        pages = []
        current_page = {'title': '', 'points': []}
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # 标题行（# 开头）
            if line.startswith('# '):
                if current_page['points']:
                    pages.append(current_page)
                current_page = {'title': line[2:], 'points': []}
            # 二级标题
            elif line.startswith('## '):
                if current_page['points']:
                    pages.append(current_page)
                current_page = {'title': line[3:], 'points': []}
            # 列表项
            elif line.startswith('- ') or line.startswith('* '):
                current_page['points'].append(line[2:])
            # 普通段落
            else:
                if len(line) > 20:
                    current_page['points'].append(line)
        
        if current_page['points'] or current_page['title']:
            pages.append(current_page)
        
        # 限制页面数量
        if len(pages) > self.max_images:
            pages = pages[:self.max_images]
        
        return pages
    
    def generate_prompt(self, page: dict, page_num: int, total: int) -> str:
        """生成图像提示词"""
        style = self.style_config
        layout = self.layout_config
        
        colors_str = ', '.join([f'#{c}' for c in style['colors']])
        
        prompt = f"""Create a Xiaohongshu-style infographic image.

Style: {style['name']} - {style['desc']}
Layout: {layout['name']} - {layout['desc']}

Color palette: {colors_str}

Page {page_num}/{total}:
Title: {page['title']}

Content points:
"""
        for i, point in enumerate(page['points'][:6], 1):
            prompt += f"{i}. {point}\n"
        
        prompt += f"""
Design requirements:
- Aspect ratio: 3:4 (vertical)
- Style: {style['name']}
- Clean typography with clear hierarchy
- Decorative elements matching the style
- Chinese text optimized layout
"""
        return prompt
    
    def generate(self, content: str, output_dir: str = None):
        """生成信息图"""
        # 解析内容
        pages = self.parse_content(content)
        
        if not pages:
            print("❌ 未能从内容中解析出有效页面")
            return None
        
        # 创建输出目录
        if not output_dir:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_dir = f'output/{timestamp}'
        
        os.makedirs(output_dir, exist_ok=True)
        
        print(f"✅ 解析完成: {len(pages)} 页内容")
        print(f"   风格: {self.style_config['name']}")
        print(f"   布局: {self.layout_config['name']}")
        print(f"   输出目录: {output_dir}")
        print()
        
        # 生成提示词
        prompts = []
        for i, page in enumerate(pages, 1):
            prompt = self.generate_prompt(page, i, len(pages))
            prompts.append({
                'page': i,
                'title': page['title'],
                'prompt': prompt
            })
            
            # 保存提示词到文件
            with open(f'{output_dir}/page_{i:02d}.txt', 'w', encoding='utf-8') as f:
                f.write(prompt)
        
        # 保存所有提示词
        with open(f'{output_dir}/prompts.json', 'w', encoding='utf-8') as f:
            json.dump(prompts, f, ensure_ascii=False, indent=2)
        
        print("📄 提示词已生成:")
        for p in prompts:
            print(f"   - {output_dir}/page_{p['page']:02d}.txt")
        print()
        
        # 输出使用说明
        print("🎨 下一步:")
        print("   将提示词复制到图像生成工具（如 DALL-E、Midjourney、Coze）生成图片")
        print("   或使用配套的图像生成脚本自动批量生成")
        print()
        
        return output_dir


def main():
    parser = argparse.ArgumentParser(description='小红书信息图生成器')
    parser.add_argument('input', help='输入文件路径或直接文本')
    parser.add_argument('--style', default='cute', choices=list(STYLES.keys()),
                       help='视觉风格')
    parser.add_argument('--layout', default='balanced', choices=list(LAYOUTS.keys()),
                       help='布局方式')
    parser.add_argument('--max-images', type=int, default=10,
                       help='最大图片数量')
    parser.add_argument('-o', '--output', help='输出目录')
    
    args = parser.parse_args()
    
    # 读取输入
    if os.path.isfile(args.input):
        with open(args.input, 'r', encoding='utf-8') as f:
            content = f.read()
    else:
        content = args.input
    
    # 生成
    generator = XHSImageGenerator(
        style=args.style,
        layout=args.layout,
        max_images=args.max_images
    )
    
    result = generator.generate(content, args.output)
    
    if result:
        print(f"✅ 完成! 查看 {result}/ 目录")
    else:
        sys.exit(1)


if __name__ == '__main__':
    main()
