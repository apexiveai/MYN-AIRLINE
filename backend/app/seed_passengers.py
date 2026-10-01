from sqlalchemy import select

from app.db.database import SessionLocal

from app.models.passenger import Passenger

PASSENGERS = [

    {

        "passenger_code": "PAX-0001",

        "first_name": "Aung",

        "last_name": "Min",

        "gender": "MALE",

        "date_of_birth": "1995-04-12",

        "nationality": "Myanmar",

        "passport_number": "MM1234567",

        "phone": "+95-9-710000001",

        "email": "aung.min@example.com",

    },

    {

        "passenger_code": "PAX-0002",

        "first_name": "Su",

        "last_name": "Myat",

        "gender": "FEMALE",

        "date_of_birth": "1998-09-20",

        "nationality": "Myanmar",

        "passport_number": "MM1234568",

        "phone": "+95-9-710000002",

        "email": "su.myat@example.com",

    },

    {

        "passenger_code": "PAX-0003",

        "first_name": "David",

        "last_name": "Tan",

        "gender": "MALE",

        "date_of_birth": "1991-02-18",

        "nationality": "Singapore",

        "passport_number": "SG9876543",

        "phone": "+65-80000003",

        "email": "david.tan@example.com",

    },

]

def main():

    db = SessionLocal()

    try:

        for item in PASSENGERS:

            existing = db.scalar(

                select(Passenger).where(

                    Passenger.passenger_code

                    == item["passenger_code"]

                )

            )

            if existing:

                print(

                    f"[SKIP] "

                    f"{item['passenger_code']}"

                )

                continue

            passenger = Passenger(**item)

            db.add(passenger)

            print(

                f"[CREATED] "

                f"{item['passenger_code']}"

            )

        db.commit()

    finally:

        db.close()

if __name__ == "__main__":

    main()