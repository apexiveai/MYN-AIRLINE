from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy import select

from sqlalchemy.orm import Session

from app.db.database import get_db

from app.models.fare import Fare

from app.models.flight import Flight

from app.schemas.fare import (

    FareCreate,

    FareResponse,

    FareUpdate,

)

router = APIRouter(

    prefix="/api/fares",

    tags=["Revenue & Fares"],

)

def fare_to_response(fare: Fare) -> dict:

    return {

        "id": fare.id,

        "flight_id": fare.flight_id,

        "flight_number": fare.flight.flight_number,

        "fare_code": fare.fare_code,

        "cabin_class": fare.cabin_class,

        "booking_class": fare.booking_class,

        "base_fare": fare.base_fare,

        "taxes": fare.taxes,

        "total_fare": fare.base_fare + fare.taxes,

        "currency": fare.currency,

        "seats_available": fare.seats_available,

        "status": fare.status,

    }

@router.get("", response_model=list[FareResponse])

def list_fares(

    flight_id: int | None = None,

    db: Session = Depends(get_db),

):

    query = select(Fare)

    if flight_id is not None:

        query = query.where(Fare.flight_id == flight_id)

    fares = db.scalars(query.order_by(Fare.id.desc())).all()

    return [fare_to_response(fare) for fare in fares]

@router.get("/{fare_id}", response_model=FareResponse)

def get_fare(

    fare_id: int,

    db: Session = Depends(get_db),

):

    fare = db.get(Fare, fare_id)

    if not fare:

        raise HTTPException(

            status_code=404,

            detail="Fare not found",

        )

    return fare_to_response(fare)

@router.post("", response_model=FareResponse, status_code=201)

def create_fare(

    payload: FareCreate,

    db: Session = Depends(get_db),

):

    flight = db.get(Flight, payload.flight_id)

    if not flight:

        raise HTTPException(

            status_code=404,

            detail="Flight not found",

        )

    fare = Fare(

        flight_id=payload.flight_id,

        fare_code=payload.fare_code,

        cabin_class=payload.cabin_class,

        booking_class=payload.booking_class,

        base_fare=payload.base_fare,

        taxes=payload.taxes,

        currency=payload.currency,

        seats_available=payload.seats_available,

    )

    db.add(fare)

    db.commit()

    db.refresh(fare)

    return fare_to_response(fare)

@router.patch("/{fare_id}", response_model=FareResponse)

def update_fare(

    fare_id: int,

    payload: FareUpdate,

    db: Session = Depends(get_db),

):

    fare = db.get(Fare, fare_id)

    if not fare:

        raise HTTPException(

            status_code=404,

            detail="Fare not found",

        )

    updates = payload.model_dump(exclude_unset=True)

    for field, value in updates.items():

        setattr(fare, field, value)

    db.commit()

    db.refresh(fare)

    return fare_to_response(fare)

@router.delete("/{fare_id}")

def delete_fare(

    fare_id: int,

    db: Session = Depends(get_db),

):

    fare = db.get(Fare, fare_id)

    if not fare:

        raise HTTPException(

            status_code=404,

            detail="Fare not found",

        )

    db.delete(fare)

    db.commit()

    return {

        "message": "Fare deleted",

        "id": fare_id,

    }