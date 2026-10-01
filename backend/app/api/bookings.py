import secrets

import string

from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy import select

from sqlalchemy.orm import Session, joinedload

from app.db.database import get_db

from app.models.booking import Booking

from app.models.flight import Flight

from app.models.passenger import Passenger

from app.models.seat import SeatAssignment

from app.schemas.booking import (

    BookingCreate,

    BookingResponse,

    BookingUpdate,

)

router = APIRouter(

    prefix="/api/bookings",

    tags=["Bookings"],

)

def generate_pnr(db: Session) -> str:

    alphabet = string.ascii_uppercase + string.digits

    while True:

        pnr = "".join(

            secrets.choice(alphabet)

            for _ in range(6)

        )

        existing = db.scalar(

            select(Booking).where(

                Booking.pnr == pnr

            )

        )

        if not existing:

            return pnr

def booking_response(

    booking: Booking,

):

    seat_number = None

    if booking.seat:

        seat_number = (

            booking.seat.seat_number

        )

    return {

        "id": booking.id,

        "pnr": booking.pnr,

        "flight_id": booking.flight_id,

        "flight_number": (

            booking.flight.flight_number

        ),

        "passenger_id": booking.passenger_id,

        "passenger_name": (

            f"{booking.passenger.first_name} "

            f"{booking.passenger.last_name}"

        ),

        "booking_class": booking.booking_class,

        "fare_type": booking.fare_type,

        "status": booking.status,

        "ticket_number": booking.ticket_number,

        "seat_number": seat_number,

    }

def load_booking(

    db: Session,

    booking_id: int,

):

    return db.scalar(

        select(Booking)

        .options(

            joinedload(

                Booking.flight

            ),

            joinedload(

                Booking.passenger

            ),

            joinedload(

                Booking.seat

            ),

        )

        .where(

            Booking.id == booking_id

        )

    )

@router.get(

    "",

    response_model=list[BookingResponse],

)

def list_bookings(

    db: Session = Depends(get_db),

):

    bookings = db.scalars(

        select(Booking)

        .options(

            joinedload(

                Booking.flight

            ),

            joinedload(

                Booking.passenger

            ),

            joinedload(

                Booking.seat

            ),

        )

        .order_by(Booking.id.desc())

    ).all()

    return [

        booking_response(booking)

        for booking in bookings

    ]

@router.get(

    "/{booking_id}",

    response_model=BookingResponse,

)

def get_booking(

    booking_id: int,

    db: Session = Depends(get_db),

):

    booking = load_booking(

        db,

        booking_id,

    )

    if not booking:

        raise HTTPException(

            status_code=404,

            detail="Booking not found",

        )

    return booking_response(booking)

@router.get(

    "/pnr/{pnr}",

    response_model=BookingResponse,

)

def get_booking_by_pnr(

    pnr: str,

    db: Session = Depends(get_db),

):

    booking = db.scalar(

        select(Booking)

        .options(

            joinedload(

                Booking.flight

            ),

            joinedload(

                Booking.passenger

            ),

            joinedload(

                Booking.seat

            ),

        )

        .where(

            Booking.pnr == pnr.upper()

        )

    )

    if not booking:

        raise HTTPException(

            status_code=404,

            detail="PNR not found",

        )

    return booking_response(booking)

@router.post(

    "",

    response_model=BookingResponse,

    status_code=201,

)

def create_booking(

    payload: BookingCreate,

    db: Session = Depends(get_db),

):

    flight = db.get(

        Flight,

        payload.flight_id,

    )

    if not flight:
    
        raise HTTPException(

            status_code=404,

            detail="Flight not found",

        )

    passenger = db.get(

        Passenger,

        payload.passenger_id,

    )

    if not passenger:

        raise HTTPException(

            status_code=404,

            detail="Passenger not found",

        )

    booking = Booking(

        pnr=generate_pnr(db),

        flight_id=flight.id,

        passenger_id=passenger.id,

        booking_class=payload.booking_class,

        fare_type=payload.fare_type,

        status="CONFIRMED",

    )

    db.add(booking)

    db.commit()

    db.refresh(booking)

    booking = load_booking(

        db,

        booking.id,

    )

    return booking_response(booking)

@router.patch(

    "/{booking_id}",

    response_model=BookingResponse,

)

def update_booking(

    booking_id: int,

    payload: BookingUpdate,

    db: Session = Depends(get_db),

):

    booking = db.get(

        Booking,

        booking_id,

    )

    if not booking:

        raise HTTPException(

            status_code=404,

            detail="Booking not found",

        )

    data = payload.model_dump(

        exclude_unset=True

    )

    for field, value in data.items():

        setattr(

            booking,

            field,

            value,

        )

    db.commit()

    booking = load_booking(

        db,

        booking_id,

    )

    return booking_response(booking)