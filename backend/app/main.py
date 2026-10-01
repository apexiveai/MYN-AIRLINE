import asyncio

import random

from datetime import datetime, timezone

from fastapi import Depends, FastAPI, WebSocket, WebSocketDisconnect

from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy import func, select
from sqlalchemy.orm import Session
from app.api.fares import router as fares_router
from app.api.weather import router as weather_router
from app.api.operational_risk import router as risk_router
from app.api.disruptions import router as disruptions_router
from app.api.operational_alerts import router as alerts_router
from app.api.payments import router as payments_router
from app.api.aircraft import router as aircraft_router
from app.api.maintenance import router as maintenance_router
from app.api.tickets import router as tickets_router
from sqlalchemy.orm import Session
from app.api.baggage import router as baggage_router
from app.api.boarding import router as boarding_router
from app.api.checkin import router as checkin_router
from app.api.bookings import router as bookings_router
from app.api.passengers import router as passengers_router
from app.api.seats import router as seats_router
from app.api.flights import router as flights_router
from app.api.schedules import router as schedules_router
from app.db.database import SessionLocal, get_db
from app.api.crew import router as crew_router
from app.models.aircraft import Aircraft

from app.models.flight import Flight

app = FastAPI(

    title="MNA Airline Operations Platform",

    version="1.0.0",

)

app.add_middleware(

    CORSMiddleware,

    allow_origins=[

        "http://localhost:5173",

        "http://127.0.0.1:5173",

        "http://localhost:5174",

        "http://127.0.0.1:5174",

        "http://localhost:4173",

        "http://127.0.0.1:4173",

    ],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],

)

app.include_router(flights_router)
app.include_router(fares_router)
app.include_router(payments_router)
app.include_router(tickets_router)
app.include_router(crew_router)
app.include_router(schedules_router)
app.include_router(passengers_router)
app.include_router(bookings_router)
app.include_router(seats_router)
app.include_router(checkin_router)
app.include_router(baggage_router)
app.include_router(boarding_router)
app.include_router(aircraft_router)
app.include_router(maintenance_router)
app.include_router(weather_router)
app.include_router(risk_router)
app.include_router(disruptions_router)
app.include_router(alerts_router)

@app.on_event("startup")

def startup():

    print("[MNA] MNA Airline backend started")

@app.get("/")

def root():

    return {

        "name": "MNA Airline Operations Platform",

        "version": "1.0.0",

        "status": "ONLINE",

    }

@app.get("/health")

def health():

    return {

        "status": "healthy",

        "service": "mna-airline-backend",

    }

def update_flight_positions(

    db: Session,

):

    flights = db.scalars(

        select(Flight).where(

            Flight.status == "AIRBORNE"

        )

    ).all()

    for flight in flights:

        flight.latitude += 0.018

        flight.longitude += 0.032

        flight.altitude += random.randint(

            -150,

            150,

        )

        flight.speed += random.randint(

            -4,

            4,

        )

        flight.altitude = max(

            5000,

            min(39000, flight.altitude),

        )

        flight.speed = max(

            250,

            min(520, flight.speed),

        )

    db.commit()

def serialize_flight(

    flight: Flight,

):

    return {

        "flight": flight.flight_number,

        "origin": (

            flight.origin.iata_code

            if flight.origin

            else None

        ),

        "destination": (

            flight.destination.iata_code

            if flight.destination

            else None

        ),

        "aircraft": (

            flight.aircraft.registration

            if flight.aircraft

            else None

        ),

        "lat": flight.latitude,

        "lng": flight.longitude,

        "altitude": flight.altitude,

        "speed": flight.speed,

        "heading": flight.heading,

        "status": flight.status,

    }

@app.websocket("/ws/flights")

async def flight_stream(

    websocket: WebSocket,

):

    await websocket.accept()

    print(

        "[MNA] Flight WebSocket connected"

    )

    db = SessionLocal()

    try:

        while True:

            update_flight_positions(db)

            flights = db.scalars(

                select(Flight)

            ).all()

            payload = {

                "type": "flight_update",

                "timestamp": datetime.now(

                    timezone.utc

                ).isoformat(),

                "flights": [
                    serialize_flight(flight)

                    for flight in flights

                ],

            }

            await websocket.send_json(

                payload

            )

            await asyncio.sleep(2)

    except WebSocketDisconnect:

        print(

            "[MNA] Flight WebSocket disconnected"

        )

    except Exception as exc:

        print(

            f"[MNA] WebSocket error: {exc}"

        )

    finally:

        db.close()

@app.get("/api/dashboard")

def dashboard(db: Session = Depends(get_db)):

    from app.models.aircraft import Aircraft

    from app.models.crew import Crew

    from app.models.passenger import Passenger

    from app.models.operational_alert import OperationalAlert

    from app.models.operational_risk import OperationalRisk

    from app.models.disruption import Disruption

    from app.models.maintenance import MaintenanceRecord

    from app.models.flight_schedule import FlightSchedule

    from app.models.booking import Booking

    flights = db.scalars(

        select(Flight)

    ).all()

    aircraft = db.scalars(

        select(Aircraft)

    ).all()

    crew = db.scalars(

        select(Crew)

    ).all()

    passengers = db.scalars(

        select(Passenger)

    ).all()

    bookings = db.scalars(

        select(Booking)

    ).all()

    alerts = db.scalars(

        select(OperationalAlert)

        .where(OperationalAlert.status == "OPEN")

        .order_by(OperationalAlert.created_at.desc())

    ).all()

    risks = db.scalars(

        select(OperationalRisk)

        .where(OperationalRisk.status == "OPEN")

        .order_by(OperationalRisk.created_at.desc())

    ).all()

    disruptions = db.scalars(

        select(Disruption)

        .where(Disruption.status == "OPEN")

        .order_by(Disruption.created_at.desc())

    ).all()

    maintenance = db.scalars(

        select(MaintenanceRecord)

        .where(

            MaintenanceRecord.status.in_(

                ["SCHEDULED", "IN_PROGRESS"]

            )

        )

        .order_by(MaintenanceRecord.id.desc())

    ).all()

    schedules = db.scalars(

        select(FlightSchedule)

        .order_by(FlightSchedule.scheduled_departure)

    ).all()

    return {

        "flights": {

            "total": len(flights),

            "airborne": sum(

                1 for f in flights

                if f.status == "AIRBORNE"

            ),

            "scheduled": sum(

                1 for f in flights

                if f.status == "SCHEDULED"

            ),

            "boarding": sum(

                1 for f in flights

                if f.status == "BOARDING"

            ),

            "delayed": sum(

                1 for f in flights

                if f.status == "DELAYED"

            ),

            "disrupted": sum(

                1 for f in flights

                if f.status == "DISRUPTED"

            ),

            "cancelled": sum(

                1 for f in flights

                if f.status == "CANCELLED"

            ),

        },

        "fleet": {

            "total": len(aircraft),

            "available": sum(

                1 for a in aircraft

                if a.status == "AVAILABLE"

            ),

            "in_service": sum(

                1 for a in aircraft

                if a.status == "IN_SERVICE"

            ),

            "maintenance": sum(

                1 for a in aircraft

                if a.status == "MAINTENANCE"

            ),

        },

        "crew": {

            "total": len(crew),

            "available": sum(

                1 for c in crew

                if c.status == "AVAILABLE"

            ),

            "assigned": sum(

                1 for c in crew

                if c.status == "ASSIGNED"

            ),

        },

        "passengers": {

            "total": len(passengers),

        },

        "bookings": {

            "total": len(bookings),

            "confirmed": sum(

                1 for b in bookings

                if b.status == "CONFIRMED"

            ),

            "checked_in": sum(

                1 for b in bookings

                if b.status == "CHECKED_IN"

            ),

            "boarded": sum(

                1 for b in bookings

                if b.status == "BOARDED"

            ),

            "ticketed": sum(

                1 for b in bookings

                if b.status == "TICKETED"

            ),

        },

        "operations": {
        
            "open_alerts": len(alerts),

            "open_risks": len(risks),

            "open_disruptions": len(disruptions),

            "maintenance_events": len(maintenance),

        },

        "alerts": [

            {

                "id": alert.id,

                "flight_id": alert.flight_id,

                "flight_number": (

                    alert.flight.flight_number

                    if alert.flight

                    else None

                ),

                "type": alert.alert_type,

                "severity": alert.severity,

                "title": alert.title,

                "message": alert.message,

                "status": alert.status,

                "created_at": alert.created_at,

            }

            for alert in alerts[:10]

        ],

        "risks": [

            {

                "id": risk.id,

                "flight_id": risk.flight_id,

                "flight_number": risk.flight.flight_number,

                "type": risk.risk_type,

                "severity": risk.severity,

                "score": risk.score,

                "title": risk.title,

                "description": risk.description,

            }

            for risk in risks[:10]

        ],

        "disruptions": [

            {

                "id": disruption.id,

                "flight_id": disruption.flight_id,

                "flight_number": disruption.flight.flight_number,

                "type": disruption.disruption_type,

                "severity": disruption.severity,

                "reason": disruption.reason,

                "status": disruption.status,

            }

            for disruption in disruptions[:10]

        ],

        "maintenance": [

            {

                "id": record.id,

                "aircraft_id": record.aircraft_id,

                "registration": record.aircraft.registration,

                "type": record.maintenance_type,

                "status": record.status,

                "technician": record.technician,

            }

            for record in maintenance[:10]

        ],

        "schedule": [

            {

                "id": schedule.id,

                "flight_id": schedule.flight_id,

                "flight_number": schedule.flight.flight_number,

                "origin": schedule.flight.origin.iata_code,

                "destination": schedule.flight.destination.iata_code,

                "departure": schedule.scheduled_departure,

                "arrival": schedule.scheduled_arrival,

                "status": schedule.status,

                "delay_minutes": schedule.delay_minutes,

            }

            for schedule in schedules[:20]

        ],

    }