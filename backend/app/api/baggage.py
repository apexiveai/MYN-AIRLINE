import secrets

from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy import select

from sqlalchemy.orm import Session

from app.db.database import get_db

from app.models.baggage import Baggage

from app.models.booking import Booking

from app.schemas.baggage import (

    BaggageCreate,

    BaggageResponse,

)

router = APIRouter(

    prefix="/api/baggage",

    tags=["Baggage"],

)

@router.get(
    "",
    response_model=list[BaggageResponse],
)
def list_baggage(
    db: Session = Depends(get_db),
):
    return db.scalars(
        select(Baggage).order_by(Baggage.id)
    ).all()

def generate_bag_tag(db: Session) -> str:

    while True:

        tag = (

            "MNA"

            + secrets.token_hex(5).upper()

        )

        existing = db.scalar(

            select(Baggage).where(

                Baggage.bag_tag == tag

            )

        )

        if not existing:

            return tag

@router.get(

    "/booking/{booking_id}",

    response_model=list[BaggageResponse],

)

def booking_baggage(

    booking_id: int,

    db: Session = Depends(get_db),

):

    return db.scalars(

        select(Baggage)

        .where(

            Baggage.booking_id

            == booking_id

        )

        .order_by(Baggage.id)

    ).all()

@router.post(

    "",

    response_model=BaggageResponse,

    status_code=201,

)

def add_baggage(

    payload: BaggageCreate,

    db: Session = Depends(get_db),

):

    booking = db.get(

        Booking,

        payload.booking_id,

    )

    if not booking:

        raise HTTPException(

            status_code=404,

            detail="Booking not found",

        )

    if booking.status not in (

        "CHECKED_IN",

        "CONFIRMED",

    ):

        raise HTTPException(

            status_code=409,

            detail="Passenger is not eligible for baggage drop",

        )

    if payload.weight_kg <= 0:

        raise HTTPException(

            status_code=400,

            detail="Baggage weight must be greater than zero",

        )

    baggage = Baggage(

        booking_id=booking.id,

        bag_tag=generate_bag_tag(db),

        weight_kg=payload.weight_kg,

        bag_type=payload.bag_type,

        status="ACCEPTED",

    )

    db.add(baggage)

    db.commit()

    db.refresh(baggage)

    return baggage