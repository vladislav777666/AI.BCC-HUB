from sqlalchemy import Column, Integer, String, Numeric, Boolean, DateTime, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Client(Base):
    __tablename__ = "clients"
    client_code = Column(Integer, primary_key=True)
    name = Column(String)
    status = Column(String)
    age = Column(Integer)
    city = Column(String)
    avg_monthly_balance_KZT = Column(Numeric)
    push_opt_in = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True, autoincrement=True)
    client_code = Column(Integer)
    date = Column(DateTime)
    category = Column(String)
    amount = Column(Numeric)
    currency = Column(String)

class Transfer(Base):
    __tablename__ = "transfers"
    id = Column(Integer, primary_key=True, autoincrement=True)
    client_code = Column(Integer)
    date = Column(DateTime)
    type = Column(String)
    direction = Column(String)
    amount = Column(Numeric)
    currency = Column(String)

class Recommendation(Base):
    __tablename__ = "recommendations"
    id = Column(Integer, primary_key=True, autoincrement=True)
    client_code = Column(Integer)
    product = Column(String)
    push_text = Column(String)
    rank_position = Column(Integer)
    push_quality_score = Column(Integer)
    model_version = Column(String)
    confidence = Column(Numeric)
    created_at = Column(DateTime, default=datetime.utcnow)

class RecommendationAudit(Base):
    __tablename__ = "recommendation_audit"
    id = Column(Integer, primary_key=True, autoincrement=True)
    recommendation_id = Column(Integer, ForeignKey("recommendations.id"))
    ranked_products = Column(JSON)
    explain = Column(JSON)
    suggested_template = Column(JSON)
    tov_meta = Column(JSON)

class PushLog(Base):
    __tablename__ = "push_logs"
    id = Column(Integer, primary_key=True, autoincrement=True)
    recommendation_id = Column(Integer, ForeignKey("recommendations.id"))
    client_code = Column(Integer)
    channel = Column(String)
    status = Column(String)
    provider_response = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)

class Subscription(Base):
    __tablename__ = "subscriptions"
    id = Column(Integer, primary_key=True, autoincrement=True)
    subscription_json = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)