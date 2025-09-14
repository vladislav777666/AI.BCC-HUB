from app.models.features import Features

def enforce_rules(features: Features, product: str, confidence: float) -> bool:
    if not features.push_opt_in:
        return False
    if product == "Премиальная карта" and features.avg_monthly_balance_KZT < 1000000:
        return False
    if confidence < 0.5:
        return False
    return True