from app.db.database import SessionLocal
from app.models.aircraft import Aircraft


AIRCRAFT = [
    {
        "registration": "XY-001",
        "model": "B737-800",
        "manufacturer": "Boeing",
        "seat_capacity": 162,
        "status": "AVAILABLE",
    },
    {
        "registration": "XY-002",
        "model": "B737-800",
        "manufacturer": "Boeing",
        "seat_capacity": 162,
        "status": "IN_SERVICE",
    },
    {
        "registration": "XY-003",
        "model": "ATR 72",
        "manufacturer": "ATR",
        "seat_capacity": 72,
        "status": "IN_SERVICE",
    },
    {
        "registration": "XY-004",
        "model": "A320",
        "manufacturer": "Airbus",
        "seat_capacity": 180,
        "status": "MAINTENANCE",
    },
]


def seed():
    db = SessionLocal()

    try:
        for item in AIRCRAFT:
            existing = (
                db.query(Aircraft)
                .filter(
                    Aircraft.registration
                    == item["registration"]
                )
                .first()
            )

            if existing:
                continue

            db.add(Aircraft(**item))

        db.commit()

        print(
            "[MNA] Aircraft fleet seeded successfully."
        )

    finally:
        db.close()


if __name__ == "__main__":
    seed()