from PIL import Image, ImageDraw, ImageFont
import textwrap

class EnhancedLayoutDesigner:
    def __init__(self, font_path, bold_font_path):
        self.font_path = font_path
        self.bold_font_path = bold_font_path
    
    def _hex_to_rgb(self, hex_color):
        """Convert hex color to RGB tuple"""
        if isinstance(hex_color, tuple):
            return hex_color
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    def _add_text_with_outline(self, draw, text, position, font, text_color, outline_color, outline_width=2):
        """Add text with outline"""
        x, y = position
        
        # Convert colors if they're hex strings
        if isinstance(text_color, str):
            text_color = self._hex_to_rgb(text_color)
        if isinstance(outline_color, str):
            outline_color = self._hex_to_rgb(outline_color)
        
        # Draw outline
        for dx in range(-outline_width, outline_width + 1):
            for dy in range(-outline_width, outline_width + 1):
                if dx != 0 or dy != 0:
                    draw.text((x + dx, y + dy), text, font=font, fill=outline_color, anchor="mm")
        
        # Draw main text
        draw.text((x, y), text, font=font, fill=text_color, anchor="mm")
    
    def design_poster(self, image, text_elements, colors, tone):
        """Design poster layout"""
        # Convert image to RGBA if needed
        if image.mode != 'RGBA':
            poster = image.convert('RGBA')
        else:
            poster = image.copy()
        
        draw = ImageDraw.Draw(poster, 'RGBA')
        width, height = poster.size
        
        # Convert all colors from hex to RGB
        rgb_colors = {}
        for key, value in colors.items():
            rgb_colors[key] = self._hex_to_rgb(value)
        
        # Load fonts
        try:
            title_font = ImageFont.truetype(self.bold_font_path, 70)
            subtitle_font = ImageFont.truetype(self.font_path, 50)
            body_font = ImageFont.truetype(self.font_path, 40)
            small_font = ImageFont.truetype(self.font_path, 30)
        except:
            title_font = ImageFont.load_default()
            subtitle_font = ImageFont.load_default()
            body_font = ImageFont.load_default()
            small_font = ImageFont.load_default()
        
        # Add semi-transparent overlay for text
        overlay_height = 450
        overlay = Image.new('RGBA', (width, overlay_height), (0, 0, 0, 0))
        overlay_draw = ImageDraw.Draw(overlay)
        
        for y in range(overlay_height):
            alpha = int(180 * (1 - y / overlay_height))
            overlay_draw.line([(0, y), (width, y)], fill=(0, 0, 0, alpha))
        
        poster.paste(overlay, (0, height - overlay_height), overlay)
        
        # Draw accent lines
        draw.rectangle([0, 0, width, 10], fill=rgb_colors['accent'])
        draw.rectangle([0, height-10, width, height], fill=rgb_colors['accent'])
        
        # Position text
        y_position = height - 350
        
        # Draw headline
        if 'headline' in text_elements:
            headline = text_elements['headline']
            wrapped_lines = textwrap.wrap(headline, width=25)
            
            for i, line in enumerate(wrapped_lines[:2]):
                y_offset = y_position + i * 80
                self._add_text_with_outline(
                    draw, line, (width//2, y_offset),
                    title_font if i == 0 else subtitle_font,
                    rgb_colors.get('text', (255, 255, 255)),
                    (0, 0, 0), 3
                )
            
            y_position += len(wrapped_lines[:2]) * 80 + 20
        
        # Draw features
        if 'features' in text_elements:
            for i, feature in enumerate(text_elements['features'][:3]):
                feature_y = y_position + i * 60
                # Draw bullet point
                draw.ellipse([width//2 - 100, feature_y - 10, width//2 - 80, feature_y + 10], 
                           fill=rgb_colors['accent'])
                # Draw feature text
                draw.text((width//2 - 50, feature_y), feature, font=body_font, 
                         fill=(255, 255, 255), anchor="lm")
            
            y_position += 200
        
        # Draw CTA
        if 'cta' in text_elements:
            draw.text((width//2, height - 70), text_elements['cta'], 
                     font=body_font, fill=rgb_colors['accent'], anchor="mm")
        
        # Draw percentage badge
        if text_elements.get('percentage'):
            badge_text = text_elements['percentage']
            # Draw badge background
            draw.ellipse([150, 150, 250, 250], fill=rgb_colors['accent'] + (200,))
            draw.ellipse([160, 160, 240, 240], fill=rgb_colors['primary'] + (230,))
            # Draw text
            draw.text((200, 200), badge_text, font=title_font, fill=(255, 255, 255), anchor="mm")
            draw.text((200, 250), "ACCURACY", font=small_font, fill=(255, 255, 255), anchor="mm")
        
        return poster.convert('RGB')