from PIL import Image
import os

def resize_image(image, max_size=(1080, 1080)):
    """Resize image while maintaining aspect ratio"""
    image.thumbnail(max_size, Image.Resampling.LANCZOS)
    return image

def save_poster(poster, output_path, filename):
    """Save generated poster"""
    os.makedirs(output_path, exist_ok=True)
    base_filename = filename.replace(" ", "_").lower()
    full_path = os.path.join(output_path, f"{base_filename}.png")
    poster.save(full_path, "PNG", quality=95)
    return full_path