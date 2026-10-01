from pydantic import BaseModel

class PassengerCreate(BaseModel):

    passenger_code: str

    first_name: str

    last_name: str

    gender: str | None = None

    date_of_birth: str | None = None

    nationality: str | None = None

    passport_number: str | None = None

    phone: str | None = None

    email: str | None = None

class PassengerUpdate(BaseModel):

    first_name: str | None = None

    last_name: str | None = None

    gender: str | None = None

    date_of_birth: str | None = None

    nationality: str | None = None

    passport_number: str | None = None

    phone: str | None = None

    email: str | None = None

class PassengerResponse(BaseModel):

    id: int

    passenger_code: str

    first_name: str

    last_name: str

    gender: str | None

    date_of_birth: str | None

    nationality: str | None

    passport_number: str | None

    phone: str | None

    email: str | None

    model_config = {

        "from_attributes": True,

    }