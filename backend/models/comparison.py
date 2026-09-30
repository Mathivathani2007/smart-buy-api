from typing import Any, Dict, List
from pydantic import BaseModel, Field


class ComparisonRequest(BaseModel):
    product_name: str = Field(min_length=2, max_length=160)
    brand: str = ""
    category: str = ""
    keywords: List[str] = []


class ComparisonResponse(BaseModel):
    products: List[Dict[str, Any]]
    recommendation: Dict[str, Any]
    review_insights: Dict[str, Any]
