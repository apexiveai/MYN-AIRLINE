from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy import select

from sqlalchemy.orm import Session

from app.db.database import get_db

from app.models.booking import Booking

from app.models.checkin import CheckIn

from app.schemas.checkin import (

    CheckInCreate,

    CheckInResponse,

)

router = APIRouter(

    prefix="/api/check-in",

    tags=["Check-in"],

)

@router.post(

    "",

    response_model=CheckInResponse,

    status_code=201,

)

def check_in_passenger(

    payload: CheckInCreate,

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

    if booking.status != "CONFIRMED":

        raise HTTPException(

            status_code=409,

            detail="Booking is not eligible for check-in",

        )

    existing = db.scalar(

        select(CheckIn).where(

            CheckIn.booking_id

            == payload.booking_id

        )

    )

    if existing:

        raise HTTPException(

            status_code=409,

            detail="Passenger already checked in",

        )

    checkin = CheckIn(

        booking_id=booking.id,

        status="CHECKED_IN",

        checkin_method=payload.checkin_method,

    )

    db.add(checkin)

    booking.status = "CHECKED_IN"

    db.commit()

    db.refresh(checkin)

    return checkin