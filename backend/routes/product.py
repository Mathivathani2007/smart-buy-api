from fastapi import APIRouter
from services.product_matching import find_matches
from services.recommendation import build_recommendation
from services.review_analyzer import analyze_reviews

router = APIRouter()


@router.get("/demo/products")
def demo_products():
    products = find_matches(["demo"], fallback_to_demo=True)
    return {"products": products, "recommendation": build_recommendation(products), "review_insights": analyze_reviews(products)}
