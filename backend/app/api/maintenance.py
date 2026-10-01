from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy import select

from sqlalchemy.orm import Session

from app.db.database import get_db

from app.models.aircraft import Aircraft

from app.models.maintenance import MaintenanceRecord

from app.schemas.maintenance import (

    MaintenanceCreate,

    MaintenanceResponse,

    MaintenanceUpdate,

)

router = APIRouter(

    prefix="/api/maintenance",

    tags=["Fleet Maintenance"],

)

def maintenance_to_response(

    record: MaintenanceRecord,

) -> dict:

    return {

        "id": record.id,

        "aircraft_id": record.aircraft_id,

        "registration": record.aircraft.registration,

        "aircraft_model": record.aircraft.model,

        "maintenance_type": record.maintenance_type,

        "status": record.status,

        "description": record.description,

        "scheduled_start": record.scheduled_start,

        "scheduled_end": record.scheduled_end,

        "actual_start": record.actual_start,

        "actual_end": record.actual_end,

        "technician": record.technician,

        "created_at": record.created_at,

    }

@router.get(

    "",

    response_model=list[MaintenanceResponse],

)

def list_maintenance(

    aircraft_id: int | None = None,

    status: str | None = None,

    db: Session = Depends(get_db),

):

    query = select(MaintenanceRecord)

    if aircraft_id is not None:

        query = query.where(

            MaintenanceRecord.aircraft_id == aircraft_id

        )

    if status is not None:

        query = query.where(

            MaintenanceRecord.status == status

        )

    records = db.scalars(

        query.order_by(MaintenanceRecord.id.desc())

    ).all()

    return [

        maintenance_to_response(record)

        for record in records

    ]

@router.get(

    "/{maintenance_id}",

    response_model=MaintenanceResponse,

)

def get_maintenance(

    maintenance_id: int,

    db: Session = Depends(get_db),

):

    record = db.get(

        MaintenanceRecord,

        maintenance_id,

    )

    if not record:

        raise HTTPException(

            status_code=404,

            detail="Maintenance record not found",

        )

    return maintenance_to_response(record)

@router.post(

    "",

    response_model=MaintenanceResponse,

    status_code=201,

)

def create_maintenance(

    payload: MaintenanceCreate,

    db: Session = Depends(get_db),

):

    aircraft = db.get(

        Aircraft,

        payload.aircraft_id,

    )

    if not aircraft:

        raise HTTPException(

            status_code=404,

            detail="Aircraft not found",

        )

    record = MaintenanceRecord(

        aircraft_id=payload.aircraft_id,

        maintenance_type=payload.maintenance_type,

        status="SCHEDULED",

        description=payload.description,

        scheduled_start=payload.scheduled_start,

        scheduled_end=payload.scheduled_end,

        technician=payload.technician,

    )

    db.add(record)

    aircraft.status = "MAINTENANCE"

    db.commit()

    db.refresh(record)

    return maintenance_to_response(record)

@router.patch(

    "/{maintenance_id}",

    response_model=MaintenanceResponse,

)

def update_maintenance(

    maintenance_id: int,

    payload: MaintenanceUpdate,

    db: Session = Depends(get_db),

):

    record = db.get(

        MaintenanceRecord,

        maintenance_id,

    )

    if not record:

        raise HTTPException(

            status_code=404,

            detail="Maintenance record not found",

        )

    updates = payload.model_dump(

        exclude_unset=True

    )

    for field, value in updates.items():

        setattr(record, field, value)

    aircraft = record.aircraft

    if record.status == "IN_PROGRESS":

        aircraft.status = "MAINTENANCE"

        if record.actual_start is None:

            record.actual_start = datetime.utcnow()

    elif record.status == "COMPLETED":

        aircraft.status = "AVAILABLE"

        if record.actual_end is None:
        
            record.actual_end = datetime.utcnow()

        aircraft.last_maintenance_at = (

            record.actual_end

        )

    elif record.status == "CANCELLED":

        aircraft.status = "AVAILABLE"

    db.commit()

    db.refresh(record)

    return maintenance_to_response(record)

@router.delete("/{maintenance_id}")

def delete_maintenance(

    maintenance_id: int,

    db: Session = Depends(get_db),

):

    record = db.get(

        MaintenanceRecord,

        maintenance_id,

    )

    if not record:

        raise HTTPException(

            status_code=404,

            detail="Maintenance record not found",

        )

    db.delete(record)

    db.commit()

    return {

        "message": "Maintenance record deleted",

        "id": maintenance_id,

    }