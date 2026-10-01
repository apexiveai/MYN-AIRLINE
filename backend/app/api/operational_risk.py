from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy import select

from sqlalchemy.orm import Session

from app.db.database import get_db

from app.models.flight import Flight

from app.models.operational_risk import OperationalRisk

from app.schemas.operational_risk import (

    RiskCreate,

    RiskResponse,

    RiskUpdate,

)

router = APIRouter(

    prefix="/api/risks",

    tags=["Operational Risk"],

)

def risk_to_response(

    risk: OperationalRisk,

) -> dict:

    return {

        "id": risk.id,

        "flight_id": risk.flight_id,

        "flight_number": risk.flight.flight_number,

        "risk_type": risk.risk_type,

        "severity": risk.severity,

        "score": risk.score,

        "title": risk.title,

        "description": risk.description,

        "status": risk.status,

        "created_at": risk.created_at,

        "resolved_at": risk.resolved_at,

    }

@router.get(

    "",

    response_model=list[RiskResponse],

)

def list_risks(

    flight_id: int | None = None,

    status: str | None = None,

    db: Session = Depends(get_db),

):

    query = select(OperationalRisk)

    if flight_id is not None:

        query = query.where(

            OperationalRisk.flight_id == flight_id

        )

    if status is not None:

        query = query.where(

            OperationalRisk.status == status

        )

    risks = db.scalars(

        query.order_by(

            OperationalRisk.created_at.desc()

        )

    ).all()

    return [

        risk_to_response(risk)

        for risk in risks

    ]

@router.post(

    "",

    response_model=RiskResponse,

    status_code=201,

)

def create_risk(

    payload: RiskCreate,

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

    risk = OperationalRisk(

        flight_id=payload.flight_id,

        risk_type=payload.risk_type,

        severity=payload.severity,

        score=payload.score,

        title=payload.title,

        description=payload.description,

    )

    db.add(risk)

    db.commit()

    db.refresh(risk)

    return risk_to_response(risk)

@router.patch(

    "/{risk_id}",

    response_model=RiskResponse,

)

def update_risk(

    risk_id: int,

    payload: RiskUpdate,

    db: Session = Depends(get_db),

):

    risk = db.get(

        OperationalRisk,

        risk_id,

    )

    if not risk:

        raise HTTPException(

            status_code=404,

            detail="Operational risk not found",

        )

    updates = payload.model_dump(

        exclude_unset=True

    )

    for field, value in updates.items():

        setattr(risk, field, value)

    if risk.status == "RESOLVED":

        risk.resolved_at = datetime.utcnow()

    db.commit()

    db.refresh(risk)

    return risk_to_response(risk)