from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy import select

from sqlalchemy.orm import Session

from app.db.database import get_db

from app.models.aircraft import Aircraft

from app.schemas.aircraft import (

    AircraftCreate,

    AircraftResponse,

    AircraftUpdate,

)

router = APIRouter(

    prefix="/api/fleet",

    tags=["Fleet"],

)

@router.get(

    "",

    response_model=list[AircraftResponse],

)

def list_aircraft(

    status: str | None = None,

    db: Session = Depends(get_db),

):

    query = select(Aircraft)

    if status:

        query = query.where(

            Aircraft.status == status

        )

    return db.scalars(

        query.order_by(Aircraft.id)

    ).all()

@router.get(

    "/{aircraft_id}",

    response_model=AircraftResponse,

)

def get_aircraft(

    aircraft_id: int,

    db: Session = Depends(get_db),

):

    aircraft = db.get(

        Aircraft,

        aircraft_id,

    )

    if not aircraft:

        raise HTTPException(

            status_code=404,

            detail="Aircraft not found",

        )

    return aircraft

@router.post(

    "",

    response_model=AircraftResponse,

    status_code=201,

)

def create_aircraft(

    payload: AircraftCreate,

    db: Session = Depends(get_db),

):

    existing = db.scalar(

        select(Aircraft).where(

            Aircraft.registration

            == payload.registration

        )

    )

    if existing:

        raise HTTPException(

            status_code=409,

            detail="Aircraft registration already exists",

        )

    aircraft = Aircraft(

        registration=payload.registration,

        model=payload.model,

        manufacturer=payload.manufacturer,

        seat_capacity=payload.seat_capacity,

        status=payload.status,

    )

    db.add(aircraft)

    db.commit()

    db.refresh(aircraft)

    return aircraft

@router.patch(

    "/{aircraft_id}",

    response_model=AircraftResponse,

)

def update_aircraft(

    aircraft_id: int,

    payload: AircraftUpdate,

    db: Session = Depends(get_db),

):

    aircraft = db.get(

        Aircraft,

        aircraft_id,

    )

    if not aircraft:

        raise HTTPException(

            status_code=404,

            detail="Aircraft not found",

        )

    updates = payload.model_dump(

        exclude_unset=True

    )

    for field, value in updates.items():

        setattr(aircraft, field, value)

    db.commit()

    db.refresh(aircraft)

    return aircraft

@router.delete("/{aircraft_id}")

def delete_aircraft(

    aircraft_id: int,

    db: Session = Depends(get_db),

):

    aircraft = db.get(

        Aircraft,

        aircraft_id,

    )

    if not aircraft:

        raise HTTPException(

            status_code=404,

            detail="Aircraft not found",

        )

    db.delete(aircraft)

    db.commit()

    return {

        "message": "Aircraft deleted",

        "id": aircraft_id,

    }