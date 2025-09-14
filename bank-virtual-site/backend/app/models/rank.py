from pydantic import BaseModel
from typing import List, Dict

class RankRequest(BaseModel):
    client_code: int
    features: Dict
    candidates: List[str]

class RankResponse(BaseModel):
    client_code: int
    best_product: str
    ranked_products: List[Dict[str, float]]
    explain: List[Dict[str, float]]
    suggested_template: Dict
    confidence: float
    model_version: str