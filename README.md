# 🏥 Medical AI Poster Generator

**Automatically create professional social media posters for AI-based medical diagnosis systems using advanced NLP and AI image generation.**

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

[![HuggingFace](https://img.shields.io/badge/🤗-HuggingFace-orange)](https://huggingface.co/)

---
# Live app :
[![Live Demo](https://img.shields.io/badge/🚀-Live%20Demo-green)](https://huggingface.co/spaces/surabhic/ai-medical-poster-generator)


## 📋 Overview

The **Medical AI Poster Generator** combines **Natural Language Processing (NLP)** with **Hugging Face's Inference API** to create stunning, customized promotional materials for medical AI systems. Simply input your promotional text, and get a professional poster with auto-generated social media caption!

### ✨ Key Features

| Feature | Description |
|---------|-------------|
| 🤖 **AI Image Generation** | Uses Hugging Face's top models (FLUX, SDXL) - no local GPU needed |
| 📝 **Smart Text Analysis** | Extracts medical conditions, accuracy percentages, and tone automatically |
| 🎨 **Dynamic Layouts** | Professional poster designs with automatic text placement |
| 🎭 **Tone Detection** | Identifies tone (professional, urgent, trust, innovative) and adjusts colors |
| 🏷️ **Auto Branding** | Adds your company logo with customizable positioning |
| 📱 **Social Media Ready** | Multiple formats: Instagram, Facebook, Twitter, LinkedIn |
| 📝 **Caption Generation** | Creates engaging captions with relevant hashtags |

---

## 🎯 Demo

**Input:**
```
"Promote our AI-based Medical Diagnosis System with 95% accuracy 
and instant results for diabetes and heart disease."
```

**Output:**
- ✅ Professional medical poster (1080x1080)
- ✅ Social media caption with hashtags
- ✅ Customized to your brand colors
- ✅ Ready to post!

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Internet connection
- HuggingFace API token (free)

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/surabhi-chandrakant/ai-medical-poster-generator.git
cd ai-medical-poster-generator

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Download NLTK data
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('averaged_perceptron_tagger')"

# 5. Set up your API token
echo "HF_API_TOKEN=your_token_here" > .env

# 6. Run the application
python app.py
```

### Get Your HuggingFace API Token

1. Go to [https://huggingface.co/settings/tokens](https://huggingface.co/settings/tokens)
2. Click "New token"
3. Copy the token (starts with `hf_`)
4. Add to `.env` file or enter in the UI

---

## 📁 Project Structure

```
medical_ai_poster_generator/
│
├── app.py                          # Main Gradio application
├── config.py                       # Configuration settings
├── requirements.txt                # Python dependencies
├── .env                            # Environment variables (API token)
├── README.md                       # Documentation
│
├── modules/                        # Core modules
│   ├── __init__.py
│   ├── text_analyzer.py           # NLP text analysis
│   ├── hf_api_generator.py        # HuggingFace API integration
│   ├── image_generator.py         # Template fallback
│   ├── layout_designer.py         # Poster layout design
│   ├── style_selector.py          # Style and color selection
│   ├── branding.py                # Logo management
│   └── caption_generator.py       # Caption generation
│
├── utils/                          # Utility functions
│   ├── __init__.py
│   └── image_utils.py             # Image helpers
│
├── assets/                         # Static assets
│   ├── logo.png                   # Your logo (optional)
│   ├── icons/                     # Medical icons
│   └── fonts/                     # Font files (optional)
│
└── output/                         # Generated posters
```

---

## 🎨 Available Models

| Model | Speed | Quality | Best For |
|-------|-------|---------|----------|
| **FLUX.1 Schnell** | ⚡⚡⚡ | ⭐⭐⭐ | Fast generation, good quality |
| **Stable Diffusion XL** | ⚡ | ⭐⭐⭐⭐⭐ | Highest quality, detailed images |
| **SDXL Turbo** | ⚡⚡⚡⚡ | ⭐⭐ | Very fast, decent quality |
| **Playground v2.5** | ⚡⚡ | ⭐⭐⭐⭐ | Aesthetic, artistic style |
| **Stable Diffusion 2.1** | ⚡⚡ | ⭐⭐⭐ | Reliable, consistent results |

---

## 🎨 Features in Detail

### 📊 Smart Text Analysis

The NLP engine automatically extracts:
- **Medical conditions** (diabetes, heart disease, cancer, etc.)
- **Accuracy percentages** (95%, 98%, etc.)
- **AI-related terms** (machine learning, automated, etc.)
- **Tone** (professional, urgent, trustworthy, innovative)

### 🎨 Visual Styles

Choose from 5 different styles:
- **Photorealistic** - Realistic medical imagery
- **Cinematic** - Dramatic, professional photography
- **Illustration** - Clean medical illustrations
- **Abstract** - Modern, abstract designs
- **Minimalist** - Simple, clean layouts

### 🎭 Color Palettes

Automatic color selection based on tone:

| Tone | Colors | Use Case |
|------|--------|----------|
| **Professional** | Dark Blue, Blue, Red | Corporate, clinical |
| **Urgent** | Deep Red, Orange | Emergency, time-sensitive |
| **Trust** | Teal, Turquoise | Healthcare, patient-focused |
| **Innovative** | Purple, Blue | Cutting-edge technology |

### 📱 Output Formats

| Platform | Dimensions | Aspect Ratio |
|----------|------------|--------------|
| Instagram Square | 1080×1080 | 1:1 |
| Facebook | 1200×630 | 1.91:1 |
| Twitter | 1024×512 | 2:1 |
| LinkedIn | 1200×1200 | 1:1 |

---

## 💡 Usage Examples

### Example 1: Diabetes Detection System

**Input:**
```
AI-powered diabetes diagnosis with 98% accuracy. Get instant results 
in under 2 minutes. Trusted by 1000+ healthcare providers.
```

**Output:**
- Poster with professional blue color scheme
- Headline: "98% Accurate AI Diagnosis for Diabetes"
- Features listed with checkmarks
- Caption with #AIHealthcare #DiabetesDetection hashtags

### Example 2: Cancer Detection

**Input:**
```
Revolutionary AI detects cancer with 95% accuracy in 5 minutes. 
Cutting-edge technology for early detection.
```

**Output:**
- Innovative purple/blue color scheme
- Urgent tone with dynamic layout
- Caption emphasizing breakthrough technology

---

## 🏗️ System Architecture

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  User Input     │────▶│  Text Analysis  │────▶│  Tone & Color   │
│  (Prompt)       │     │  (NLP)          │     │  Selection      │
└─────────────────┘     └─────────────────┘     └─────────────────┘
                                                         │
                                                         ▼
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  Final Poster   │◀────│  Layout Design  │◀────│  HF API Image   │
│  + Caption      │     │  + Branding     │     │  Generation     │
└─────────────────┘     └─────────────────┘     └─────────────────┘
```

---

## 🔧 Configuration

Edit `config.py` to customize:

```python
# Add custom color palettes
COLOR_PALETTES['custom'] = {
    'primary': '#YOUR_COLOR',
    'secondary': '#YOUR_COLOR',
    'accent': '#YOUR_COLOR'
}

# Add custom models
HF_MODELS['My Model'] = "model/id"

# Adjust generation settings
DEFAULT_INFERENCE_STEPS = 30
DEFAULT_GUIDANCE_SCALE = 8.0
```

---

## 🐛 Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| **"API token missing"** | Enter valid HuggingFace token in UI or `.env` file |
| **"Model loading"** | Wait 10-30 seconds, auto-retry enabled |
| **"503 Error"** | Model is loading on HF servers, will retry automatically |
| **Font warnings** | Optional - system will use defaults if custom fonts missing |
| **Slow generation** | Use FLUX.1 Schnell or SDXL Turbo for faster results |

### Debug Commands

```bash
# Test API connection
python -c "from huggingface_hub import InferenceClient; print('✅ HuggingFace module working')"

# Test text analyzer
python -c "from modules.text_analyzer import EnhancedTextAnalyzer; analyzer = EnhancedTextAnalyzer(); print('✅ Text analyzer working')"

# Check NLTK data
python -c "import nltk; print(nltk.data.find('tokenizers/punkt'))"
```

---

## 📊 Module Details

### Core Modules

1. **text_analyzer.py** - NLP engine for text analysis
   - Extracts medical conditions, percentages, tone
   - Uses NLTK for natural language processing

2. **hf_api_generator.py** - HuggingFace API integration
   - Generates images using Inference API
   - Handles retries and error cases

3. **layout_designer.py** - Poster layout engine
   - Creates professional layouts
   - Adds text with outlines and shadows

4. **style_selector.py** - Style management
   - Selects colors based on tone
   - Manages font styles

5. **branding.py** - Logo management
   - Adds company logos
   - Creates default medical logo if needed

6. **caption_generator.py** - Caption creation
   - Generates social media captions
   - Adds relevant hashtags

---

## 🔒 Security & Privacy

- ✅ API tokens stored in `.env` (never committed to git)
- ✅ No user data stored permanently
- ✅ Images processed in memory
- ✅ HTTPS for all API communications
- ✅ Temporary files auto-cleaned

---

## 📈 Performance Tips

### For Faster Generation:
- Use **FLUX.1 Schnell** or **SDXL Turbo**
- Reduce inference steps (15-20)
- Use smaller output formats

### For Better Quality:
- Use **Stable Diffusion XL**
- Increase inference steps (30-40)
- Use photorealistic style
- Add detailed descriptions

---

## 🤝 Contributing

Contributions welcome! Areas for improvement:
- Additional layout templates
- More medical icon sets
- Multi-language support
- Custom model integration
- Advanced text effects

### Development Setup

```bash
# Clone repository
git clone https://github.com/surabhi-chandrakant/ai-medical-poster-generator.git
cd ai-medical-poster-generator

# Install development dependencies
pip install -r requirements.txt
pip install pytest black flake8

# Run tests (if available)
pytest tests/
```

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **[HuggingFace](https://huggingface.co/)** - For the amazing Inference API
- **[Gradio](https://gradio.app/)** - For the easy-to-use UI framework
- **[NLTK](https://www.nltk.org/)** - For natural language processing
- **[Pillow](https://pillow.readthedocs.io/)** - For image manipulation

---

## 📧 Support

- **Issues**: [GitHub Issues](https://github.com/surabhi-chandrakant/ai-medical-poster-generator/issues)
- **Email**: surabhi.chandrakant@example.com
- **Documentation**: [Full Docs](https://github.com/surabhi-chandrakant/ai-medical-poster-generator/wiki)

---

## 📊 Stats

![GitHub stars](https://img.shields.io/github/stars/surabhi-chandrakant/ai-medical-poster-generator?style=social)
![GitHub forks](https://img.shields.io/github/forks/surabhi-chandrakant/ai-medical-poster-generator?style=social)
![GitHub watchers](https://img.shields.io/github/watchers/surabhi-chandrakant/ai-medical-poster-generator?style=social)

---

**Made with ❤️ for healthcare professionals and medical marketers**

**⭐ Star this repo if you find it useful!**
