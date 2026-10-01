import secrets

from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session

from app.db.database import get_db

from app.models.booking import Booking

from app.models.ticket import Ticket

from app.models.payment import Payment

from app.schemas.ticket import (

    TicketIssueCreate,

    TicketResponse,

)

router = APIRouter(

    prefix="/api/tickets",

    tags=["Ticketing"],

)

def generate_ticket_number() -> str:

    return (

        "176-"

        + secrets.token_hex(5).upper()

    )

@router.get(

    "/booking/{booking_id}",

    response_model=TicketResponse,

)

def get_booking_ticket(

    booking_id: int,

    db: Session = Depends(get_db),

):

    ticket = (

        db.query(Ticket)

        .filter(Ticket.booking_id == booking_id)

        .first()

    )

    if not ticket:

        raise HTTPException(

            status_code=404,

            detail="Ticket not found",

        )

    return ticket

@router.post(

    "/issue",

    response_model=TicketResponse,

    status_code=201,

)

def issue_ticket(

    payload: TicketIssueCreate,

    db: Session = Depends(get_db),

):

    booking = db.get(Booking, payload.booking_id)

    if not booking:

        raise HTTPException(

            status_code=404,

            detail="Booking not found",

        )

    existing_ticket = (

        db.query(Ticket)

        .filter(Ticket.booking_id == booking.id)

        .first()

    )

    if existing_ticket:

        raise HTTPException(

            status_code=409,

            detail="Ticket already issued",

        )

    successful_payment = (

        db.query(Payment)

        .filter(

            Payment.booking_id == booking.id,

            Payment.status == "PAID",

        )

        .first()

    )

    if not successful_payment:

        raise HTTPException(

            status_code=400,

            detail="Booking must have a successful payment before ticket issuance",

        )

    ticket = Ticket(

        booking_id=booking.id,

        ticket_number=generate_ticket_number(),

        issue_status="ISSUED",

        issued_at=datetime.utcnow(),

    )

    db.add(ticket)

    booking.ticket_number = ticket.ticket_number

    booking.status = "TICKETED"

    db.commit()

    db.refresh(ticket)

    return ticket

@router.post(

    "/{ticket_id}/void",

    response_model=TicketResponse,

)

def void_ticket(

    ticket_id: int,

    db: Session = Depends(get_db),

):

    ticket = db.get(Ticket, ticket_id)

    if not ticket:

        raise HTTPException(

            status_code=404,

            detail="Ticket not found",

        )

    if ticket.issue_status == "VOID":

        raise HTTPException(

            status_code=400,

            detail="Ticket already voided",

        )

    ticket.issue_status = "VOID"

    ticket.voided_at = datetime.utcnow()

    ticket.booking.status = "TICKET_VOID"

    db.commit()

    db.refresh(ticket)

    return ticket