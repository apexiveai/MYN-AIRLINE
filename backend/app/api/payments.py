from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy import select

from sqlalchemy.orm import Session

from app.db.database import get_db

from app.models.booking import Booking

from app.models.payment import Payment

from app.schemas.payment import (

    PaymentCreate,

    PaymentResponse,

)

router = APIRouter(

    prefix="/api/payments",

    tags=["Payments"],

)

@router.get("", response_model=list[PaymentResponse])

def list_payments(

    booking_id: int | None = None,

    db: Session = Depends(get_db),

):

    query = select(Payment)

    if booking_id is not None:

        query = query.where(Payment.booking_id == booking_id)

    payments = db.scalars(

        query.order_by(Payment.id.desc())

    ).all()

    return payments

@router.get("/{payment_id}", response_model=PaymentResponse)

def get_payment(

    payment_id: int,

    db: Session = Depends(get_db),

):

    payment = db.get(Payment, payment_id)

    if not payment:

        raise HTTPException(

            status_code=404,

            detail="Payment not found",

        )

    return payment

@router.post(

    "",

    response_model=PaymentResponse,

    status_code=201,

)

def create_payment(

    payload: PaymentCreate,

    db: Session = Depends(get_db),

):

    booking = db.get(Booking, payload.booking_id)

    if not booking:

        raise HTTPException(

            status_code=404,

            detail="Booking not found",

        )

    if payload.amount <= 0:

        raise HTTPException(

            status_code=400,

            detail="Payment amount must be greater than zero",

        )

    payment = Payment(

        booking_id=payload.booking_id,

        amount=payload.amount,

        currency=payload.currency,

        method=payload.method,

        provider=payload.provider,

        transaction_id=payload.transaction_id,

        status="PAID",

        paid_at=datetime.utcnow(),

    )

    db.add(payment)

    booking.status = "PAID"

    db.commit()

    db.refresh(payment)

    return payment