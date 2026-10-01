from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy import select

from sqlalchemy.orm import Session

from app.db.database import get_db

from app.models.airport import Airport

from app.models.weather import WeatherObservation

from app.schemas.weather import (

    WeatherCreate,

    WeatherResponse,

)

router = APIRouter(

    prefix="/api/weather",

    tags=["Weather"],

)

def weather_to_response(

    weather: WeatherObservation,

) -> dict:

    return {

        "id": weather.id,

        "airport_id": weather.airport_id,

        "iata_code": weather.airport.iata_code,

        "airport_name": weather.airport.name,

        "temperature_c": weather.temperature_c,

        "wind_speed_kmh": weather.wind_speed_kmh,

        "wind_direction": weather.wind_direction,

        "visibility_km": weather.visibility_km,

        "precipitation_mm": weather.precipitation_mm,

        "cloud_cover": weather.cloud_cover,

        "condition": weather.condition,

        "risk_level": weather.risk_level,

        "observed_at": weather.observed_at,

    }

@router.get(

    "",

    response_model=list[WeatherResponse],

)

def list_weather(

    airport_id: int | None = None,

    db: Session = Depends(get_db),

):

    query = select(WeatherObservation)

    if airport_id is not None:

        query = query.where(

            WeatherObservation.airport_id == airport_id

        )

    records = db.scalars(

        query.order_by(

            WeatherObservation.observed_at.desc()

        )

    ).all()

    return [

        weather_to_response(record)

        for record in records

    ]

@router.get(

    "/airport/{airport_id}",

    response_model=WeatherResponse,

)

def latest_weather(

    airport_id: int,

    db: Session = Depends(get_db),

):

    airport = db.get(Airport, airport_id)

    if not airport:

        raise HTTPException(

            status_code=404,

            detail="Airport not found",

        )

    weather = db.scalar(

        select(WeatherObservation)

        .where(

            WeatherObservation.airport_id

            == airport_id

        )

        .order_by(

            WeatherObservation.observed_at.desc()

        )

    )

    if not weather:

        raise HTTPException(

            status_code=404,

            detail="Weather observation not found",

        )

    return weather_to_response(weather)

@router.post(

    "",

    response_model=WeatherResponse,

    status_code=201,

)

def create_weather(

    payload: WeatherCreate,

    db: Session = Depends(get_db),

):

    airport = db.get(

        Airport,

        payload.airport_id,

    )

    if not airport:

        raise HTTPException(

            status_code=404,

            detail="Airport not found",

        )

    if not 0 <= payload.cloud_cover <= 100:

        raise HTTPException(

            status_code=400,

            detail="Cloud cover must be between 0 and 100",

        )

    if payload.visibility_km < 0:

        raise HTTPException(

            status_code=400,

            detail="Visibility cannot be negative",

        )

    weather = WeatherObservation(

        airport_id=payload.airport_id,

        temperature_c=payload.temperature_c,

        wind_speed_kmh=payload.wind_speed_kmh,

        wind_direction=payload.wind_direction,

        visibility_km=payload.visibility_km,

        precipitation_mm=payload.precipitation_mm,

        cloud_cover=payload.cloud_cover,

        condition=payload.condition,

        risk_level=payload.risk_level,

    )

    db.add(weather)

    db.commit()

    db.refresh(weather)

    return weather_to_response(weather)