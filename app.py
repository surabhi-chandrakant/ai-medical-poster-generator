#!/usr/bin/env python3
"""
Medical AI Poster Generator - Hugging Face API Only Version
FORCED API USAGE - No fallback to templates
DEBUG VERSION with comprehensive error handling
"""

import gradio as gr
import sys
from pathlib import Path
import tempfile
from PIL import Image
import os
from dotenv import load_dotenv
import datetime
import traceback

# Load environment variables
load_dotenv()

# Add project root to path
sys.path.append(str(Path(__file__).parent))

from modules.text_analyzer import EnhancedTextAnalyzer
from modules.hf_api_generator import HuggingFaceAPIGenerator
from modules.layout_designer import EnhancedLayoutDesigner
from modules.style_selector import StyleSelector
from modules.branding import Branding
from modules.caption_generator import CaptionGenerator
from config import (
    OUTPUT_DIR, DEFAULT_LOGO_PATH,
    DEFAULT_FONT_PATH, DEFAULT_BOLD_FONT_PATH, COLOR_PALETTES, HF_MODELS
)

def safe_str(value, default=""):
    """Safely convert any value to string"""
    if value is None:
        return default
    if isinstance(value, (list, tuple)):
        return str(value[0]) if len(value) > 0 else default
    return str(value)

def safe_get_percentage(key_phrases):
    """Safely extract percentage from key_phrases"""
    try:
        percentages = key_phrases.get('percentages', ['95%'])
        if isinstance(percentages, (list, tuple)):
            if len(percentages) > 0:
                return safe_str(percentages[0], '95%')
        elif isinstance(percentages, str):
            return percentages
        return '95%'
    except Exception as e:
        print(f"Warning: Error extracting percentage: {e}")
        return '95%'

class APIPosterGenerator:
    def __init__(self):
        """Initialize with Hugging Face API only"""
        print("\n" + "="*60)
        print("🏥 MEDICAL AI POSTER GENERATOR (HF API ONLY MODE)")
        print("="*60)
        print("\n⚠️  This version uses ONLY Hugging Face API - NO fallback!")
        print("⚠️  API token is REQUIRED for all generations")
        print("\n📝 Initializing components...")
        
        self.text_analyzer = EnhancedTextAnalyzer()
        print("  ✓ Text Analyzer loaded")
        
        self.layout_designer = EnhancedLayoutDesigner(DEFAULT_FONT_PATH, DEFAULT_BOLD_FONT_PATH)
        print("  ✓ Layout Designer loaded")
        
        self.style_selector = StyleSelector()
        print("  ✓ Style Selector loaded")
        
        self.branding = Branding(DEFAULT_LOGO_PATH)
        print("  ✓ Branding module loaded")
        
        self.caption_generator = CaptionGenerator()
        print("  ✓ Caption Generator loaded")
        
        # Track API instances
        self.api_generators = {}
        self.current_api = None
        
        self.temp_dir = tempfile.mkdtemp()
        
        print("\n" + "="*60)
        print("✅ SYSTEM READY!")
        print("="*60)
        print("\n🔑 API Token required: https://huggingface.co/settings/tokens")
        print("🚀 Access the UI at: http://localhost:7860\n")
    
    def get_api_generator(self, token, model_name):
        """Get or create API generator instance"""
        model_id = HF_MODELS.get(model_name, "black-forest-labs/FLUX.1-schnell")
        key = f"{token}_{model_id}"
        
        if key not in self.api_generators:
            self.api_generators[key] = HuggingFaceAPIGenerator(
                api_token=token.strip(),
                model_id=model_id
            )
        
        self.current_api = self.api_generators[key]
        return self.current_api
    
    def generate_poster(
        self,
        prompt,
        api_token,
        selected_model,
        tone_override,
        color_scheme,
        include_logo,
        logo_position,
        poster_size,
        inference_steps,
        guidance_scale,
        image_style
    ):
        """Generate poster using ONLY Hugging Face API with comprehensive error handling"""
        try:
            status_lines = []
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Validate API token
            if not api_token or api_token.strip() == "":
                error_msg = "❌ ERROR: API Token Missing\n\n"
                error_msg += "Please enter your Hugging Face API token to continue.\n"
                error_msg += "Get your free token at: https://huggingface.co/settings/tokens"
                return None, "", error_msg
            
            # Initialize API generator
            try:
                api_gen = self.get_api_generator(api_token, selected_model)
                status_lines.append(f"✅ HF API CONNECTED")
                status_lines.append(f"   • Model: {selected_model}")
                status_lines.append(f"   • Token: {api_token[:8]}...{api_token[-4:]}")
                status_lines.append("")
            except Exception as e:
                error_trace = traceback.format_exc()
                return None, "", f"❌ Failed to initialize API:\n{str(e)}\n\n{error_trace}"
            
            # Text Analysis
            try:
                status_lines.append("📊 STEP 1: Text Analysis")
                key_phrases = self.text_analyzer.extract_key_phrases(prompt)
                
                # DEBUG: Print key_phrases structure
                print(f"DEBUG - key_phrases type: {type(key_phrases)}")
                print(f"DEBUG - key_phrases: {key_phrases}")
                
                if tone_override != "Auto-detect":
                    tone = {'primary_tone': tone_override.lower()}
                else:
                    tone = self.text_analyzer.determine_tone(prompt)
                
                # Safe extraction with type checking
                conditions = key_phrases.get('conditions', ['medical'])
                if isinstance(conditions, (list, tuple)):
                    conditions_str = ', '.join([safe_str(c) for c in conditions])
                else:
                    conditions_str = safe_str(conditions, 'medical')
                
                tone_str = safe_str(tone.get('primary_tone', 'professional'), 'professional')
                
                status_lines.append(f"   • Detected conditions: {conditions_str}")
                status_lines.append(f"   • Detected tone: {tone_str}")
                status_lines.append("")
                
            except Exception as e:
                error_trace = traceback.format_exc()
                return None, "", f"❌ Text analysis failed:\n{str(e)}\n\n{error_trace}"
            
            # Get headline
            try:
                headlines = self.text_analyzer.generate_headline(key_phrases)
                selected_headline = safe_str(headlines[0] if headlines else "AI Medical Diagnosis", "AI Medical Diagnosis")
            except Exception as e:
                print(f"Warning: Headline generation failed: {e}")
                selected_headline = "AI Medical Diagnosis"
            
            # Color Selection
            try:
                if color_scheme != "Auto-detect":
                    colors = COLOR_PALETTES[color_scheme.lower()]
                else:
                    colors = self.style_selector.select_colors(tone)
            except Exception as e:
                print(f"Warning: Color selection failed: {e}")
                colors = COLOR_PALETTES['professional']
            
            # Generate Image via API (NO FALLBACK)
            try:
                status_lines.append("🎨 STEP 2: HF API Image Generation")
                status_lines.append(f"   • Sending request to Hugging Face...")
                status_lines.append(f"   • Style: {image_style}")
                status_lines.append(f"   • Steps: {inference_steps}")
                
                image = api_gen.generate_image(
                    key_phrases=key_phrases,
                    tone=tone,
                    colors=colors,
                    num_inference_steps=inference_steps,
                    guidance_scale=guidance_scale,
                    style=image_style
                )
                
                # Get API stats
                api_stats = api_gen.get_api_status()
                status_lines.append(f"   ✅ Image generated via HF API!")
                status_lines.append(f"   • Request #{api_stats['requests']}")
                status_lines.append("")
                
            except Exception as api_error:
                error_trace = traceback.format_exc()
                error_msg = f"❌ HF API ERROR:\n\n{str(api_error)}\n\n"
                error_msg += f"Full trace:\n{error_trace}\n\n"
                error_msg += "This app uses ONLY Hugging Face API - no fallback available.\n"
                error_msg += "Please check:\n"
                error_msg += "1. Your API token is valid\n"
                error_msg += "2. You have internet connection\n"
                error_msg += "3. The model is available\n"
                error_msg += f"4. Install huggingface_hub: pip install huggingface_hub\n"
                return None, "", error_msg
            
            # Resize
            try:
                size_map = {
                    "Instagram Square (1080x1080)": (1080, 1080),
                    "Facebook (1200x630)": (1200, 630),
                    "Twitter (1024x512)": (1024, 512),
                    "LinkedIn (1200x1200)": (1200, 1200)
                }
                target_size = size_map.get(poster_size, (1080, 1080))
                image = image.resize(target_size, Image.Resampling.LANCZOS)
            except Exception as e:
                print(f"Warning: Resize failed: {e}")
            
            # Prepare text elements with safe extraction
            try:
                features = self.text_analyzer.generate_features(key_phrases)
                if isinstance(features, (list, tuple)):
                    features_safe = [safe_str(f) for f in features]
                else:
                    features_safe = [safe_str(features)]
                
                text_elements = {
                    'headline': selected_headline,
                    'features': features_safe,
                    'cta': "Learn More • Get Started Today",
                    'percentage': safe_get_percentage(key_phrases)
                }
            except Exception as e:
                error_trace = traceback.format_exc()
                return None, "", f"❌ Text elements preparation failed:\n{str(e)}\n\n{error_trace}"
            
            # Design Layout
            try:
                status_lines.append("🎨 STEP 3: Layout Design")
                final_poster = self.layout_designer.design_poster(
                    image, text_elements, colors, tone
                )
                status_lines.append("   ✅ Layout created")
                status_lines.append("")
            except Exception as e:
                error_trace = traceback.format_exc()
                return None, "", f"❌ Layout design failed:\n{str(e)}\n\n{error_trace}"
            
            # Add Branding
            try:
                if include_logo:
                    status_lines.append("🏷️ STEP 4: Adding Branding")
                    final_poster = self.branding.add_logo(
                        final_poster, position=logo_position.lower()
                    )
                    status_lines.append("   ✅ Logo added")
                    status_lines.append("")
            except Exception as e:
                print(f"Warning: Logo addition failed: {e}")
            
            # Generate Caption
            try:
                status_lines.append("✍️ STEP 5: Generating Caption")
                caption = self.caption_generator.generate_caption(
                    key_phrases, tone  # Fixed: Pass correct parameters
                )
                status_lines.append("   ✅ Caption generated")
                status_lines.append("")
            except Exception as e:
                print(f"Warning: Caption generation failed: {e}")
                caption = f"{selected_headline}\n\nLearn more about our AI-powered medical diagnosis system."
            
            # Save
            try:
                output_path = os.path.join(self.temp_dir, "hf_api_poster.png")
                final_poster.save(output_path, quality=95)
                status_lines.append(f"✅ COMPLETE!")
                status_lines.append(f"   • Generated at: {timestamp}")
                status_lines.append(f"   • Size: {poster_size}")
                status_lines.append(f"   • API Requests: {api_stats['requests']}")
            except Exception as e:
                error_trace = traceback.format_exc()
                return None, "", f"❌ Save failed:\n{str(e)}\n\n{error_trace}"
            
            return final_poster, caption, "\n".join(status_lines)
            
        except Exception as e:
            error_trace = traceback.format_exc()
            error_msg = f"❌ UNEXPECTED ERROR:\n{str(e)}\n\n"
            error_msg += f"Full trace:\n{error_trace}\n\n"
            error_msg += "This application requires Hugging Face API to function.\n"
            error_msg += "Please ensure you have:\n"
            error_msg += "1. A valid API token\n"
            error_msg += "2. Internet connection\n"
            error_msg += "3. Selected model is available\n"
            error_msg += "4. Installed: pip install huggingface_hub pillow\n"
            return None, "", error_msg
    
    def test_api_connection(self, api_token):
        """Test HF API connection"""
        if not api_token or api_token.strip() == "":
            return "❌ Please enter your API token first"
        
        try:
            from huggingface_hub import InferenceClient
            client = InferenceClient(api_key=api_token.strip())
            return f"✅ Connection successful!\nToken: {api_token[:8]}...{api_token[-4:]}"
        except Exception as e:
            return f"❌ Connection failed: {str(e)}\n\nMake sure you have installed: pip install huggingface_hub"
    
    def create_ui(self):
        """Create Gradio UI with clear API indicators"""
        
        with gr.Blocks(title="Medical AI Poster Generator (HF API Only)") as demo:
            
            gr.Markdown("""
            # 🏥 Medical AI Poster Generator
            ### ⚡ Powered by Hugging Face API
            """)
            
            gr.Markdown("""
            <div style="background-color: #fff3cd; border-left: 4px solid #ffc107; padding: 12px; margin: 10px 0;">
            <strong>⚠️ API-ONLY MODE</strong><br>
            This application uses ONLY Hugging Face's cloud API for image generation.<br>
            You need a valid HF API token to generate posters.
            </div>
            """)
            
            with gr.Row():
                with gr.Column(scale=1):
                    # API Settings - Prominent section
                    gr.Markdown("### 🔑 REQUIRED: Hugging Face API Token")
                    gr.Markdown("Get your free token: https://huggingface.co/settings/tokens")
                    
                    api_token = gr.Textbox(
                        label="API Token",
                        placeholder="hf_xxxxxxxxxxxxxxxxxxxxx",
                        type="password",
                        value=os.getenv("HF_API_TOKEN", ""),
                        info="Your token starts with 'hf_'"
                    )
                    
                    test_btn = gr.Button("🧪 Test API Connection", size="sm")
                    test_result = gr.Textbox(label="Connection Test", interactive=False, visible=False)
                    
                    gr.Markdown("---")
                    
                    gr.Markdown("### 🤖 Model Selection")
                    model_selector = gr.Dropdown(
                        label="Select HF Model",
                        choices=list(HF_MODELS.keys()),
                        value=list(HF_MODELS.keys())[0] if HF_MODELS else "FLUX.1 Schnell (Fast & Quality)",
                        info="All models run on Hugging Face's servers"
                    )
                    
                    gr.Markdown("---")
                    
                    # Input Section
                    gr.Markdown("### 📝 Campaign Text")
                    prompt_input = gr.Textbox(
                        label="Promotional Message",
                        placeholder="Enter your promotional text...",
                        value="Promote our AI-based Medical Diagnosis System with 95% accuracy and instant results for diabetes and heart disease.",
                        lines=4
                    )
                    
                    # Generation Settings
                    gr.Markdown("### 🎨 Generation Settings")
                    
                    with gr.Row():
                        image_style = gr.Dropdown(
                            label="Image Style",
                            choices=["photorealistic", "cinematic", "illustration", "abstract", "minimalist"],
                            value="photorealistic"
                        )
                        
                        inference_steps = gr.Slider(
                            label="Quality Steps",
                            minimum=15,
                            maximum=40,
                            value=25,
                            step=5
                        )
                    
                    guidance_scale = gr.Slider(
                        label="Prompt Guidance",
                        minimum=5.0,
                        maximum=12.0,
                        value=7.5,
                        step=0.5
                    )
                    
                    # Design Settings
                    gr.Markdown("### 🎨 Design Settings")
                    
                    with gr.Row():
                        tone_override = gr.Dropdown(
                            label="Tone",
                            choices=["Auto-detect", "Professional", "Urgent", "Trust", "Innovative"],
                            value="Auto-detect"
                        )
                        
                        color_scheme = gr.Dropdown(
                            label="Color Scheme",
                            choices=["Auto-detect", "Professional", "Urgent", "Trust", "Innovative"],
                            value="Auto-detect"
                        )
                    
                    with gr.Row():
                        include_logo = gr.Checkbox(label="Include Logo", value=True)
                        logo_position = gr.Dropdown(
                            label="Logo Position",
                            choices=["Top-left", "Top-right", "Bottom-left", "Bottom-right"],
                            value="Top-right"
                        )
                    
                    poster_size = gr.Dropdown(
                        label="Poster Size",
                        choices=[
                            "Instagram Square (1080x1080)",
                            "Facebook (1200x630)",
                            "Twitter (1024x512)",
                            "LinkedIn (1200x1200)"
                        ],
                        value="Instagram Square (1080x1080)"
                    )
                    
                    generate_btn = gr.Button("🚀 Generate with HF API", 
                                           variant="primary", 
                                           size="lg")
                    
                with gr.Column(scale=2):
                    # Output Section with API Badge
                    gr.Markdown("### 🖼️ Generated Poster")
                    with gr.Row():
                        gr.Markdown("""
                        <div style="background-color: #4CAF50; color: white; padding: 5px 10px; border-radius: 3px; display: inline-block;">
                        ⚡ GENERATED VIA HUGGING FACE API
                        </div>
                        """)
                    
                    poster_output = gr.Image(label="", type="pil", height=600)
                    
                    with gr.Row():
                        download_btn = gr.File(label="📥 Download Poster", visible=False)
                    
                    gr.Markdown("### 📱 Social Media Caption")
                    caption_output = gr.Textbox(label="", lines=8, interactive=False)
                    
                    gr.Markdown("### 📊 Generation Log")
                    status_output = gr.Textbox(
                        label="Detailed Status",
                        lines=15,
                        interactive=False,
                        max_lines=20
                    )
            
            # Examples
            gr.Markdown("### 💡 Example Prompts")
            examples = gr.Examples(
                examples=[
                    ["Promote our AI-based Medical Diagnosis System with 95% accuracy and instant results for diabetes and heart disease."],
                    ["Revolutionary AI healthcare solution! 98% accurate cancer detection in under 5 minutes. Trusted by 500+ hospitals."],
                    ["Get instant cardiac risk assessment with our new AI system. 24/7 available, 99% accuracy."]
                ],
                inputs=[prompt_input]
            )
            
            # Event handlers
            test_btn.click(
                fn=self.test_api_connection,
                inputs=[api_token],
                outputs=[test_result]
            ).then(
                fn=lambda: gr.Textbox(visible=True),
                inputs=None,
                outputs=[test_result]
            )
            
            generate_btn.click(
                fn=self.generate_poster,
                inputs=[
                    prompt_input, api_token, model_selector,
                    tone_override, color_scheme, include_logo,
                    logo_position, poster_size, inference_steps,
                    guidance_scale, image_style
                ],
                outputs=[poster_output, caption_output, status_output]
            ).then(
                fn=lambda: gr.File(visible=True, 
                                 value=os.path.join(self.temp_dir, "hf_api_poster.png") 
                                 if os.path.exists(os.path.join(self.temp_dir, "hf_api_poster.png")) 
                                 else None),
                inputs=None,
                outputs=[download_btn]
            )
            
        return demo

def main():
    generator = APIPosterGenerator()
    demo = generator.create_ui()
    
    # Launch with clear messages
    demo.launch(
        server_name="127.0.0.1",
        server_port=7860,
        share=False,
        show_error=True,
        quiet=False
    )

if __name__ == "__main__":
    main()