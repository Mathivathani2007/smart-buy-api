from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class ProductIdentity(BaseModel):
    product_name: str
    brand: str
    category: str
    model: str
    description: str
    keywords: List[str]
    confidence: int = Field(ge=0, le=100)


class MarketplaceProduct(BaseModel):
    platform: str
    product_name: str
    price: Optional[float] = None
    original_price: Optional[float] = None
    currency: str = "INR"
    rating: Optional[float] = Field(default=None, ge=0, le=5)
    review_count: int = Field(default=0, ge=0)
    product_url: str
    image_url: str
    availability: str = "Unknown"
    specifications: Dict[str, Any] = {}
    reviews: List[str] = []
    source: str = "demo"
    last_updated: str
    match_score: int = Field(default=0, ge=0, le=100)
    smartbuy_score: int = Field(default=0, ge=0, le=100)


class AnalyzeResponse(BaseModel):
    identity: ProductIdentity
    products: List[MarketplaceProduct]
    recommendation: Dict[str, Any]
    review_insights: Dict[str, Any]
    demo_mode: bool = True
