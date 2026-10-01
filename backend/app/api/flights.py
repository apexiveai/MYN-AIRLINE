from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy import select

from sqlalchemy.orm import Session, joinedload

from app.db.database import get_db

from app.models.airport import Airport

from app.models.aircraft import Aircraft

from app.models.flight import Flight

from app.schemas.flight import (

    FlightCreate,

    FlightUpdate,

    FlightResponse,

)

router = APIRouter(

    prefix="/api/flights",

    tags=["Flights"],

)

def flight_to_response(flight: Flight) -> dict:

    return {

        "id": flight.id,

        "flight_number": flight.flight_number,

        "origin": flight.origin.iata_code,

        "destination": flight.destination.iata_code,

        "aircraft": (

            flight.aircraft.model

            if flight.aircraft

            else ""

        ),

        "aircraft_registration": (

            flight.aircraft.registration

            if flight.aircraft

            else None

        ),

        "gate": flight.gate,

        "status": flight.status,

        "departure_time": flight.departure_time,

        "arrival_time": flight.arrival_time,

        "latitude": flight.latitude,

        "longitude": flight.longitude,

        "altitude": flight.altitude,

        "speed": flight.speed,

        "heading": flight.heading,

    }

def get_airport_by_iata(

    db: Session,

    iata_code: str,

) -> Airport:

    airport = db.scalar(

        select(Airport).where(

            Airport.iata_code == iata_code.upper()

        )

    )

    if not airport:

        raise HTTPException(

            status_code=404,

            detail=f"Airport not found: {iata_code}",

        )

    return airport

def get_aircraft_by_registration(

    db: Session,

    registration: str,

) -> Aircraft:

    aircraft = db.scalar(

        select(Aircraft).where(

            Aircraft.registration == registration.upper()

        )

    )

    if not aircraft:

        raise HTTPException(

            status_code=404,

            detail=f"Aircraft not found: {registration}",

        )

    return aircraft

@router.get("", response_model=list[FlightResponse])

def list_flights(

    db: Session = Depends(get_db),

):

    flights = db.scalars(

        select(Flight)

        .options(

            joinedload(Flight.origin),

            joinedload(Flight.destination),

            joinedload(Flight.aircraft),

        )

        .order_by(Flight.id)

    ).all()

    return [

        flight_to_response(flight)

        for flight in flights

    ]

@router.get(

    "/{flight_id}",

    response_model=FlightResponse,

)

def get_flight(

    flight_id: int,

    db: Session = Depends(get_db),

):

    flight = db.scalar(

        select(Flight)

        .options(

            joinedload(Flight.origin),

            joinedload(Flight.destination),

            joinedload(Flight.aircraft),

        )

        .where(Flight.id == flight_id)

    )

    if not flight:

        raise HTTPException(

            status_code=404,

            detail="Flight not found",

        )

    return flight_to_response(flight)

@router.post(

    "",

    response_model=FlightResponse,

    status_code=201,

)

def create_flight(

    payload: FlightCreate,

    db: Session = Depends(get_db),

):

    existing = db.scalar(

        select(Flight).where(

            Flight.flight_number == payload.flight_number

        )

    )

    if existing:

        raise HTTPException(

            status_code=409,

            detail="Flight number already exists",

        )

    origin = get_airport_by_iata(

        db,

        payload.origin,

    )

    destination = get_airport_by_iata(

        db,

        payload.destination,

    )

    aircraft = get_aircraft_by_registration(

        db,

        payload.aircraft,

    )

    flight = Flight(

        flight_number=payload.flight_number,

        origin_id=origin.id,

        destination_id=destination.id,

        aircraft_id=aircraft.id,

        gate=payload.gate,

        status=payload.status,

        departure_time=payload.departure_time,

        arrival_time=payload.arrival_time,

        latitude=payload.latitude,

        longitude=payload.longitude,

        altitude=payload.altitude,

        speed=payload.speed,

        heading=payload.heading,

    )

    db.add(flight)

    db.commit()

    db.refresh(flight)

    flight = db.scalar(

        select(Flight)

        .options(

            joinedload(Flight.origin),

            joinedload(Flight.destination),

            joinedload(Flight.aircraft),

        )

        .where(Flight.id == flight.id)

    )

    return flight_to_response(flight)

@router.patch(

    "/{flight_id}",

    response_model=FlightResponse,

)

def update_flight(

    flight_id: int,

    payload: FlightUpdate,

    db: Session = Depends(get_db),

):

    flight = db.scalar(

        select(Flight)

        .options(

            joinedload(Flight.origin),

            joinedload(Flight.destination),

            joinedload(Flight.aircraft),

        )

        .where(Flight.id == flight_id)

    )

    if not flight:

        raise HTTPException(

            status_code=404,

            detail="Flight not found",

        )

    if payload.origin is not None:

        origin = get_airport_by_iata(

            db,

            payload.origin,

        )

        flight.origin_id = origin.id

    if payload.destination is not None:

        destination = get_airport_by_iata(

            db,

            payload.destination,

        )

        flight.destination_id = destination.id

    if payload.aircraft is not None:

        aircraft = get_aircraft_by_registration(

            db,

            payload.aircraft,

        )

        flight.aircraft_id = aircraft.id

    update_fields = {

        "gate": payload.gate,

        "status": payload.status,

        "departure_time": payload.departure_time,

        "arrival_time": payload.arrival_time,

        "latitude": payload.latitude,

        "longitude": payload.longitude,

        "altitude": payload.altitude,

        "speed": payload.speed,

        "heading": payload.heading,

    }

    for field, value in update_fields.items():

        if value is not None:

            setattr(flight, field, value)

    db.commit()

    flight = db.scalar(

        select(Flight)

        .options(

            joinedload(Flight.origin),

            joinedload(Flight.destination),

            joinedload(Flight.aircraft),

        )

        .where(Flight.id == flight_id)

    )

    return flight_to_response(flight)

@router.delete("/{flight_id}")

def delete_flight(

    flight_id: int,

    db: Session = Depends(get_db),

):

    flight = db.get(Flight, flight_id)

    if not flight:

        raise HTTPException(

            status_code=404,

            detail="Flight not found",

        )

    db.delete(flight)

    db.commit()

    return {

        "message": "Flight deleted",

        "flight_id": flight_id,

    }