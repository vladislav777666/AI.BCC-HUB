from fastapi import FastAPI
from app.models.rank import RankRequest, RankResponse
from app.services.model_loader import load_model
from app.services.preprocessor import preprocess
import os
import torch
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from typing import List, Dict

app = FastAPI()

MODEL_PATH = os.getenv("MODEL_PATH", "/models/model.pkl")
model = load_model(MODEL_PATH)

@app.post("/ai/rank", response_model=RankResponse)
def rank(req: RankRequest):
    features = req.features
    X = preprocess(features)
    with torch.no_grad():
        embedding = model.encoder(torch.tensor(X, dtype=torch.float32)).numpy()
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(embedding.reshape(1, -1))
    cluster = KMeans(n_clusters=9, random_state=42).fit(X_scaled).labels_[0]
    benefits = calculate_benefits(features)
    ranked = sorted(benefits.items(), key=lambda x: x[1], reverse=True)
    ranked_list = [{"product": p, "score": s} for p, s in ranked]
    best = ranked_list[0]["product"]
    confidence = ranked_list[0]["score"] / sum([s for _, s in ranked]) if sum([s for _, s in ranked]) > 0 else 0.5
    explain_list = [{"text": f"12 поездок на такси — 27 400 ₸", "impact": 0.12}]
    variables = {"month": "август", "trip_count": 12, "estimated_cashback": "1 100 ₸"}
    template = {"template_id": "travel_01", "variables": variables}
    return RankResponse(
        client_code=req.client_code,
        best_product=best,
        ranked_products=ranked_list,
        explain=explain_list,
        suggested_template=template,
        confidence=confidence,
        model_version="v1.0.0"
    )

def calculate_benefits(features: Dict) -> Dict:
    spend_by_cat = features['spend_by_category']
    balance = features['avg_monthly_balance_KZT']
    total_spend = features['spend_3m_total']
    benefits = {}
    travel_spend = sum(spend_by_cat.get(cat, 0) for cat in ['Путешествия', 'Отели', 'Такси'])
    benefits["Карта для путешествий"] = travel_spend * 0.04 / 3
    cb_rate = 0.02
    if balance > 6000000:
        cb_rate = 0.04
    elif balance > 1000000:
        cb_rate = 0.03
    premium_spend = sum(spend_by_cat.get(cat, 0) for cat in ['Ювелирные украшения', 'Косметика и Парфюмерия', 'Кафе и рестораны'])
    benefits["Премиальная карта"] = (total_spend * cb_rate + premium_spend * 0.04) / 3
    top_spend = sum(spend_by_cat.get(cat, 0) for cat in features['top3_categories'])
    online_spend = sum(spend_by_cat.get(cat, 0) for cat in ['Смотрим дома', 'Играем дома', 'Кино'])
    benefits["Кредитная карта"] = (top_spend * 0.1 + online_spend * 0.1) / 3
    fx_amount = features['fx_tx_count_3m'] * 5000
    benefits["Обмен валют"] = fx_amount * 0.005 / 3
    loan_amount = features.get('large_out', 0)
    benefits["Кредит наличными"] = loan_amount * 0.05 / 3
    benefits["Депозит Мультивалютный"] = balance * 0.145 / 12
    benefits["Депозит Сберегательный"] = balance * 0.165 / 12
    benefits["Депозит Накопительный"] = balance * 0.155 / 12
    invest_amount = features.get('invest_count', 0) * 10000
    benefits["Инвестиции"] = invest_amount * 0.1 / 12
    gold_amount = features.get('gold_count', 0) * 20000
    benefits["Золотые слитки"] = gold_amount * 0.05 / 12
    return benefits

@app.get("/ai/health")
def health():
    return {"status": "ok"}

@app.get("/ai/version")
def version():
    return {"model_version": "v1.0.0"}