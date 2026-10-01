import secrets

from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy import select

from sqlalchemy.orm import Session

from app.db.database import get_db

from app.models.passenger import Passenger

from app.schemas.passenger import (

    PassengerCreate,

    PassengerResponse,

    PassengerUpdate,

)

router = APIRouter(

    prefix="/api/passengers",

    tags=["Passengers"],

)

def generate_passenger_code() -> str:

    return "PAX-" + secrets.token_hex(4).upper()

@router.get(

    "",

    response_model=list[PassengerResponse],

)

def list_passengers(

    db: Session = Depends(get_db),

):

    return db.scalars(

        select(Passenger)

        .order_by(Passenger.id)

    ).all()

@router.get(

    "/{passenger_id}",

    response_model=PassengerResponse,

)

def get_passenger(

    passenger_id: int,

    db: Session = Depends(get_db),

):

    passenger = db.get(

        Passenger,

        passenger_id,

    )

    if not passenger:

        raise HTTPException(

            status_code=404,

            detail="Passenger not found",

        )

    return passenger

@router.post(

    "",

    response_model=PassengerResponse,

    status_code=201,

)

def create_passenger(

    payload: PassengerCreate,

    db: Session = Depends(get_db),

):

    existing = None

    if payload.passport_number:

        existing = db.scalar(

            select(Passenger).where(

                Passenger.passport_number

                == payload.passport_number

            )

        )

    if existing:

        raise HTTPException(

            status_code=409,

            detail="Passport number already exists",

        )

    passenger = Passenger(

        passenger_code=(

            payload.passenger_code

            or generate_passenger_code()

        ),

        first_name=payload.first_name,

        last_name=payload.last_name,

        gender=payload.gender,

        date_of_birth=payload.date_of_birth,

        nationality=payload.nationality,

        passport_number=payload.passport_number,

        phone=payload.phone,

        email=payload.email,

    )

    db.add(passenger)

    db.commit()

    db.refresh(passenger)

    return passenger

@router.patch(

    "/{passenger_id}",

    response_model=PassengerResponse,

)

def update_passenger(

    passenger_id: int,

    payload: PassengerUpdate,

    db: Session = Depends(get_db),

):

    passenger = db.get(

        Passenger,

        passenger_id,

    )

    if not passenger:

        raise HTTPException(

            status_code=404,

            detail="Passenger not found",

        )

    data = payload.model_dump(

        exclude_unset=True

    )

    for field, value in data.items():

        setattr(

            passenger,

            field,

            value,

        )

    db.commit()

    db.refresh(passenger)

    return passenger