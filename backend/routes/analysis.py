from fastapi import APIRouter, File, HTTPException, UploadFile
from services.image_service import validate_image
from services.product_identification import identify
from services.product_matching import find_best_product, find_matches
from services.recommendation import build_recommendation
from services.review_analyzer import analyze_reviews

router = APIRouter()


@router.post("/analyze")
async def analyze(image: UploadFile = File(...)):
    try:
        content = await image.read()
        validated = validate_image(content, image.content_type or "")
        identity = identify(content, image.filename or "", image.content_type or "image/jpeg")
        detected_product = find_best_product(identity)
        products = find_matches([detected_product["product_name"]]) if detected_product else []
        if not products:
            detail = "We couldn't identify the product. Please upload a clearer image showing the product." if identity.confidence < 40 else "No matching product found in our current database. Try another product image."
            raise HTTPException(status_code=404, detail=detail)
        insights = analyze_reviews(products)
        recommendation = build_recommendation(products) if products else {}
        return {"identity": identity, "products": products, "recommendation": recommendation, "review_insights": insights, "match_found": bool(products), "demo_mode": True}
    except HTTPException:
        raise
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=503, detail="Analysis is temporarily unavailable. Please try again.") from exc
