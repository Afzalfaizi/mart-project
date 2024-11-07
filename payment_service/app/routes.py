from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.db import get_session
from app.schemas import PaymentCreate, PaymentResponse
from app.crud import create_payment, update_payment_status

router = APIRouter()

@router.post("/payments/", response_model=PaymentResponse)
async def initiate_payment(payment: PaymentCreate, session: Session = Depends(get_session)):
    return await create_payment(session, payment)

@router.put("/payments/{payment_id}/status")
async def change_payment_status(payment_id: int, status: str, session: Session = Depends(get_session)):
    payment = await update_payment_status(session, payment_id, status)
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    return payment
