from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy import select

from sqlalchemy.orm import Session

from app.db.database import get_db

from app.models.crew import Crew

from app.models.flight import Flight

from app.models.flight_crew import FlightCrew

from app.schemas.crew import (

    CrewCreate,

    CrewResponse,

    CrewUpdate,

    FlightCrewCreate,

    FlightCrewResponse,

)

router = APIRouter(

    prefix="/api/crew",

    tags=["Crew"],

)

@router.get(

    "",

    response_model=list[CrewResponse],

)

def list_crew(

    db: Session = Depends(get_db),

):

    return db.scalars(

        select(Crew).order_by(Crew.id)

    ).all()

@router.get(

    "/{crew_id}",

    response_model=CrewResponse,

)

def get_crew(

    crew_id: int,

    db: Session = Depends(get_db),

):

    crew = db.get(Crew, crew_id)

    if not crew:

        raise HTTPException(

            status_code=404,

            detail="Crew member not found",

        )

    return crew

@router.post(

    "",

    response_model=CrewResponse,

    status_code=201,

)

def create_crew(

    payload: CrewCreate,

    db: Session = Depends(get_db),

):

    existing = db.scalar(

        select(Crew).where(

            Crew.employee_code

            == payload.employee_code

        )

    )

    if existing:

        raise HTTPException(

            status_code=409,

            detail="Employee code already exists",

        )

    crew = Crew(

        employee_code=payload.employee_code,

        full_name=payload.full_name,

        role=payload.role,

        license_number=payload.license_number,

        base_airport=payload.base_airport.upper(),

        status=payload.status,

        phone=payload.phone,

        email=payload.email,

    )

    db.add(crew)

    db.commit()

    db.refresh(crew)

    return crew

@router.patch(

    "/{crew_id}",

    response_model=CrewResponse,

)

def update_crew(

    crew_id: int,

    payload: CrewUpdate,

    db: Session = Depends(get_db),

):

    crew = db.get(Crew, crew_id)

    if not crew:

        raise HTTPException(

            status_code=404,

            detail="Crew member not found",

        )

    data = payload.model_dump(

        exclude_unset=True

    )

    if "base_airport" in data:

        data["base_airport"] = (

            data["base_airport"].upper()

        )

    for field, value in data.items():

        setattr(crew, field, value)

    db.commit()

    db.refresh(crew)

    return crew

@router.delete("/{crew_id}")

def delete_crew(

    crew_id: int,

    db: Session = Depends(get_db),

):

    crew = db.get(Crew, crew_id)

    if not crew:

        raise HTTPException(

            status_code=404,

            detail="Crew member not found",

        )

    db.delete(crew)

    db.commit()

    return {

        "message": "Crew member deleted",

        "crew_id": crew_id,

    }

@router.get(

    "/flight/{flight_id}",

    response_model=list[FlightCrewResponse],

)

def get_flight_crew(

    flight_id: int,

    db: Session = Depends(get_db),

):

    flight = db.get(Flight, flight_id)

    if not flight:

        raise HTTPException(

            status_code=404,

            detail="Flight not found",

        )

    assignments = db.scalars(

        select(FlightCrew)

        .where(

            FlightCrew.flight_id == flight_id

        )

        .order_by(FlightCrew.id)

    ).all()

    return [

        {

            "id": assignment.id,

            "flight_id": assignment.flight_id,

            "crew_id": assignment.crew_id,

            "duty_role": assignment.duty_role,

            "crew_name": assignment.crew.full_name,

            "employee_code": assignment.crew.employee_code,

        }

        for assignment in assignments

    ]

@router.post(

    "/flight/{flight_id}",

    response_model=FlightCrewResponse,

    status_code=201,

)

def assign_crew(

    flight_id: int,

    payload: FlightCrewCreate,

    db: Session = Depends(get_db),

):

    flight = db.get(Flight, flight_id)

    if not flight:

        raise HTTPException(

            status_code=404,

            detail="Flight not found",

        )

    crew = db.get(Crew, payload.crew_id)

    if not crew:

        raise HTTPException(

            status_code=404,

            detail="Crew member not found",

        )

    existing = db.scalar(

        select(FlightCrew).where(

            FlightCrew.flight_id == flight_id,

            FlightCrew.crew_id == payload.crew_id,

        )

    )

    if existing:

        raise HTTPException(

            status_code=409,

            detail="Crew member already assigned",

        )

    assignment = FlightCrew(

        flight_id=flight_id,

        crew_id=payload.crew_id,

        duty_role=payload.duty_role,

    )

    db.add(assignment)

    crew.status = "ASSIGNED"

    db.commit()

    db.refresh(assignment)

    return {

        "id": assignment.id,

        "flight_id": assignment.flight_id,

        "crew_id": assignment.crew_id,

        "duty_role": assignment.duty_role,

        "crew_name": crew.full_name,

        "employee_code": crew.employee_code,

    }

@router.delete(

    "/flight/{flight_id}/{assignment_id}"

)

def remove_crew_assignment(

    flight_id: int,

    assignment_id: int,

    db: Session = Depends(get_db),

):

    assignment = db.scalar(

        select(FlightCrew).where(

            FlightCrew.id == assignment_id,

            FlightCrew.flight_id == flight_id,

        )

    )

    if not assignment:

        raise HTTPException(

            status_code=404,

            detail="Crew assignment not found",

        )

    crew = db.get(

        Crew,

        assignment.crew_id,

    )

    if crew:

        crew.status = "AVAILABLE"

    db.delete(assignment)

    db.commit()

    return {

        "message": "Crew assignment removed",

        "assignment_id": assignment_id,

    }