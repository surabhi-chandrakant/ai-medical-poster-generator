from PIL import Image
from pathlib import Path

class Branding:
    def __init__(self, logo_path):
        self.logo_path = Path(logo_path)
        self.logo = self._load_logo()
        
    def _load_logo(self):
        """Load or create default logo"""
        if self.logo_path.exists():
            try:
                return Image.open(self.logo_path).convert('RGBA')
            except:
                return self._create_default_logo()
        return self._create_default_logo()
    
    def _create_default_logo(self):
        """Create default medical logo"""
        img = Image.new('RGBA', (200, 200), (0, 0, 0, 0))
        from PIL import ImageDraw
        draw = ImageDraw.Draw(img)
        draw.ellipse([0, 0, 199, 199], fill=(41, 128, 185, 255))
        draw.rectangle([85, 40, 115, 160], fill=(255, 255, 255, 255))
        draw.rectangle([40, 85, 160, 115], fill=(255, 255, 255, 255))
        return img
    
    def add_logo(self, poster, position='top-right'):
        """Add logo to poster"""
        if self.logo is None:
            return poster
        
        logo_size = (120, 120)
        logo_resized = self.logo.resize(logo_size, Image.Resampling.LANCZOS)
        
        positions = {
            'top-right': (poster.width - logo_size[0] - 20, 20),
            'top-left': (20, 20),
            'bottom-right': (poster.width - logo_size[0] - 20, poster.height - logo_size[1] - 20),
            'bottom-left': (20, poster.height - logo_size[1] - 20)
        }
        
        x, y = positions.get(position, positions['top-right'])
        poster.paste(logo_resized, (x, y), logo_resized)
        return poster