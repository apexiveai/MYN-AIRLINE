from sqlalchemy import select

from app.db.database import SessionLocal

from app.models.crew import Crew

CREW = [

    {

        "employee_code": "MNA-CPT-001",

        "full_name": "Captain Aung Min",

        "role": "CAPTAIN",

        "license_number": "MM-ATPL-001",

        "base_airport": "RGN",

        "status": "AVAILABLE",

        "phone": "+95-9-700000001",

        "email": "captain001@mna.example",

    },

    {

        "employee_code": "MNA-CPT-002",

        "full_name": "Captain Kyaw Zin",

        "role": "CAPTAIN",

        "license_number": "MM-ATPL-002",

        "base_airport": "RGN",

        "status": "AVAILABLE",

        "phone": "+95-9-700000002",

        "email": "captain002@mna.example",

    },

    {

        "employee_code": "MNA-FO-001",

        "full_name": "First Officer Thant Zin",

        "role": "FIRST_OFFICER",

        "license_number": "MM-CPL-001",

        "base_airport": "RGN",

        "status": "AVAILABLE",

        "phone": "+95-9-700000003",

        "email": "fo001@mna.example",

    },

    {

        "employee_code": "MNA-FO-002",

        "full_name": "First Officer Min Htet",

        "role": "FIRST_OFFICER",

        "license_number": "MM-CPL-002",

        "base_airport": "RGN",

        "status": "AVAILABLE",

        "phone": "+95-9-700000004",

        "email": "fo002@mna.example",

    },

    {

        "employee_code": "MNA-CAB-001",

        "full_name": "Cabin Crew Su Su",

        "role": "CABIN_CREW",

        "license_number": None,

        "base_airport": "RGN",

        "status": "AVAILABLE",

        "phone": "+95-9-700000005",

        "email": "cabin001@mna.example",

    },

    {

        "employee_code": "MNA-CAB-002",

        "full_name": "Cabin Crew Ei Ei",

        "role": "CABIN_CREW",

        "license_number": None,

        "base_airport": "RGN",

        "status": "AVAILABLE",

        "phone": "+95-9-700000006",

        "email": "cabin002@mna.example",

    },

]

def main():

    db = SessionLocal()

    try:

        for item in CREW:

            existing = db.scalar(

                select(Crew).where(

                    Crew.employee_code

                    == item["employee_code"]

                )

            )

            if existing:

                print(

                    f"[SKIP] "

                    f"{item['employee_code']}"

                )

                continue

            crew = Crew(**item)

            db.add(crew)

            print(

                f"[CREATED] "

                f"{item['employee_code']} "

                f"{item['full_name']}"

            )

        db.commit()

    finally:

        db.close()

if __name__ == "__main__":

    main()