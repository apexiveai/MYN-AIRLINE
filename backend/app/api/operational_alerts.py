from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy import select

from sqlalchemy.orm import Session

from app.db.database import get_db

from app.models.operational_alert import OperationalAlert

from app.schemas.operational_alert import (

    AlertResponse,

    AlertUpdate,

)

router = APIRouter(

    prefix="/api/alerts",

    tags=["Operational Alerts"],

)

def alert_to_response(

    alert: OperationalAlert,

) -> dict:

    return {

        "id": alert.id,

        "flight_id": alert.flight_id,

        "flight_number": (

            alert.flight.flight_number

            if alert.flight

            else None

        ),

        "alert_type": alert.alert_type,

        "severity": alert.severity,

        "title": alert.title,

        "message": alert.message,

        "status": alert.status,

        "created_at": alert.created_at,

        "acknowledged_at": alert.acknowledged_at,

    }

@router.get(

    "",

    response_model=list[AlertResponse],

)

def list_alerts(

    status: str | None = None,

    db: Session = Depends(get_db),

):

    query = select(OperationalAlert)

    if status is not None:

        query = query.where(

            OperationalAlert.status == status

        )

    alerts = db.scalars(

        query.order_by(

            OperationalAlert.created_at.desc()

        )

    ).all()

    return [

        alert_to_response(alert)

        for alert in alerts

    ]

@router.patch(

    "/{alert_id}",

    response_model=AlertResponse,

)

def update_alert(

    alert_id: int,

    payload: AlertUpdate,

    db: Session = Depends(get_db),

):

    alert = db.get(

        OperationalAlert,

        alert_id,

    )

    if not alert:

        raise HTTPException(

            status_code=404,

            detail="Alert not found",

        )

    if payload.status is not None:

        alert.status = payload.status

        if payload.status == "ACKNOWLEDGED":

            alert.acknowledged_at = datetime.utcnow()

    db.commit()

    db.refresh(alert)

    return alert_to_response(alert)