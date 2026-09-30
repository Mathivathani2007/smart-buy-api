import base64
import json
import os
from urllib.request import Request, urlopen

from dotenv import load_dotenv
from PIL import Image
from io import BytesIO
from models.product import ProductIdentity
from services.product_matching import catalog_products

load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env"))


def _demo_identity(image: bytes = b"", filename: str = "") -> ProductIdentity:
    filename_text = filename.replace("_", " ").replace("-", " ").lower()
    for product in catalog_products():
        product_terms = product["product_name"].lower().split()
        if sum(term in filename_text for term in product_terms if len(term) > 2) >= 2:
            return ProductIdentity(
                product_name=product["product_name"], brand=product.get("brand", "Unknown"),
                category=product.get("category", "Unknown"), model=product["product_name"],
                description="Matched from the uploaded filename in demo mode.",
                keywords=[product["product_name"], product.get("brand", ""), product.get("category", "")], confidence=55,
            )
    fallback = catalog_products()[0]
    return ProductIdentity(
        product_name=fallback["product_name"],
        brand=fallback.get("brand", "Unknown"),
        category=fallback.get("category", "Unknown"),
        model=fallback["product_name"],
        description="Vision matching is unavailable, so this result uses the local demo catalog.",
        keywords=[fallback["product_name"], fallback.get("brand", ""), fallback.get("category", "")],
        confidence=40,
    )


def _catalog_prompt():
    candidates = "\n".join(
        f"- {product['product_name']} | brand: {product.get('brand', '')} | category: {product.get('category', '')} | features: {', '.join(str(value) for value in product.get('specifications', {}).values())}"
        for product in catalog_products()
    )
    return f"""Identify the product in this image using the candidate catalog below. Choose the closest candidate only when visual evidence supports it; otherwise use Product not identified. Return JSON with product_name, brand, category, model, description, keywords (array), confidence (0-100). Include the selected product name and brand in keywords. Never claim an exact model unless visible.\n\nCandidate catalog:\n{candidates}"""


def _parse_identity(text: str) -> ProductIdentity:
    text = text.strip()
    if text.startswith("```"):
        text = text.split("\n", 1)[1].rsplit("```", 1)[0].strip()
    return ProductIdentity.model_validate(json.loads(text))


def _google_identity(image: bytes, api_key: str, content_type: str) -> ProductIdentity:
    model = os.getenv("AI_MODEL", "gemini-2.0-flash")
    payload = {
        "contents": [{"parts": [
            {"text": _catalog_prompt()},
            {"inline_data": {"mime_type": content_type, "data": base64.b64encode(image).decode()}},
        ]}],
        "generationConfig": {"responseMimeType": "application/json"},
    }
    endpoint = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
    request = Request(endpoint, data=json.dumps(payload).encode(), headers={"Content-Type": "application/json"})
    with urlopen(request, timeout=30) as response:
        result = json.loads(response.read())
    text = result["candidates"][0]["content"]["parts"][0]["text"]
    return _parse_identity(text)


def _openai_identity(image: bytes, api_key: str, content_type: str) -> ProductIdentity:
    model = os.getenv("AI_MODEL", "gpt-4o-mini")
    payload = {"model": model, "response_format": {"type": "json_object"}, "messages": [{"role": "user", "content": [{"type": "text", "text": _catalog_prompt()}, {"type": "image_url", "image_url": {"url": f"data:{content_type};base64,{base64.b64encode(image).decode()}"}}]}]}
    request = Request("https://api.openai.com/v1/chat/completions", data=json.dumps(payload).encode(), headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"})
    with urlopen(request, timeout=30) as response:
        result = json.loads(response.read())
    return _parse_identity(result["choices"][0]["message"]["content"])


def _vision_identity(image: bytes, content_type: str) -> ProductIdentity | None:
    api_key = os.getenv("AI_API_KEY")
    if not api_key:
        return None
    if os.getenv("AI_PROVIDER", "google").lower() == "google":
        return _google_identity(image, api_key, content_type)
    return _openai_identity(image, api_key, content_type)


def identify_product(image, filename: str = "", content_type: str = "image/jpeg") -> ProductIdentity:
    """Use configured vision AI, with a cautious fallback when it is unavailable."""
    try:
        return _vision_identity(image, content_type) or _demo_identity(image, filename)
    except Exception:
        return _demo_identity(image, filename)
