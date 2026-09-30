from services.ai_service import identify_product


def identify(image, filename="", content_type="image/jpeg"):
    return identify_product(image, filename, content_type)
