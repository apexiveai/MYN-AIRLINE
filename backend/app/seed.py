from app.db.database import Base, SessionLocal, engine
from app.models.flight import Flight


def seed():
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    try:
        if db.query(Flight).count() > 0:
            print("[MNA] Flights already exist.")
            return

        flights = [
            Flight(
                flight_number="UB001",
                origin="RGN",
                destination="BKK",
                aircraft="B737-800",
                gate="A03",
                status="AIRBORNE",
                departure_time="08:10",
                arrival_time="10:45",
                latitude=17.42,
                longitude=96.25,
                altitude=31000,
                speed=448,
                heading=78,
            ),
            Flight(
                flight_number="UB102",
                origin="RGN",
                destination="MDL",
                aircraft="ATR 72",
                gate="B02",
                status="BOARDING",
                departure_time="10:50",
                arrival_time="12:00",
                latitude=16.91,
                longitude=96.13,
                altitude=0,
                speed=0,
                heading=0,
            ),
            Flight(
                flight_number="UB207",
                origin="RGN",
                destination="SIN",
                aircraft="A320",
                gate="A07",
                status="SCHEDULED",
                departure_time="12:05",
                arrival_time="15:20",
                latitude=16.91,
                longitude=96.13,
                altitude=0,
                speed=0,
                heading=0,
            ),
            Flight(
                flight_number="UB315",
                origin="RGN",
                destination="CNX",
                aircraft="B737-800",
                gate="B05",
                status="DELAYED",
                departure_time="13:10",
                arrival_time="14:25",
                latitude=17.08,
                longitude=96.31,
                altitude=18000,
                speed=365,
                heading=12,
            ),
        ]

        db.add_all(flights)
        db.commit()

        print(
            "[MNA] Initial flights inserted successfully."
        )

    finally:
        db.close()


if __name__ == "__main__":
    seed()