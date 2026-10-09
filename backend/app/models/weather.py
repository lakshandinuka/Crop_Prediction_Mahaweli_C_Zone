from sqlalchemy import Column, DateTime, Float, Integer, String, Text
from sqlalchemy.sql import func

from ..db import Base


class WeatherObservation(Base):
    __tablename__ = 'weather_observations'

    id = Column(Integer, primary_key=True, index=True)
    location = Column(String(120), nullable=True)
    observation_date = Column(String(30), nullable=False)
    rainfall_mm = Column(Float, nullable=True)
    temperature_c = Column(Float, nullable=True)
    humidity_pct = Column(Float, nullable=True)
    sunshine_hours = Column(Float, nullable=True)
    soil_temperature_c = Column(Float, nullable=True)
    wind_speed_kmh = Column(Float, nullable=True)
    pressure_hpa = Column(Float, nullable=True)
    evaporation_mm = Column(Float, nullable=True)
    data_provenance = Column(String(120), default='observed')
    note = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Farm(Base):
    __tablename__ = 'farms'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(120), nullable=False)
    location = Column(String(120), nullable=True)
    area_ha = Column(Float, nullable=True)
    owner_id = Column(Integer, nullable=True)
