#!/usr/bin/env python3
"""
微信公众号发布工具
改编自 baoyu-post-to-wechat
"""

import os
import sys
import json
import time
import argparse
from pathlib import Path
from urllib.parse import urlencode

try:
    import requests
except ImportError:
    print("请先安装依赖: pip install requests")
    sys.exit(1)


class WeChatPublisher:
    """微信公众号发布器"""
    
    API_BASE = 'https://api.weixin.qq.com/cgi-bin'
    
    def __init__(self, app_id: str = None, app_secret: str = None):
        self.app_id = app_id or os.getenv('WECHAT_APP_ID')
        self.app_secret = app_secret or os.getenv('WECHAT_APP_SECRET')
        self.access_token = None
    
    def get_access_token(self) -> str:
        """获取 Access Token"""
        if not self.app_id or not self.app_secret:
            raise ValueError("缺少 WECHAT_APP_ID 或 WECHAT_APP_SECRET")
        
        url = f'{self.API_BASE}/token'
        params = {
            'grant_type': 'client_credential',
            'appid': self.app_id,
            'secret': self.app_secret
        }
        
        response = requests.get(url, params=params)
        data = response.json()
        
        if 'access_token' in data:
            self.access_token = data['access_token']
            return self.access_token
        else:
            raise Exception(f"获取 Access Token 失败: {data}")
    
    def upload_image(self, image_path: str) -> str:
        """上传图片到微信服务器，返回 URL"""
        if not self.access_token:
            self.get_access_token()
        
        url = f'{self.API_BASE}/media/uploadimg?access_token={self.access_token}'
        
        with open(image_path, 'rb') as f:
            files = {'media': f}
            response = requests.post(url, files=files)
        
        data = response.json()
        if 'url' in data:
            return data['url']
        else:
            raise Exception(f"上传图片失败: {data}")
    
    def draft_add(self, title: str, content: str, author: str = '', 
                  digest: str = '', cover_url: str = '', 
                  need_open_comment: int = 1, only_fans_can_comment: int = 0) -> str:
        """添加草稿"""
        if not self.access_token:
            self.get_access_token()
        
        url = f'{self.API_BASE}/draft/add?access_token={self.access_token}'
        
        articles = [{
            'title': title,
            'content': content,
            'author': author,
            'digest': digest,
            'thumb_media_id': cover_url,  # 这里应该是 media_id，简化处理
            'need_open_comment': need_open_comment,
            'only_fans_can_comment': only_fans_can_comment,
            'show_cover_pic': 1
        }]
        
        data = {'articles': articles}
        
        response = requests.post(url, json=data)
        result = response.json()
        
        if 'media_id' in result:
            return result['media_id']
        else:
            raise Exception(f"添加草稿失败: {result}")
    
    def publish(self, media_id: str) -> dict:
        """发布文章"""
        if not self.access_token:
            self.get_access_token()
        
        url = f'{self.API_BASE}/freepublish/submit?access_token={self.access_token}'
        
        data = {'media_id': media_id}
        
        response = requests.post(url, json=data)
        return response.json()


def extract_frontmatter(content: str) -> tuple:
    """提取 frontmatter"""
    import re
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


def load_config() -> dict:
    """加载配置"""
    config = {}
    
    # 从环境变量读取
    config['app_id'] = os.getenv('WECHAT_APP_ID')
    config['app_secret'] = os.getenv('WECHAT_APP_SECRET')
    
    # 从配置文件读取
    config_paths = [
        '.baoyu-skills/.env',
        os.path.expanduser('~/.baoyu-skills/.env')
    ]
    
    for path in config_paths:
        if os.path.exists(path):
            with open(path, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and '=' in line and not line.startswith('#'):
                        key, value = line.split('=', 1)
                        if key == 'WECHAT_APP_ID' and not config['app_id']:
                            config['app_id'] = value.strip().strip('"\'')
                        elif key == 'WECHAT_APP_SECRET' and not config['app_secret']:
                            config['app_secret'] = value.strip().strip('"\'')
    
    return config


def prepare_browser_content(input_path: str, output_path: str = None) -> dict:
    """准备浏览器发布的内容"""
    # 导入转换模块
    sys.path.insert(0, str(Path(__file__).parent))
    from convert import convert_file
    
    # 转换
    html_path, frontmatter = convert_file(input_path, output_path)
    
    # 读取 HTML
    with open(html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # 提取 body 内容
    import re
    body_match = re.search(r'<body>.*?<div class="container">(.*)</div>.*?</body>', 
                           html_content, re.DOTALL)
    if body_match:
        content_html = body_match.group(1).strip()
    else:
        content_html = html_content
    
    return {
        'title': frontmatter.get('title', '无标题'),
        'author': frontmatter.get('author', ''),
        'summary': frontmatter.get('summary', ''),
        'cover': frontmatter.get('cover', ''),
        'html_path': html_path,
        'content_html': content_html
    }


def main():
    parser = argparse.ArgumentParser(description='微信公众号发布工具')
    parser.add_argument('input', help='输入 Markdown 文件')
    parser.add_argument('--title', help='文章标题（覆盖 frontmatter）')
    parser.add_argument('--author', help='作者名（覆盖 frontmatter）')
    parser.add_argument('--cover', help='封面图路径')
    parser.add_argument('--method', choices=['api', 'browser'], default='browser',
                       help='发布方式：api 或 browser')
    parser.add_argument('--publish', action='store_true', 
                       help='立即发布（仅 API 方式有效）')
    parser.add_argument('-o', '--output', help='输出 HTML 文件路径')
    
    args = parser.parse_args()
    
    if not Path(args.input).exists():
        print(f"❌ 文件不存在: {args.input}")
        sys.exit(1)
    
    if args.method == 'browser':
        # 浏览器方式
        print("🌐 浏览器发布方式")
        print()
        
        result = prepare_browser_content(args.input, args.output)
        
        print("=" * 60)
        print(f"📄 文章信息")
        print("=" * 60)
        print(f"标题: {result['title']}")
        print(f"作者: {result['author'] or '未设置'}")
        print(f"摘要: {result['summary'][:80] + '...' if result['summary'] else '未设置'}")
        print(f"封面: {result['cover'] or '未设置'}")
        print()
        print(f"HTML 文件: {result['html_path']}")
        print()
        print("=" * 60)
        print("📋 发布步骤")
        print("=" * 60)
        print("1. 打开生成的 HTML 文件，复制内容")
        print("2. 登录 mp.weixin.qq.com")
        print("3. 内容与互动 → 草稿箱 → 写新图文")
        print("4. 粘贴内容到编辑器")
        print("5. 设置封面图和摘要")
        print("6. 保存并发布")
        print()
        
    else:
        # API 方式
        print("🔌 API 发布方式")
        print()
        
        # 加载配置
        config = load_config()
        
        if not config['app_id'] or not config['app_secret']:
            print("❌ 缺少微信公众号 API 配置")
            print()
            print("请设置以下环境变量或在 .baoyu-skills/.env 中添加:")
            print("  WECHAT_APP_ID=你的AppID")
            print("  WECHAT_APP_SECRET=你的AppSecret")
            print()
            print("获取方式:")
            print("  1. 登录 https://mp.weixin.qq.com")
            print("  2. 开发 → 基本配置 → 复制 AppID 和 AppSecret")
            sys.exit(1)
        
        try:
            publisher = WeChatPublisher(config['app_id'], config['app_secret'])
            
            # 准备内容
            result = prepare_browser_content(args.input)
            
            print("📤 正在发布...")
            print(f"   标题: {result['title']}")
            print(f"   作者: {result['author']}")
            
            # 添加草稿
            media_id = publisher.draft_add(
                title=result['title'],
                content=result['content_html'],
                author=result['author'],
                digest=result['summary'][:120]
            )
            
            print(f"✅ 草稿已添加，Media ID: {media_id}")
            
            if args.publish:
                # 立即发布
                pub_result = publisher.publish(media_id)
                print(f"✅ 发布请求已提交")
                print(f"   Publish ID: {pub_result.get('publish_id', 'N/A')}")
                print()
                print("⚠️  注意：发布成功后会有延迟，请在公众号后台查看状态")
            else:
                print()
                print("💡 草稿已保存，请登录公众号后台查看并手动发布")
            
        except Exception as e:
            print(f"❌ 发布失败: {e}")
            sys.exit(1)


if __name__ == '__main__':
    main()
