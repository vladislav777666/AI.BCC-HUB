from fastapi import APIRouter, Depends, Request, Body
from app.db.session import get_db
from app.tasks.push_tasks import send_push
from sqlalchemy.orm import Session
from app.db.models import Subscription
import json

router = APIRouter()

VAPID_PUBLIC_KEY = "<YOUR_VAPID_PUBLIC_KEY>"
VAPID_PRIVATE_KEY = "<YOUR_VAPID_PRIVATE_KEY>"
VAPID_CLAIMS = {"sub": "mailto:you@example.com"}

@router.post("/subscribe")
async def subscribe(request: Request, db: Session = Depends(get_db)):
    subscription = await request.json()
    sub = Subscription(subscription_json=subscription)
    db.add(sub)
    db.commit()
    return {"message": "Subscribed successfully"}

@router.post("/send")
def send_push_body(body: dict, db: Session = Depends(get_db)):
    client_code = body["client_code"]
    channels = body["channels"]
    override_message = body.get("override_message")
    task = send_push.delay(client_code, channels, override_message)
    return {"task_id": "..."}