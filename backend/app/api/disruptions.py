from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy import select

from sqlalchemy.orm import Session

from app.db.database import get_db

from app.models.disruption import Disruption

from app.models.flight import Flight

from app.models.operational_alert import OperationalAlert

from app.schemas.disruption import (

    DisruptionCreate,

    DisruptionResponse,

    DisruptionUpdate,

)

router = APIRouter(

    prefix="/api/disruptions",

    tags=["Disruption Management"],

)

def disruption_to_response(

    disruption: Disruption,

) -> dict:

    return {

        "id": disruption.id,

        "flight_id": disruption.flight_id,

        "flight_number": disruption.flight.flight_number,

        "disruption_type": disruption.disruption_type,

        "severity": disruption.severity,

        "status": disruption.status,

        "reason": disruption.reason,

        "description": disruption.description,

        "resolution": disruption.resolution,

        "created_at": disruption.created_at,

        "resolved_at": disruption.resolved_at,

    }

@router.get(

    "",

    response_model=list[DisruptionResponse],

)

def list_disruptions(

    status: str | None = None,

    db: Session = Depends(get_db),

):

    query = select(Disruption)

    if status is not None:

        query = query.where(

            Disruption.status == status

        )

    records = db.scalars(

        query.order_by(

            Disruption.created_at.desc()

        )

    ).all()

    return [

        disruption_to_response(record)

        for record in records

    ]

@router.get(

    "/{disruption_id}",

    response_model=DisruptionResponse,

)

def get_disruption(

    disruption_id: int,

    db: Session = Depends(get_db),

):

    disruption = db.get(

        Disruption,

        disruption_id,

    )

    if not disruption:

        raise HTTPException(

            status_code=404,

            detail="Disruption not found",

        )

    return disruption_to_response(disruption)

@router.post(

    "",

    response_model=DisruptionResponse,

    status_code=201,

)

def create_disruption(

    payload: DisruptionCreate,

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

    disruption = Disruption(

        flight_id=payload.flight_id,

        disruption_type=payload.disruption_type,

        severity=payload.severity,

        status="OPEN",

        reason=payload.reason,

        description=payload.description,

    )

    db.add(disruption)

    flight.status = (

        "CANCELLED"

        if payload.disruption_type == "CANCELLATION"

        else "DISRUPTED"

    )

    alert = OperationalAlert(

        flight_id=flight.id,

        alert_type="DISRUPTION",

        severity=payload.severity,

        title=f"{flight.flight_number} operational disruption",

        message=payload.reason,

    )

    db.add(alert)

    db.commit()

    db.refresh(disruption)

    return disruption_to_response(disruption)

@router.patch(

    "/{disruption_id}",

    response_model=DisruptionResponse,

)

def update_disruption(

    disruption_id: int,

    payload: DisruptionUpdate,

    db: Session = Depends(get_db),

):

    disruption = db.get(

        Disruption,

        disruption_id,

    )

    if not disruption:

        raise HTTPException(

            status_code=404,

            detail="Disruption not found",

        )

    updates = payload.model_dump(

        exclude_unset=True

    )

    for field, value in updates.items():

        setattr(disruption, field, value)

    if disruption.status == "RESOLVED":

        disruption.resolved_at = datetime.utcnow()

        if disruption.flight.status == "DISRUPTED":

            disruption.flight.status = "SCHEDULED"

    db.commit()

    db.refresh(disruption)

    return disruption_to_response(disruption)