# Fallback Template Generator
from PIL import Image, ImageDraw, ImageFilter
import random
import math
import hashlib
from pathlib import Path

class DynamicImageGenerator:
    def __init__(self, icons_dir):
        self.icons_dir = Path(icons_dir)
        self.icons = self._load_icons()
        
    def _load_icons(self):
        """Load medical icons"""
        icons = {}
        if self.icons_dir.exists():
            for icon_file in self.icons_dir.glob("*.png"):
                icons[icon_file.stem] = str(icon_file)
        return icons
    
    def _create_placeholder_icons(self):
        """Create simple placeholder icons"""
        icon_colors = {
            "heart": (255, 99, 132),
            "diabetes": (54, 162, 235),
            "brain": (153, 102, 255),
            "stethoscope": (75, 192, 192),
            "ecg": (255, 159, 64),
            "pill": (255, 205, 86),
            "hospital": (201, 203, 207),
            "doctor": (255, 99, 132)
        }
        
        for icon_name, color in icon_colors.items():
            icon_path = self.icons_dir / f"{icon_name}.png"
            if not icon_path.exists():
                img = Image.new('RGBA', (100, 100), (0, 0, 0, 0))
                draw = ImageDraw.Draw(img)
                
                if icon_name == "heart":
                    draw.polygon([(50, 25), (30, 45), (50, 65), (70, 45)], fill=color)
                    draw.ellipse([25, 15, 45, 35], fill=color)
                    draw.ellipse([55, 15, 75, 35], fill=color)
                elif icon_name == "diabetes":
                    draw.polygon([(50, 20), (30, 60), (70, 60)], fill=color)
                    draw.ellipse([40, 50, 60, 70], fill=color)
                else:
                    draw.rectangle([40, 20, 60, 80], fill=color)
                    draw.rectangle([20, 40, 80, 60], fill=color)
                
                img.save(icon_path)
    
    def _create_gradient_background(self, size, colors, style="radial"):
        """Create gradient background"""
        width, height = size
        image = Image.new('RGB', size)
        draw = ImageDraw.Draw(image)
        
        if style == "linear":
            for i in range(height):
                r = colors['gradient_start'][0] + (colors['gradient_end'][0] - colors['gradient_start'][0]) * i // height
                g = colors['gradient_start'][1] + (colors['gradient_end'][1] - colors['gradient_start'][1]) * i // height
                b = colors['gradient_start'][2] + (colors['gradient_end'][2] - colors['gradient_start'][2]) * i // height
                draw.line([(0, i), (width, i)], fill=(r, g, b))
        else:
            center_x, center_y = width // 2, height // 2
            max_dist = math.sqrt(center_x**2 + center_y**2)
            
            for x in range(width):
                for y in range(height):
                    dist = math.sqrt((x - center_x)**2 + (y - center_y)**2)
                    ratio = dist / max_dist
                    r = int(colors['gradient_start'][0] * (1 - ratio) + colors['gradient_end'][0] * ratio)
                    g = int(colors['gradient_start'][1] * (1 - ratio) + colors['gradient_end'][1] * ratio)
                    b = int(colors['gradient_start'][2] * (1 - ratio) + colors['gradient_end'][2] * ratio)
                    draw.point((x, y), fill=(r, g, b))
        
        return image
    
    def generate_image(self, key_phrases, tone, colors):
        """Generate template-based image"""
        # Create seed
        seed_text = str(key_phrases) + str(tone)
        seed = int(hashlib.md5(seed_text.encode()).hexdigest()[:8], 16)
        random.seed(seed)
        
        size = (1080, 1080)
        
        # Create gradient background
        gradient_style = random.choice(["linear", "radial"])
        image = self._create_gradient_background(size, colors, gradient_style)
        
        # Add medical icons
        self._create_placeholder_icons()
        
        # Add ECG line
        draw = ImageDraw.Draw(image)
        ecg_points = []
        for i in range(0, size[0], 20):
            x = i
            y = size[1]//2 + 50 * math.sin(i/50)
            ecg_points.append((x, y))
        
        if len(ecg_points) > 1:
            draw.line(ecg_points, fill=colors['accent'], width=5)
        
        return image