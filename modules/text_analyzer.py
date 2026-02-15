import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from collections import Counter

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')
    nltk.download('stopwords')
    nltk.download('averaged_perceptron_tagger')

class EnhancedTextAnalyzer:
    def __init__(self):
        self.stop_words = set(stopwords.words('english'))
        self.medical_terms = {
            'diabetes': ['diabetes', 'blood sugar', 'insulin', 'glucose'],
            'heart': ['heart', 'cardiac', 'cardiovascular', 'blood pressure'],
            'cancer': ['cancer', 'oncology', 'tumor', 'malignant'],
            'brain': ['brain', 'neurological', 'neural', 'stroke'],
            'respiratory': ['lung', 'breathing', 'respiratory', 'asthma'],
            'general': ['medical', 'health', 'diagnosis', 'patient', 'treatment']
        }
        
    def extract_key_phrases(self, text):
        """Extract key phrases from input text"""
        # Extract percentages
        percentages = re.findall(r'\d+%', text)
        
        # Extract numbers
        numbers = re.findall(r'\d+', text)
        
        # Extract medical conditions
        found_conditions = []
        for category, terms in self.medical_terms.items():
            for term in terms:
                if term.lower() in text.lower():
                    if category not in found_conditions:
                        found_conditions.append(category)
        
        # Extract AI-related terms
        ai_terms = ['AI', 'artificial intelligence', 'machine learning', 'automated']
        found_ai_terms = []
        for term in ai_terms:
            if term.lower() in text.lower():
                found_ai_terms.append(term)
        
        # Tokenize and get important words
        tokens = word_tokenize(text.lower())
        important_words = [word for word in tokens if word not in self.stop_words 
                          and len(word) > 3 and word.isalpha()]
        
        # Get word frequencies
        word_freq = Counter(important_words)
        
        return {
            'percentages': percentages,
            'numbers': numbers,
            'conditions': found_conditions,
            'ai_terms': found_ai_terms,
            'important_words': important_words[:5],
            'word_frequencies': dict(word_freq.most_common(5)),
            'full_text': text
        }
    
    def determine_tone(self, text):
        """Determine the tone of the text"""
        text_lower = text.lower()
        
        # Professional keywords
        professional_keywords = ['accurate', 'precise', 'reliable', 'trusted', 
                                'professional', 'expert', 'advanced']
        professional_score = sum(2 for word in professional_keywords if word in text_lower)
        
        # Urgent keywords
        urgent_keywords = ['instant', 'fast', 'quick', 'rapid', 'immediate', 
                          'emergency', 'critical', 'urgent']
        urgent_score = sum(2 for word in urgent_keywords if word in text_lower)
        
        # Trustworthy keywords
        trust_keywords = ['trust', 'safe', 'secure', 'verified', 'certified', 
                         'guaranteed', 'proven', 'reliable']
        trust_score = sum(2 for word in trust_keywords if word in text_lower)
        
        # Innovative keywords
        innovative_keywords = ['revolutionary', 'innovative', 'cutting-edge', 'breakthrough',
                              'advanced', 'futuristic', 'next-generation']
        innovative_score = sum(2 for word in innovative_keywords if word in text_lower)
        
        # Calculate scores
        scores = {
            'professional': professional_score + 1,
            'urgent': urgent_score + 1,
            'trust': trust_score + 1,
            'innovative': innovative_score + 1
        }
        
        # Determine primary tone
        primary_tone = max(scores, key=scores.get)
        
        return {
            'primary_tone': primary_tone,
            'scores': scores
        }
    
    def generate_headline(self, key_phrases):
        """Generate headline options"""
        conditions = key_phrases['conditions']
        percentages = key_phrases['percentages']
        
        headlines = []
        
        if percentages and conditions:
            headlines.append(f"{percentages[0]} Accurate AI Diagnosis for {conditions[0].title()}")
        
        if conditions:
            headlines.append(f"Revolutionary AI Detects {conditions[0].title()} with Unmatched Precision")
        
        headlines.append("AI-Powered Medical Diagnosis: The Future of Healthcare")
        headlines.append("Trusted AI Healthcare Solution for Accurate Diagnosis")
        
        return headlines
    
    def generate_features(self, key_phrases):
        """Generate feature list"""
        features = []
        
        if key_phrases['percentages']:
            features.append(f"✓ {key_phrases['percentages'][0]} Diagnostic Accuracy")
        
        features.append("✓ Instant Results in Minutes")
        
        if key_phrases['conditions']:
            conditions_text = ", ".join(key_phrases['conditions'][:2])
            features.append(f"✓ Detects {conditions_text.title()}")
        
        features.append("✓ 24/7 AI-Powered Analysis")
        
        return features[:4]