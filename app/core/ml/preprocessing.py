import numpy as np
from PIL import Image

def validate_image(image_path):
    """
    Validate that file is a real image
    
    Args:
        image_path: Path to image file
    
    Returns:
        bool: True if valid image, False otherwise
    """
    try:
        # Try to open and verify image with Pillow
        img = Image.open(image_path)
        img.verify()
        
        # Re-open to check format (verify closes the file)
        img = Image.open(image_path)
        if img.format.lower() not in ['png', 'jpeg', 'jpg']:
            return False
        
        return True
    except Exception as e:
        print(f"Image validation failed: {e}")
        return False


def preprocess_image(image_path, target_size=(224, 224)):
    """
    Preprocess image for model prediction
    
    Args:
        image_path: Path to image file
        target_size: Target size tuple (height, width)
    
    Returns:
        numpy array: Preprocessed image ready for model
    """
    # Load image
    img = Image.open(image_path)
    
    # Convert to RGB if needed (handle RGBA, grayscale, etc.)
    if img.mode != 'RGB':
        img = img.convert('RGB')
    
    # Resize to target size
    img = img.resize(target_size, Image.LANCZOS)
    
    # Convert to numpy array
    img_array = np.array(img)
    
    # Normalize pixel values to [0, 1]
    img_array = img_array.astype('float32') / 255.0
    
    # Add batch dimension
    img_array = np.expand_dims(img_array, axis=0)
    
    return img_array


def preprocess_base64_image(base64_string, target_size=(224, 224)):
    """
    Preprocess base64 encoded image
    
    Args:
        base64_string: Base64 encoded image string
        target_size: Target size tuple (height, width)
    
    Returns:
        numpy array: Preprocessed image ready for model
    """
    import base64
    from io import BytesIO
    
    # Remove data URL prefix if present
    if 'base64,' in base64_string:
        base64_string = base64_string.split('base64,')[1]
    
    # Decode base64
    image_bytes = base64.b64decode(base64_string)
    
    # Load image from bytes
    img = Image.open(BytesIO(image_bytes))
    
    # Convert to RGB
    if img.mode != 'RGB':
        img = img.convert('RGB')
    
    # Resize
    img = img.resize(target_size, Image.LANCZOS)
    
    # Convert to array and normalize
    img_array = np.array(img).astype('float32') / 255.0
    
    # Add batch dimension
    img_array = np.expand_dims(img_array, axis=0)
    
    return img_array
