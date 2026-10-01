from pydantic import BaseModel

class CrewCreate(BaseModel):

    employee_code: str

    full_name: str

    role: str

    license_number: str | None = None

    base_airport: str

    status: str = "AVAILABLE"

    phone: str | None = None

    email: str | None = None

class CrewUpdate(BaseModel):

    full_name: str | None = None

    role: str | None = None

    license_number: str | None = None

    base_airport: str | None = None

    status: str | None = None

    phone: str | None = None

    email: str | None = None

class CrewResponse(BaseModel):

    id: int

    employee_code: str

    full_name: str

    role: str

    license_number: str | None

    base_airport: str

    status: str

    phone: str | None

    email: str | None

    model_config = {

        "from_attributes": True,

    }

class FlightCrewCreate(BaseModel):

    crew_id: int

    duty_role: str

class FlightCrewResponse(BaseModel):

    id: int

    flight_id: int

    crew_id: int

    duty_role: str

    crew_name: str

    employee_code: str