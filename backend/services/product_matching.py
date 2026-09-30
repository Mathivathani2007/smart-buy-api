import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import List
from models.product import MarketplaceProduct

CATALOG_PATH = Path(__file__).resolve().parent.parent / "data" / "demo_products.json"


def _catalog():
    with CATALOG_PATH.open(encoding="utf-8") as catalog_file:
        return json.load(catalog_file)["products"]


def _tokens(value):
    return {token.rstrip("s") for token in re.findall(r"[a-z0-9]+", str(value).lower()) if len(token) > 1}


def _searchable(product):
    return " ".join([
        product["product_name"],
        product.get("brand", ""),
        product.get("category", ""),
        " ".join(str(value) for value in product.get("specifications", {}).values()),
    ])


def _matches(product, terms):
    query_tokens = set().union(*(_tokens(term) for term in terms)) if terms else set()
    name_tokens = _tokens(product["product_name"])
    brand_tokens = _tokens(product.get("brand", ""))
    category_tokens = _tokens(product.get("category", ""))
    specification_tokens = _tokens(" ".join(str(value) for value in product.get("specifications", {}).values()))
    return (
        len(name_tokens & query_tokens) * 2
        + len(brand_tokens & query_tokens) * 4
        + len(category_tokens & query_tokens)
        + len(specification_tokens & query_tokens)
    )


def catalog_products():
    products = _catalog()
    seen = set()
    unique = []
    for product in products:
        if product["product_name"] not in seen:
            seen.add(product["product_name"])
            unique.append(product)
    return unique


def _listing(product, keywords):
    platform = product["platform"]
    terms = [term.lower() for term in (keywords or []) if term.strip()]
    query = "+".join(terms or ["products"])
    domain = "amazon.in" if platform == "Amazon" else f"{platform.lower()}.com"
    return MarketplaceProduct(
        **product,
        product_url=f"https://www.{domain}/search?{'k' if platform == 'Amazon' else 'q'}={query}",
        reviews=["Review sample available for this demo listing."],
        source="demo catalog",
        last_updated=datetime.now(timezone.utc).isoformat(),
        match_score=min(99, 75 + (_matches(product, terms) * 8)) if terms else 85,
    )


def search_catalog(platform: str, keywords: List[str]):
    terms = [term.lower() for term in (keywords or []) if term.strip()]
    products = [product for product in _catalog() if product["platform"] == platform]
    if terms and "demo" not in terms:
        families = {}
        for product in products:
            families.setdefault(product["product_name"], product)
        ranked = [(product, _matches(product, terms)) for product in families.values()]
        matches = [(product, score) for product, score in ranked if score]
        highest_score = max((score for _, score in matches), default=0)
        if highest_score >= 3:
            matches = [(product, score) for product, score in matches if score == highest_score]
        products = [product for product, _ in sorted(matches, key=lambda item: item[1], reverse=True)]
    return [_listing(product, terms) for product in products]


def find_best_product(identity):
    terms = [identity.product_name, identity.brand, identity.category, identity.model, *identity.keywords]
    ranked = sorted(((product, _matches(product, terms)) for product in catalog_products()), key=lambda item: item[1], reverse=True)
    if not ranked or ranked[0][1] < 2 or identity.confidence < 40:
        return None
    return ranked[0][0]


def find_matches(keywords: List[str], fallback_to_demo=False):
    from providers.amazon import AmazonProvider
    from providers.flipkart import FlipkartProvider
    from providers.meesho import MeeshoProvider
    from providers.myntra import MyntraProvider
    providers = [AmazonProvider(), FlipkartProvider(), MeeshoProvider(), MyntraProvider()]
    matches = [listing for provider in providers for listing in provider.search(keywords)]
    return matches or (find_matches(["demo"]) if fallback_to_demo else [])
