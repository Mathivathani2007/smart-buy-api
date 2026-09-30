from typing import Any, Dict, List


def score_products(products: List[Any]):
    prices = [p.price for p in products if p.price is not None]
    max_reviews = max((p.review_count for p in products), default=1)
    min_price = min(prices, default=0)
    max_price = max(prices, default=1)
    for product in products:
        price_score = round(100 - ((product.price - min_price) / max(max_price - min_price, 1) * 100)) if product.price is not None else 50
        rating_score = round((product.rating or 0) / 5 * 100)
        review_score = round(min(product.review_count / max_reviews, 1) * 100)
        sentiment_score = 89
        product.smartbuy_score = round(price_score * .35 + rating_score * .25 + sentiment_score * .2 + review_score * .1 + product.match_score * .1)


def build_recommendation(products: List[Any]) -> Dict[str, Any]:
    score_products(products)
    best = max(products, key=lambda item: item.smartbuy_score)
    cheapest = min((p for p in products if p.price is not None), key=lambda item: item.price, default=best)
    highest_rated = max(products, key=lambda item: item.rating or 0)
    return {
        "best_platform": best.platform,
        "best_product": best.product_name,
        "best_price": best.price,
        "smartbuy_score": best.smartbuy_score,
        "cheapest_platform": cheapest.platform,
        "highest_rated_platform": highest_rated.platform,
        "why": f"{best.platform} provides the strongest overall balance of price, rating, review confidence and product match.",
        "breakdown": {"price": 35, "rating": 25, "sentiment": 20, "reviews": 10, "match": 10},
    }
