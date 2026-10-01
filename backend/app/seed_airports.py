from app.db.database import SessionLocal
from app.models.airport import Airport


AIRPORTS = [
    {
        "iata_code": "RGN",
        "icao_code": "VYYY",
        "name": "Yangon International Airport",
        "city": "Yangon",
        "country": "Myanmar",
        "latitude": 16.9073,
        "longitude": 96.1332,
    },
    {
        "iata_code": "MDL",
        "icao_code": "VYMD",
        "name": "Mandalay International Airport",
        "city": "Mandalay",
        "country": "Myanmar",
        "latitude": 21.7022,
        "longitude": 95.9779,
    },
    {
        "iata_code": "BKK",
        "icao_code": "VTBS",
        "name": "Suvarnabhumi Airport",
        "city": "Bangkok",
        "country": "Thailand",
        "latitude": 13.6900,
        "longitude": 100.7501,
    },
    {
        "iata_code": "SIN",
        "icao_code": "WSSS",
        "name": "Singapore Changi Airport",
        "city": "Singapore",
        "country": "Singapore",
        "latitude": 1.3644,
        "longitude": 103.9915,
    },
    {
        "iata_code": "CNX",
        "icao_code": "VTCC",
        "name": "Chiang Mai International Airport",
        "city": "Chiang Mai",
        "country": "Thailand",
        "latitude": 18.7668,
        "longitude": 98.9626,
    },
]


def seed():
    db = SessionLocal()

    try:
        for item in AIRPORTS:
            existing = (
                db.query(Airport)
                .filter(
                    Airport.iata_code
                    == item["iata_code"]
                )
                .first()
            )

            if existing:
                continue

            db.add(Airport(**item))

        db.commit()

        print(
            "[MNA] Airports seeded successfully."
        )

    finally:
        db.close()


if __name__ == "__main__":
    seed()