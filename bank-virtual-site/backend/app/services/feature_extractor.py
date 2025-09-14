from sqlalchemy.orm import Session
from app.db.models import Client, Transaction, Transfer
from app.models.features import Features
from typing import Dict
from datetime import datetime, timedelta

def extract_features(db: Session, client_code: int) -> Features:
    client = db.query(Client).filter(Client.client_code == client_code).first()
    if not client:
        raise ValueError("Client not found")
    
    three_months_ago = datetime.now() - timedelta(days=90)
    transactions = db.query(Transaction).filter(Transaction.client_code == client_code, Transaction.date >= three_months_ago).all()
    transfers = db.query(Transfer).filter(Transfer.client_code == client_code, Transfer.date >= three_months_ago).all()
    
    spend_by_category: Dict[str, float] = {}
    spend_3m_total = 0.0
    trips_count_3m = 0
    salary_incoming_avg = 0.0
    fx_tx_count_3m = 0
    large_out = 0.0
    invest_count = 0
    gold_count = 0
    
    for tx in transactions:
        amt = float(tx.amount)
        spend_by_category[tx.category] = spend_by_category.get(tx.category, 0) + amt
        spend_3m_total += amt
        if tx.category in ["Такси", "Путешествия", "Отели"]:
            trips_count_3m += 1
    
    for tf in transfers:
        amt = float(tf.amount)
        if tf.type in ["salary_in", "stipend_in"] and tf.direction == "in":
            salary_incoming_avg += amt / 3
        if "fx" in tf.type:
            fx_tx_count_3m += 1
        if tf.direction == "out" and amt > 100000:
            large_out += amt
        if "invest" in tf.type:
            invest_count += 1
        if "gold" in tf.type:
            gold_count += 1
    
    top3_categories = sorted(spend_by_category, key=spend_by_category.get, reverse=True)[:3]
    
    return Features(
        client_code=client_code,
        age=client.age,
        status=client.status,
        city=client.city,
        avg_monthly_balance_KZT=float(client.avg_monthly_balance_KZT),
        top3_categories=top3_categories,
        spend_by_category=spend_by_category,
        spend_3m_total=spend_3m_total,
        trips_count_3m=trips_count_3m,
        salary_incoming_avg=salary_incoming_avg,
        deposit_balance=float(client.avg_monthly_balance_KZT),
        fx_tx_count_3m=fx_tx_count_3m,
        push_opt_in=client.push_opt_in,
        large_out=large_out,
        invest_count=invest_count,
        gold_count=gold_count
    )