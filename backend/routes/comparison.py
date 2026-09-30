from fastapi import APIRouter
from models.comparison import ComparisonRequest
from services.product_matching import find_matches
from services.recommendation import build_recommendation
from services.review_analyzer import analyze_reviews

router = APIRouter()


@router.post("/compare")
def compare(request: ComparisonRequest):
    products = find_matches(request.keywords or [request.product_name])
    return {"products": products, "recommendation": build_recommendation(products), "review_insights": analyze_reviews(products)}


@router.post("/reviews/analyze")
def review_analysis(request: ComparisonRequest):
    products = find_matches(request.keywords or [request.product_name])
    return analyze_reviews(products)
