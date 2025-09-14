from app.models.features import Features
from typing import Dict

def rule_based_rank(features: Features, candidates: list) -> Dict:
    scores = {}
    for product in candidates:
        if product == "Карта для путешествий":
            scores[product] = features.trips_count_3m * 0.1
        elif product == "Премиальная карта":
            scores[product] = features.avg_monthly_balance_KZT / 1000000
        else:
            scores[product] = 0.5
    
    ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    best = ranked[0][0]
    confidence = ranked[0][1]
    explain = [{"text": "Rule-based fallback", "impact": 0.5}]
    template = {"template_id": "default_01", "variables": {"month": "август", "trip_count": features.trips_count_3m}}
    return {
        "best_product": best,
        "ranked_products": [{"product": p, "score": s} for p, s in ranked],
        "explain": explain,
        "suggested_template": template,
        "confidence": confidence,
        "model_version": "fallback_v1"
    }