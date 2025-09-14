from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services.feature_extractor import extract_features
from app.services.text_generator import generate_push_text
from app.services.tov_validator import validate_tov
from app.services.decision_enforcer import enforce_rules
from app.services.rules_engine import rule_based_rank
from app.db.models import Recommendation, RecommendationAudit
from app.models.rank import RankResponse
from app.tasks.push_tasks import send_push
import requests
import csv
from io import StringIO
from fastapi.responses import StreamingResponse

router = APIRouter()

MODEL_URL = "http://model-service:8000/ai/rank"
CANDIDATES = ["Карта для путешествий", "Премиальная карта", "Кредитная карта", "Обмен валют", "Кредит наличными", "Депозит Мультивалютный", "Депозит Сберегательный", "Депозит Накопительный", "Инвестиции", "Золотые слитки"]

@router.post("/run")
def run_batch(body: dict = {}, db: Session = Depends(get_db)):
    clients = body.get("clients", [c.client_code for c in db.query(Client).all()])
    for client_code in clients:
        try:
            preview = get_preview(client_code, db)
            rec = Recommendation(client_code=client_code, product=preview["best_product"], push_text=preview["push_preview"], confidence=preview["confidence"], model_version=preview["model_version"])
            db.add(rec)
            audit = RecommendationAudit(recommendation_id=rec.id, ranked_products=preview["ranked_products"], explain=preview["explain"], suggested_template=preview["suggested_template"], tov_meta=preview["tov_meta"])
            db.add(audit)
            send_push.delay(client_code, ["web"], preview["push_preview"])
        except:
            pass
    db.commit()
    return {"job_id": "..."}

@router.get("/{client_code}/preview")
def get_preview(client_code: int, db: Session = Depends(get_db)):
    features = extract_features(db, client_code)
    try:
        resp = requests.post(MODEL_URL, json={"client_code": client_code, "features": features.dict(), "candidates": CANDIDATES})
        resp.raise_for_status()
        rank_data = resp.json()
    except:
        rank_data = rule_based_rank(features, CANDIDATES)
    
    if not enforce_rules(features, rank_data["best_product"], rank_data["confidence"]):
        raise HTTPException(403, "Not eligible")
    
    push_text = generate_push_text(rank_data["suggested_template"]["template_id"], rank_data["suggested_template"]["variables"])
    tov_meta = validate_tov(push_text)
    if tov_meta["violations"]:
        raise HTTPException(400, "TOV violation")
    
    client = db.query(Client).filter(Client.client_code == client_code).first()
    preview = {
        "client_code": client_code,
        "client_name": client.name,
        "best_product": rank_data["best_product"],
        "ranked_products": rank_data["ranked_products"],
        "suggested_template": rank_data["suggested_template"],
        "push_preview": push_text,
        "tov_meta": tov_meta,
        "explain": rank_data["explain"],
        "model_version": rank_data["model_version"],
        "confidence": rank_data["confidence"]
    }
    send_push.delay(client_code, ["web"], push_text)
    return preview

@router.get("/csv")
def export_csv(db: Session = Depends(get_db)):
    recs = db.query(Recommendation).all()
    output = StringIO()
    writer = csv.writer(output, quoting=csv.QUOTE_ALL)
    writer.writerow(["client_code", "product", "push_notification"])
    for rec in recs:
        writer.writerow([rec.client_code, rec.product, rec.push_text])
    return StreamingResponse(iter([output.getvalue()]), media_type="text/csv", headers={"Content-Disposition": "attachment; filename=recommendations.csv"})