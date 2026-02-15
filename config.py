"""
Configuration file for Medical AI Poster Generator
Updated for Hugging Face router.huggingface.co endpoint
"""

from pathlib import Path

# Directories
BASE_DIR = Path(__file__).parent
OUTPUT_DIR = BASE_DIR / "outputs"
ASSETS_DIR = BASE_DIR / "assets"

# Create directories if they don't exist
OUTPUT_DIR.mkdir(exist_ok=True)
ASSETS_DIR.mkdir(exist_ok=True)

# Assets
DEFAULT_LOGO_PATH = ASSETS_DIR / "logo.png"
DEFAULT_FONT_PATH = ASSETS_DIR / "fonts" / "Roboto-Regular.ttf"
DEFAULT_BOLD_FONT_PATH = ASSETS_DIR / "fonts" / "Roboto-Bold.ttf"

# Hugging Face Models (working with router.huggingface.co)
# These models are confirmed to work with the new endpoint
HF_MODELS = {
    "FLUX.1 Schnell (Fast & Quality)": "black-forest-labs/FLUX.1-schnell",
    "Stable Diffusion XL (Best Quality)": "stabilityai/stable-diffusion-xl-base-1.0",
    "SDXL Turbo (Fastest)": "stabilityai/sdxl-turbo",
    "Playground v2.5 (Aesthetic)": "playgroundai/playground-v2.5-1024px-aesthetic",
    "Stable Diffusion 2.1 (Reliable)": "stabilityai/stable-diffusion-2-1",
    "Kandinsky 2.2 (Artistic)": "kandinsky-community/kandinsky-2-2-decoder",
}

# Color Palettes
COLOR_PALETTES = {
    'professional': {
        'primary': '#2C3E50',      # Dark blue-grey
        'secondary': '#3498DB',    # Professional blue
        'accent': '#E74C3C',       # Red accent
        'background': '#ECF0F1',   # Light grey
        'text': '#2C3E50'
    },
    'urgent': {
        'primary': '#C0392B',      # Deep red
        'secondary': '#E74C3C',    # Bright red
        'accent': '#F39C12',       # Orange
        'background': '#FADBD8',   # Light red
        'text': '#2C3E50'
    },
    'trust': {
        'primary': '#16A085',      # Teal
        'secondary': '#1ABC9C',    # Turquoise
        'accent': '#3498DB',       # Blue
        'background': '#D5F4E6',   # Light green
        'text': '#2C3E50'
    },
    'innovative': {
        'primary': '#8E44AD',      # Purple
        'secondary': '#9B59B6',    # Light purple
        'accent': '#3498DB',       # Blue
        'background': '#EBD9FC',   # Light purple
        'text': '#2C3E50'
    },
    'medical': {
        'primary': '#2980B9',      # Medical blue
        'secondary': '#3498DB',    # Light blue
        'accent': '#27AE60',       # Medical green
        'background': '#EBF5FB',   # Very light blue
        'text': '#2C3E50'
    }
}

# Image Generation Settings
DEFAULT_IMAGE_SIZE = (1024, 1024)
DEFAULT_INFERENCE_STEPS = 25
DEFAULT_GUIDANCE_SCALE = 7.5

# Text Generation Settings
MAX_HEADLINE_LENGTH = 60
MAX_FEATURES = 4
MAX_CAPTION_LENGTH = 280

# Branding Settings
LOGO_SIZES = {
    'small': (80, 80),
    'medium': (120, 120),
    'large': (160, 160)
}

DEFAULT_LOGO_SIZE = 'medium'
DEFAULT_LOGO_OPACITY = 0.9

# Layout Settings
PADDING = 40
SECTION_SPACING = 30
ELEMENT_SPACING = 15

# Font Sizes
FONT_SIZES = {
    'headline': 52,
    'subheadline': 36,
    'body': 24,
    'caption': 18,
    'small': 14
}

# API Settings
HF_API_TIMEOUT = 120  # seconds
HF_API_MAX_RETRIES = 3
HF_API_RETRY_DELAY = 10  # seconds

# Environment
import os
from dotenv import load_dotenv
load_dotenv()

HF_API_TOKEN = os.getenv("HF_API_TOKEN", "")