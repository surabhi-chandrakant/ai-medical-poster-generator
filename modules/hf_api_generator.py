import os
from PIL import Image, ImageEnhance
from huggingface_hub import InferenceClient
import time

class HuggingFaceAPIGenerator:
    """
    Image generator using Hugging Face Inference API (InferenceClient)
    """
    
    def __init__(self, api_token=None, model_id="black-forest-labs/FLUX.1-schnell"):
        """
        Initialize HF API generator
        
        Args:
            api_token: Hugging Face API token
            model_id: Model to use (default: FLUX.1-schnell - fast, free, good quality)
        """
        self.api_token = api_token or os.environ.get("HF_API_TOKEN", "")
        self.model_id = model_id
        self.request_count = 0
        
        # Initialize InferenceClient
        if self.api_token:
            self.client = InferenceClient(token=self.api_token)  # Use 'token' not 'api_key'
        else:
            self.client = None
        
    def set_api_token(self, token):
        """Set or update API token"""
        self.api_token = token
        self.client = InferenceClient(token=self.api_token)
    
    def get_api_status(self):
        """Return API usage stats"""
        return {
            "model": self.model_id,
            "requests": self.request_count,
            "using_api": True,
            "token_set": bool(self.api_token),
            "method": "huggingface_hub.InferenceClient"
        }
    
    def _build_medical_prompt(self, condition, accuracy, tone, style):
        """Build professional medical prompt for API"""
        
        # Ensure all inputs are strings
        condition = str(condition) if condition else 'medical'
        accuracy = str(accuracy) if accuracy else '95%'
        tone = str(tone).lower() if tone else 'professional'
        style = str(style).lower() if style else 'photorealistic'
        
        # Base medical scene
        base_scene = f"Professional medical visualization of AI-powered {condition} diagnosis system"
        
        # Style modifiers
        style_modifiers = {
            "photorealistic": "photorealistic, ultra detailed, 8k resolution, clinical lighting, sharp focus, medical photography",
            "cinematic": "cinematic shot, dramatic lighting, professional photography, depth of field, compelling",
            "illustration": "medical illustration, scientific diagram, clean lines, anatomical accuracy, educational",
            "abstract": "abstract medical art, digital patterns, technological aesthetic, glowing elements, futuristic",
            "minimalist": "minimalist design, clean composition, simple shapes, professional, modern, flat design"
        }
        
        # Tone modifiers
        tone_modifiers = {
            "professional": "clinical accuracy, professional atmosphere, medical expertise",
            "urgent": "emergency response, critical care, urgent medical attention, red accents",
            "trust": "trustworthy healthcare, caring environment, patient-focused, warm atmosphere",
            "innovative": "cutting-edge technology, future of medicine, breakthrough innovation, holographic displays"
        }
        
        # Build prompt
        prompt_parts = [
            base_scene,
            style_modifiers.get(style, style_modifiers["photorealistic"]),
            f"{accuracy} accuracy display, digital readout, medical dashboard",
            tone_modifiers.get(tone, tone_modifiers["professional"]),
            "modern hospital setting, AI technology, digital health interface, clean medical environment",
            "high quality, detailed, sharp focus, professional lighting, 4k, masterpiece"
        ]
        
        return ", ".join(prompt_parts)
    
    def _enhance_image(self, image):
        """Basic enhancement"""
        try:
            enhancer = ImageEnhance.Contrast(image)
            image = enhancer.enhance(1.1)
            enhancer = ImageEnhance.Sharpness(image)
            image = enhancer.enhance(1.2)
            enhancer = ImageEnhance.Color(image)
            image = enhancer.enhance(1.05)
        except Exception as e:
            print(f"Enhancement warning: {e}")
        return image
    
    def generate_image(self, key_phrases, tone, colors, 
                      num_inference_steps=25,
                      guidance_scale=7.5,
                      style="photorealistic"):
        """
        Generate image using Hugging Face InferenceClient
        """
        # Check if API token is set
        if not self.api_token or not self.client:
            raise ValueError("❌ HF API TOKEN MISSING: Please enter your Hugging Face API token")
        
        # Extract and process conditions
        conditions = key_phrases.get('conditions', [])
        if conditions and len(conditions) > 0:
            condition = str(conditions[0])
        else:
            condition = 'medical'
        
        # FIXED: Handle percentages properly - extract first element if it's a list/tuple
        percentages_data = key_phrases.get('percentages', ['95%'])
        if isinstance(percentages_data, (list, tuple)) and len(percentages_data) > 0:
            percentages = str(percentages_data[0])  # Extract first element and convert to string
        elif isinstance(percentages_data, str):
            percentages = percentages_data
        else:
            percentages = '95%'
        
        # Get tone value
        if isinstance(tone, dict):
            tone_value = str(tone.get('primary_tone', 'professional'))
        else:
            tone_value = str(tone)
        
        # Build prompt
        prompt = self._build_medical_prompt(condition, percentages, tone_value, style)
        
        print(f"\n{'='*50}")
        print(f"🚀 USING HUGGING FACE INFERENCE CLIENT")
        print(f"{'='*50}")
        print(f"📤 Model: {self.model_id}")
        print(f"📤 Request #{self.request_count + 1}")
        print(f"📤 Condition: {condition}")
        print(f"📤 Accuracy: {percentages}")
        print(f"📤 Prompt: {prompt[:100]}...")
        print(f"{'='*50}")
        
        # Make API request with retry logic
        max_retries = 3
        for attempt in range(max_retries):
            try:
                # Use InferenceClient's text_to_image method with proper parameters
                image = self.client.text_to_image(
                    prompt=prompt,
                    model=self.model_id,
                    negative_prompt="blurry, bad quality, distorted, ugly, bad anatomy, watermark, text, signature, low resolution, deformed",
                    guidance_scale=guidance_scale,
                    num_inference_steps=num_inference_steps,
                    height=1024,
                    width=1024
                )
                
                # Success!
                self.request_count += 1
                image = self._enhance_image(image)
                print(f"✅ Image generated via HF API! (Request #{self.request_count})")
                return image
                    
            except Exception as e:
                error_str = str(e)
                
                # Check if model is loading
                if "loading" in error_str.lower() or "503" in error_str:
                    if attempt < max_retries - 1:
                        wait_time = 10 * (attempt + 1)
                        print(f"⏳ Model loading on HF servers. Waiting {wait_time} seconds... (Attempt {attempt + 1}/{max_retries})")
                        time.sleep(wait_time)
                        continue
                    else:
                        raise Exception("Model failed to load after multiple retries")
                
                # Check for quota/exceeded errors
                elif "quota" in error_str.lower() or "exceeded" in error_str.lower() or "429" in error_str:
                    raise Exception(f"API quota exceeded or rate limited: {error_str}")
                
                # Other errors
                if attempt < max_retries - 1:
                    print(f"⚠️ Error: {error_str}. Retrying... (Attempt {attempt + 1}/{max_retries})")
                    time.sleep(5)
                else:
                    raise Exception(f"Failed to generate image: {error_str}")
        
        raise Exception("Failed to generate image after multiple attempts")
    
    def unload_model(self):
        """Nothing to unload - API based"""
        print("✅ No local model to unload (using HF API)")
        return True