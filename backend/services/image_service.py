from io import BytesIO
from PIL import Image, UnidentifiedImageError

MAX_IMAGE_BYTES = 8 * 1024 * 1024
ALLOWED_TYPES = {"image/jpeg", "image/png", "image/webp"}


def validate_image(content: bytes, content_type: str) -> Image.Image:
    if not content or len(content) > MAX_IMAGE_BYTES:
        raise ValueError("The image is empty or larger than 8 MB.")
    if content_type not in ALLOWED_TYPES:
        raise ValueError("Please upload a JPG, PNG or WEBP image.")
    try:
        image = Image.open(BytesIO(content))
        image.verify()
        return Image.open(BytesIO(content))
    except (UnidentifiedImageError, OSError) as exc:
        raise ValueError("This image could not be read. Please try another file.") from exc
