from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy import select

from sqlalchemy.orm import Session

from app.db.database import get_db

from app.models.booking import Booking

from app.models.seat import SeatAssignment

from app.schemas.seat import (

    SeatAssignCreate,

    SeatResponse,

)

router = APIRouter(

    prefix="/api/seats",

    tags=["Seats"],

)

@router.get(

    "/flight/{flight_id}",

)

def flight_seats(

    flight_id: int,

    db: Session = Depends(get_db),

):

    seats = db.scalars(

        select(SeatAssignment)

        .where(

            SeatAssignment.flight_id

            == flight_id

        )

        .order_by(

            SeatAssignment.seat_number

        )

    ).all()

    return [

        {

            "id": seat.id,

            "booking_id": seat.booking_id,

            "flight_id": seat.flight_id,

            "seat_number": seat.seat_number,

            "cabin_class": seat.cabin_class,

            "status": seat.status,

        }

        for seat in seats

    ]

@router.post(

    "",

    response_model=SeatResponse,

    status_code=201,

)

def assign_seat(

    payload: SeatAssignCreate,

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

    existing_booking_seat = db.scalar(

        select(SeatAssignment).where(

            SeatAssignment.booking_id

            == payload.booking_id

        )

    )

    if existing_booking_seat:

        raise HTTPException(

            status_code=409,

            detail="Booking already has a seat",

        )

    existing_seat = db.scalar(

        select(SeatAssignment).where(

            SeatAssignment.flight_id

            == booking.flight_id,

            SeatAssignment.seat_number

            == payload.seat_number.upper(),

        )

    )

    if existing_seat:

        raise HTTPException(

            status_code=409,

            detail="Seat already occupied",

        )

    seat = SeatAssignment(

        booking_id=booking.id,

        flight_id=booking.flight_id,

        seat_number=payload.seat_number.upper(),

        cabin_class=payload.cabin_class,

        status="ASSIGNED",

    )

    db.add(seat)

    db.commit()

    db.refresh(seat)

    return seat