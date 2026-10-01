from sqlalchemy import select

from app.db.database import SessionLocal

from app.models.aircraft import Aircraft

from app.models.airport import Airport

from app.models.flight import Flight

FLIGHTS = [

    {

        "flight_number": "UB001",

        "origin": "RGN",

        "destination": "BKK",

        "aircraft": "XY-002",

        "gate": "A01",

        "status": "AIRBORNE",

        "departure_time": "08:30",

        "arrival_time": "10:15",

        "latitude": 17.85,

        "longitude": 97.25,

        "altitude": 32000,

        "speed": 450,

        "heading": 72,

    },

    {

        "flight_number": "UB102",

        "origin": "RGN",

        "destination": "MDL",

        "aircraft": "XY-003",

        "gate": "A02",

        "status": "BOARDING",

        "departure_time": "11:00",

        "arrival_time": "12:15",

        "latitude": 16.9073,

        "longitude": 96.1332,

        "altitude": 0,

        "speed": 0,

        "heading": 0,

    },

    {

        "flight_number": "UB207",

        "origin": "RGN",

        "destination": "SIN",

        "aircraft": "XY-001",

        "gate": "B04",

        "status": "SCHEDULED",

        "departure_time": "13:20",

        "arrival_time": "17:45",

        "latitude": 16.9073,

        "longitude": 96.1332,

        "altitude": 0,

        "speed": 0,

        "heading": 0,

    },

    {

        "flight_number": "UB315",

        "origin": "RGN",

        "destination": "CNX",

        "aircraft": "XY-002",

        "gate": "B07",

        "status": "DELAYED",

        "departure_time": "15:10",

        "arrival_time": "16:50",

        "latitude": 16.9073,

        "longitude": 96.1332,

        "altitude": 0,

        "speed": 0,

        "heading": 0,

    },

]

def main():

    db = SessionLocal()

    try:

        for item in FLIGHTS:

            existing = db.scalar(

                select(Flight).where(

                    Flight.flight_number

                    == item["flight_number"]

                )

            )

            if existing:

                print(

                    f"[SKIP] {item['flight_number']}"

                )

                continue

            origin = db.scalar(

                select(Airport).where(

                    Airport.iata_code

                    == item["origin"]

                )

            )

            destination = db.scalar(

                select(Airport).where(

                    Airport.iata_code

                    == item["destination"]

                )

            )

            aircraft = db.scalar(

                select(Aircraft).where(

                    Aircraft.registration

                    == item["aircraft"]

                )

            )

            if not origin:

                print(

                    f"[ERROR] Airport not found: "

                    f"{item['origin']}"

                )

                continue

            if not destination:

                print(

                    f"[ERROR] Airport not found: "

                    f"{item['destination']}"

                )

                continue

            if not aircraft:

                print(

                    f"[ERROR] Aircraft not found: "

                    f"{item['aircraft']}"

                )

                continue

            flight = Flight(

                flight_number=item["flight_number"],

                origin_id=origin.id,

                destination_id=destination.id,

                aircraft_id=aircraft.id,

                gate=item["gate"],

                status=item["status"],

                departure_time=item["departure_time"],

                arrival_time=item["arrival_time"],

                latitude=item["latitude"],

                longitude=item["longitude"],

                altitude=item["altitude"],

                speed=item["speed"],

                heading=item["heading"],

            )

            db.add(flight)

            print(

                f"[CREATED] "
f"{item['flight_number']} "

                f"{item['origin']} → "

                f"{item['destination']}"

            )

        db.commit()

    finally:

        db.close()

if __name__ == "__main__":

    main()