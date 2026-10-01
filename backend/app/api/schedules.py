from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy import select
from datetime import date
from sqlalchemy.orm import Session, joinedload

from app.db.database import get_db

from app.models.flight import Flight

from app.models.flight_schedule import FlightSchedule

from app.schemas.flight_schedule import (

    FlightScheduleCreate,

    FlightScheduleResponse,

    FlightScheduleUpdate,

)

router = APIRouter(

    prefix="/api/schedules",

    tags=["Schedules"],

)

def schedule_response(

    schedule: FlightSchedule,

):

    flight = schedule.flight

    return {

        "id": schedule.id,

        "flight_id": schedule.flight_id,

        "flight_number": flight.flight_number,

        "origin": (

            flight.origin.iata_code

            if flight.origin

            else ""

        ),

        "destination": (

            flight.destination.iata_code

            if flight.destination

            else ""

        ),

        "operating_date": schedule.operating_date,

        "scheduled_departure": (

            schedule.scheduled_departure

        ),

        "scheduled_arrival": (

            schedule.scheduled_arrival

        ),

        "actual_departure": (

            schedule.actual_departure

        ),

        "actual_arrival": (

            schedule.actual_arrival

        ),

        "status": schedule.status,

        "delay_minutes": schedule.delay_minutes,

    }

@router.get(

    "",

    response_model=list[FlightScheduleResponse],

)

def list_schedules(

    db: Session = Depends(get_db),

):

    schedules = db.scalars(

        select(FlightSchedule)

        .options(

            joinedload(

                FlightSchedule.flight

            ).joinedload(

                Flight.origin

            ),

            joinedload(

                FlightSchedule.flight

            ).joinedload(

                Flight.destination

            ),

        )

        .order_by(

            FlightSchedule.operating_date,

            FlightSchedule.scheduled_departure,

        )

    ).all()

    return [

        schedule_response(schedule)

        for schedule in schedules

    ]

@router.get(

    "/{schedule_id}",

    response_model=FlightScheduleResponse,

)

def get_schedule(

    schedule_id: int,

    db: Session = Depends(get_db),

):

    schedule = db.scalar(

        select(FlightSchedule)

        .options(

            joinedload(

                FlightSchedule.flight

            ).joinedload(

                Flight.origin

            ),

            joinedload(

                FlightSchedule.flight

            ).joinedload(

                Flight.destination

            ),

        )

        .where(

            FlightSchedule.id == schedule_id

        )

    )

    if not schedule:

        raise HTTPException(

            status_code=404,

            detail="Schedule not found",

        )

    return schedule_response(schedule)

@router.post(

    "",

    response_model=FlightScheduleResponse,

    status_code=201,

)

def create_schedule(

    payload: FlightScheduleCreate,

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

    existing = db.scalar(

        select(FlightSchedule).where(

            FlightSchedule.flight_id

            == payload.flight_id,

            FlightSchedule.operating_date

            == payload.operating_date,

        )

    )

    if existing:

        raise HTTPException(

            status_code=409,

            detail="Schedule already exists for this flight and date",

        )

    schedule = FlightSchedule(

        flight_id=payload.flight_id,

        operating_date=payload.operating_date,

        scheduled_departure=(

            payload.scheduled_departure

        ),

        scheduled_arrival=(

            payload.scheduled_arrival

        ),

        status="SCHEDULED",

        delay_minutes=0,
)

    db.add(schedule)

    db.commit()

    db.refresh(schedule)

    schedule = db.scalar(

        select(FlightSchedule)

        .options(

            joinedload(

                FlightSchedule.flight

            ).joinedload(

                Flight.origin

            ),

            joinedload(

                FlightSchedule.flight

            ).joinedload(

                Flight.destination

            ),

        )

        .where(

            FlightSchedule.id == schedule.id

        )

    )

    return schedule_response(schedule)

@router.patch(

    "/{schedule_id}",

    response_model=FlightScheduleResponse,

)

def update_schedule(

    schedule_id: int,

    payload: FlightScheduleUpdate,

    db: Session = Depends(get_db),

):

    schedule = db.get(

        FlightSchedule,

        schedule_id,

    )

    if not schedule:

        raise HTTPException(

            status_code=404,

            detail="Schedule not found",

        )

    values = payload.model_dump(

        exclude_unset=True

    )

    for field, value in values.items():

        setattr(

            schedule,

            field,

            value,

        )

    db.commit()

    db.refresh(schedule)

    schedule = db.scalar(

        select(FlightSchedule)

        .options(

            joinedload(

                FlightSchedule.flight

            ).joinedload(

                Flight.origin

            ),

            joinedload(

                FlightSchedule.flight

            ).joinedload(

                Flight.destination

            ),

        )

        .where(

            FlightSchedule.id == schedule_id

        )

    )

    return schedule_response(schedule)

@router.delete("/{schedule_id}")

def delete_schedule(

    schedule_id: int,

    db: Session = Depends(get_db),

):

    schedule = db.get(

        FlightSchedule,

        schedule_id,

    )

    if not schedule:

        raise HTTPException(

            status_code=404,

            detail="Schedule not found",

        )

    db.delete(schedule)

    db.commit()

    return {

        "message": "Schedule deleted",

        "schedule_id": schedule_id,

    }

@router.get(

    "/today",

    response_model=list[FlightScheduleResponse],

)

def today_schedules(

    db: Session = Depends(get_db),

):

    today = date.today()

    schedules = db.scalars(

        select(FlightSchedule)

        .options(

            joinedload(

                FlightSchedule.flight

            ).joinedload(

                Flight.origin

            ),

            joinedload(

                FlightSchedule.flight

            ).joinedload(

                Flight.destination

            ),

        )

        .where(

            FlightSchedule.operating_date == today

        )

        .order_by(

            FlightSchedule.scheduled_departure

        )

    ).all()

    return [

        schedule_response(schedule)

        for schedule in schedules

    ]