from datetime import date, time

from sqlalchemy import select

from app.db.database import SessionLocal

from app.models.flight import Flight

from app.models.flight_schedule import FlightSchedule

SCHEDULES = [

    {

        "flight_number": "UB001",

        "departure": time(8, 30),

        "arrival": time(10, 15),

    },

    {

        "flight_number": "UB102",

        "departure": time(11, 0),

        "arrival": time(12, 15),

    },

    {

        "flight_number": "UB207",

        "departure": time(13, 20),

        "arrival": time(17, 45),

    },

    {

        "flight_number": "UB315",

        "departure": time(15, 10),

        "arrival": time(16, 50),

    },

]

def main():

    db = SessionLocal()

    try:

        today = date.today()

        for item in SCHEDULES:

            flight = db.scalar(

                select(Flight).where(

                    Flight.flight_number

                    == item["flight_number"]

                )

            )

            if not flight:

                print(

                    f"[ERROR] Flight not found: "

                    f"{item['flight_number']}"

                )

                continue

            existing = db.scalar(

                select(FlightSchedule).where(

                    FlightSchedule.flight_id

                    == flight.id,

                    FlightSchedule.operating_date

                    == today,

                )

            )

            if existing:

                print(

                    f"[SKIP] "

                    f"{item['flight_number']}"

                )

                continue

            schedule = FlightSchedule(

                flight_id=flight.id,

                operating_date=today,

                scheduled_departure=(

                    item["departure"]

                ),

                scheduled_arrival=(

                    item["arrival"]

                ),

                status=flight.status,

                delay_minutes=0,

            )

            db.add(schedule)

            print(

                f"[CREATED] "

                f"{item['flight_number']} "

                f"{today}"

            )

        db.commit()

    finally:

        db.close()

if __name__ == "__main__":

    main()