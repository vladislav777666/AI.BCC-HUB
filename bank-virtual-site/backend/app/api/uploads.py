from fastapi import APIRouter, UploadFile, File, Depends, Body
from sqlalchemy.orm import Session
from app.db.session import get_db
import pandas as pd
from app.db.models import Client, Transaction, Transfer

router = APIRouter()

@router.post("/profiles")
async def upload_profiles(file: UploadFile = File(None), data: dict = Body(None), db: Session = Depends(get_db)):
    if file:
        df = pd.read_csv(file.file)
    else:
        df = pd.DataFrame([data])
    for _, row in df.iterrows():
        client = Client(**row.to_dict())
        db.add(client)
    db.commit()
    return {"status": "ok", "imported": len(df)}

@router.post("/transactions")
async def upload_transactions(file: UploadFile = File(None), data: dict = Body(None), db: Session = Depends(get_db)):
    if file:
        df = pd.read_csv(file.file)
    else:
        df = pd.DataFrame([data])
    for _, row in df.iterrows():
        tx = Transaction(**row.to_dict())
        db.add(tx)
    db.commit()
    return {"status": "ok", "imported": len(df)}

@router.post("/transfers")
async def upload_transfers(file: UploadFile = File(None), data: dict = Body(None), db: Session = Depends(get_db)):
    if file:
        df = pd.read_csv(file.file)
    else:
        df = pd.DataFrame([data])
    for _, row in df.iterrows():
        tf = Transfer(**row.to_dict())
        db.add(tf)
    db.commit()
    return {"status": "ok", "imported": len(df)}