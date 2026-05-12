#!/usr/bin/env python3
"""
File Preview Module - Generate previews for different file types
"""

import os
import base64
from pathlib import Path
from PIL import Image
import io


class FilePreview:
    """Generate file previews"""
    
    SUPPORTED_IMAGES = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp'}
    SUPPORTED_DOCS = {'.txt', '.md', '.json', '.xml', '.csv'}
    
    def __init__(self, max_preview_size=(400, 400)):
        self.max_preview_size = max_preview_size
    
    def can_preview(self, filename):
        """Check if file can be previewed"""
        ext = Path(filename).suffix.lower()
        return ext in self.SUPPORTED_IMAGES or ext in self.SUPPORTED_DOCS
    
    def generate_image_preview(self, file_path):
        """
        Generate image preview as base64
        
        Returns:
            tuple: (success, base64_data or error_message)
        """
        try:
            with Image.open(file_path) as img:
                # Convert to RGB if needed
                if img.mode in ('RGBA', 'LA', 'P'):
                    background = Image.new('RGB', img.size, (255, 255, 255))
                    if img.mode == 'P':
                        img = img.convert('RGBA')
                    background.paste(img, mask=img.split()[-1] if img.mode in ('RGBA', 'LA') else None)
                    img = background
                
                # Resize
                img.thumbnail(self.max_preview_size, Image.Resampling.LANCZOS)
                
                # Convert to base64
                buffer = io.BytesIO()
                img.save(buffer, format='JPEG', quality=85)
                img_base64 = base64.b64encode(buffer.getvalue()).decode()
                
                return True, f"data:image/jpeg;base64,{img_base64}"
        
        except Exception as e:
            return False, str(e)
    
    def generate_text_preview(self, file_path, max_lines=50):
        """
        Generate text file preview
        
        Returns:
            tuple: (success, text_content or error_message)
        """
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                lines = []
                for i, line in enumerate(f):
                    if i >= max_lines:
                        lines.append(f"\n... ({i} more lines)")
                        break
                    lines.append(line.rstrip())
                
                return True, '\n'.join(lines)
        
        except Exception as e:
            return False, str(e)
    
    def get_file_info(self, file_path):
        """Get detailed file information"""
        try:
            path = Path(file_path)
            stat = path.stat()
            
            info = {
                'name': path.name,
                'size': stat.st_size,
                'size_formatted': self._format_size(stat.st_size),
                'extension': path.suffix.lower(),
                'modified': stat.st_mtime,
                'can_preview': self.can_preview(path.name)
            }
            
            # Add image-specific info
            if path.suffix.lower() in self.SUPPORTED_IMAGES:
                try:
                    with Image.open(file_path) as img:
                        info['width'] = img.width
                        info['height'] = img.height
                        info['format'] = img.format
                        info['mode'] = img.mode
                except:
                    pass
            
            return info
        
        except Exception as e:
            return {'error': str(e)}
    
    def _format_size(self, size):
        """Format file size"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024:
                return f"{size:.1f} {unit}"
            size /= 1024
        return f"{size:.1f} TB"


# Test
if __name__ == "__main__":
    preview = FilePreview()
    print("🖼️ File Preview Module Ready!")
    print(f"\nSupported Images: {', '.join(preview.SUPPORTED_IMAGES)}")
    print(f"Supported Docs: {', '.join(preview.SUPPORTED_DOCS)}")
