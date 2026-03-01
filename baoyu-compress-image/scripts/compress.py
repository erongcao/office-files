#!/usr/bin/env python3
"""
图片压缩工具
改编自 baoyu-compress-image
"""

import os
import sys
import argparse
from pathlib import Path

try:
    from PIL import Image, ImageOptim
except ImportError:
    print("请先安装依赖: pip install Pillow")
    sys.exit(1)


class ImageCompressor:
    """图片压缩器"""
    
    SUPPORTED_FORMATS = ('.jpg', '.jpeg', '.png', '.webp', '.bmp', '.tiff')
    
    def __init__(self, quality: int = 85):
        self.quality = quality
    
    def compress(self, input_path: str, output_path: str = None, 
                 max_width: int = None, max_height: int = None) -> str:
        """压缩单张图片"""
        
        # 打开图片
        with Image.open(input_path) as img:
            # 转换模式
            if img.mode in ('RGBA', 'P'):
                if output_path and output_path.lower().endswith('.jpg'):
                    img = img.convert('RGB')
                elif not output_path and input_path.lower().endswith('.jpg'):
                    img = img.convert('RGB')
            
            # 调整尺寸
            original_size = img.size
            if max_width or max_height:
                img.thumbnail(
                    (max_width or img.width, max_height or img.height),
                    Image.LANCZOS
                )
            
            # 确定输出路径
            if not output_path:
                base, ext = os.path.splitext(input_path)
                output_path = f"{base}-compressed{ext}"
            
            # 确定格式
            fmt = self._get_format(output_path)
            
            # 保存（压缩）
            save_kwargs = {'optimize': True}
            
            if fmt in ('JPEG', 'WEBP'):
                save_kwargs['quality'] = self.quality
                save_kwargs['progressive'] = True
            elif fmt == 'PNG':
                save_kwargs['compress_level'] = 9
            
            if img.mode == 'RGBA' and fmt == 'JPEG':
                img = img.convert('RGB')
            
            img.save(output_path, format=fmt, **save_kwargs)
            
            # 显示结果
            original_kb = os.path.getsize(input_path) / 1024
            compressed_kb = os.path.getsize(output_path) / 1024
            reduction = (1 - compressed_kb / original_kb) * 100
            
            print(f"✅ {os.path.basename(input_path)}")
            print(f"   原大小: {original_kb:.1f} KB")
            print(f"   压缩后: {compressed_kb:.1f} KB")
            print(f"   减少: {reduction:.1f}%")
            if original_size != img.size:
                print(f"   尺寸: {original_size} → {img.size}")
            
            return output_path
    
    def _get_format(self, path: str) -> str:
        """根据文件扩展名获取格式"""
        ext = os.path.splitext(path)[1].lower()
        format_map = {
            '.jpg': 'JPEG',
            '.jpeg': 'JPEG',
            '.png': 'PNG',
            '.webp': 'WEBP',
            '.bmp': 'BMP',
            '.tiff': 'TIFF',
        }
        return format_map.get(ext, 'JPEG')
    
    def compress_directory(self, dir_path: str, output_dir: str = None,
                          max_width: int = None, max_height: int = None):
        """批量压缩目录"""
        dir_path = Path(dir_path)
        
        if output_dir:
            output_dir = Path(output_dir)
            output_dir.mkdir(parents=True, exist_ok=True)
        
        # 查找所有图片
        images = []
        for ext in self.SUPPORTED_FORMATS:
            images.extend(dir_path.glob(f'*{ext}'))
            images.extend(dir_path.glob(f'*{ext.upper()}'))
        
        if not images:
            print(f"⚠️  未找到支持的图片格式: {dir_path}")
            return
        
        print(f"📁 找到 {len(images)} 张图片，开始压缩...")
        print(f"   质量设置: {self.quality}")
        print()
        
        for img_path in sorted(images):
            if output_dir:
                out_path = output_dir / img_path.name
            else:
                out_path = None
            
            try:
                self.compress(str(img_path), str(out_path) if out_path else None,
                            max_width, max_height)
                print()
            except Exception as e:
                print(f"❌ 压缩失败 {img_path.name}: {e}")
                print()


def main():
    parser = argparse.ArgumentParser(description='图片压缩工具')
    parser.add_argument('path', help='图片路径或目录')
    parser.add_argument('-q', '--quality', type=int, default=85,
                       help='压缩质量 (1-100)，默认 85')
    parser.add_argument('-o', '--output', help='输出路径')
    parser.add_argument('--max-width', type=int, help='最大宽度')
    parser.add_argument('--max-height', type=int, help='最大高度')
    parser.add_argument('--output-dir', help='批量压缩时的输出目录')
    
    args = parser.parse_args()
    
    if args.quality < 1 or args.quality > 100:
        print("❌ 质量参数应在 1-100 之间")
        sys.exit(1)
    
    compressor = ImageCompressor(quality=args.quality)
    
    if os.path.isdir(args.path):
        # 批量压缩
        compressor.compress_directory(
            args.path,
            output_dir=args.output_dir,
            max_width=args.max_width,
            max_height=args.max_height
        )
    else:
        # 单张压缩
        if not os.path.exists(args.path):
            print(f"❌ 文件不存在: {args.path}")
            sys.exit(1)
        
        try:
            compressor.compress(
                args.path,
                args.output,
                args.max_width,
                args.max_height
            )
        except Exception as e:
            print(f"❌ 压缩失败: {e}")
            sys.exit(1)


if __name__ == '__main__':
    main()
