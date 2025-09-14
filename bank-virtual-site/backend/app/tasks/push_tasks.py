from app.main import celery
from app.db.session import SessionLocal
from app.db.models import PushLog, Subscription
from pywebpush import webpush, WebPushException
import json
from app.api.push import VAPID_PRIVATE_KEY, VAPID_CLAIMS

@celery.task
def send_push(client_code: int, channels: list, message: str = None):
    db = SessionLocal()
    subs = db.query(Subscription).all()
    for sub in subs:
        try:
            webpush(
                subscription_info=sub.subscription_json,
                data=json.dumps({"title": "Новое уведомление", "message": message}),
                vapid_private_key=VAPID_PRIVATE_KEY,
                vapid_claims=VAPID_CLAIMS
            )
            log = PushLog(client_code=client_code, channel="web", status="sent", provider_response={"mock": True})
            db.add(log)
        except WebPushException as ex:
            log = PushLog(client_code=client_code, channel="web", status="failed", provider_response={"error": str(ex)})
            db.add(log)
    db.commit()
    db.close()