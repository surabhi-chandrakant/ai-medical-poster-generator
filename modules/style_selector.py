from config import COLOR_PALETTES

class StyleSelector:
    def __init__(self):
        self.color_palettes = COLOR_PALETTES
        
    def select_colors(self, tone):
        """Select color palette based on tone"""
        primary_tone = tone['primary_tone']
        
        if primary_tone in self.color_palettes:
            return self.color_palettes[primary_tone]
        else:
            return self.color_palettes['medical']
    
    def select_fonts(self, tone):
        """Select font styles based on tone"""
        # Simple font selection based on tone
        font_styles = {
            'professional': {
                'title': 'bold',
                'body': 'regular',
                'size_multiplier': 1.0
            },
            'urgent': {
                'title': 'bold',
                'body': 'bold',
                'size_multiplier': 1.2
            },
            'trust': {
                'title': 'regular',
                'body': 'regular',
                'size_multiplier': 0.9
            }
        }
        
        return font_styles.get(tone['primary_tone'], font_styles['professional'])