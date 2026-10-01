import secrets

from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy import select

from sqlalchemy.orm import Session

from app.db.database import get_db

from app.models.boarding_pass import BoardingPass

from app.models.booking import Booking

from app.models.seat import SeatAssignment

from app.schemas.boarding import (

    BoardingPassCreate,

    BoardingPassResponse,

)

router = APIRouter(

    prefix="/api/boarding",

    tags=["Boarding"],

)

def generate_boarding_number(

    db: Session,

) -> str:

    while True:

        number = (

            "MNA-"

            + secrets.token_hex(6).upper()

        )

        existing = db.scalar(

            select(BoardingPass).where(

                BoardingPass.boarding_pass_number

                == number

            )

        )

        if not existing:

            return number

@router.post(

    "/pass",

    response_model=BoardingPassResponse,

    status_code=201,

)

def issue_boarding_pass(

    payload: BoardingPassCreate,

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

    if booking.status != "CHECKED_IN":

        raise HTTPException(

            status_code=409,

            detail="Passenger must check in before boarding pass issuance",

        )

    existing = db.scalar(

        select(BoardingPass).where(

            BoardingPass.booking_id

            == booking.id

        )

    )

    if existing:

        raise HTTPException(

            status_code=409,

            detail="Boarding pass already issued",

        )

    seat = db.scalar(

        select(SeatAssignment).where(

            SeatAssignment.booking_id

            == booking.id

        )

    )

    if not seat:

        raise HTTPException(

            status_code=409,

            detail="Seat must be assigned before boarding pass issuance",

        )

    boarding_pass = BoardingPass(

        booking_id=booking.id,

        boarding_pass_number=(

            generate_boarding_number(db)

        ),

        gate=payload.gate,

        boarding_group=payload.boarding_group,

        status="ISSUED",

    )

    db.add(boarding_pass)

    db.commit()

    db.refresh(boarding_pass)

    return boarding_pass

@router.post(

    "/{boarding_pass_id}/board",

    response_model=BoardingPassResponse,

)

def board_passenger(

    boarding_pass_id: int,

    db: Session = Depends(get_db),

):

    boarding_pass = db.get(

        BoardingPass,

        boarding_pass_id,

    )

    if not boarding_pass:

        raise HTTPException(

            status_code=404,

            detail="Boarding pass not found",

        )

    if boarding_pass.status == "BOARDED":

        raise HTTPException(

            status_code=409,

            detail="Passenger already boarded",

        )

    if boarding_pass.status != "ISSUED":

        raise HTTPException(

            status_code=409,

            detail="Boarding pass is not valid for boarding",

        )

    boarding_pass.status = "BOARDED"

    boarding_pass.boarded_at = datetime.utcnow()

    booking = db.get(

        Booking,

        boarding_pass.booking_id,

    )

    if booking:

        booking.status = "BOARDED"

    db.commit()

    db.refresh(boarding_pass)

    return boarding_pass

@router.get(

    "/booking/{booking_id}",

    response_model=BoardingPassResponse,

)

def get_boarding_pass(

    booking_id: int,

    db: Session = Depends(get_db),

):

    boarding_pass = db.scalar(

        select(BoardingPass).where(

            BoardingPass.booking_id

            == booking_id

        )

    )

    if not boarding_pass:

        raise HTTPException(

            status_code=404,

            detail="Boarding pass not found",

        )

    return boarding_pass