import random

class CaptionGenerator:
    def __init__(self):
        self.hashtags = [
            '#AIHealthcare', '#MedicalAI', '#HealthTech', 
            '#DigitalHealth', '#AIinMedicine', '#FutureOfMedicine',
            '#DiagnosisRevolution', '#SmartHealthcare', '#MedTech'
        ]
    
    def generate_caption(self, key_phrases, tone):
        """Generate social media caption"""
        conditions = key_phrases['conditions']
        percentages = key_phrases['percentages']
        
        caption_parts = []
        
        # Introduction
        caption_parts.append("🤖 Introducing our AI-powered medical diagnosis system!")
        caption_parts.append("")
        
        # Features
        if percentages:
            caption_parts.append(f"✅ {percentages[0]} accuracy rate")
        
        if conditions:
            conditions_text = " and ".join(conditions[:2])
            caption_parts.append(f"✅ Specialized in {conditions_text}")
        
        caption_parts.append("✅ Instant results within minutes")
        caption_parts.append("✅ Available 24/7")
        caption_parts.append("")
        
        # Call to action
        caption_parts.append("Experience the future of healthcare today! 🚀")
        caption_parts.append("")
        
        # Hashtags
        selected = random.sample(self.hashtags, min(4, len(self.hashtags)))
        caption_parts.append(" ".join(selected))
        
        return "\n".join(caption_parts)