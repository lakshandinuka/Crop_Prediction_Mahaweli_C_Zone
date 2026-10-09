from sqlalchemy import Column, DateTime, Float, Integer, String, Text
from sqlalchemy.sql import func

from ..db import Base


class EvaporationPrediction(Base):
    __tablename__ = 'evaporation_predictions'

    id = Column(Integer, primary_key=True, index=True)
    source_type = Column(String(40), nullable=False)
    model_version = Column(String(80), nullable=True)
    input_type = Column(String(40), nullable=False, default='manual')
    location = Column(String(120), nullable=True)
    observed_date = Column(String(30), nullable=True)
    rainfall_mm = Column(Float, nullable=True)
    temperature_c = Column(Float, nullable=True)
    humidity_pct = Column(Float, nullable=True)
    sunshine_hours = Column(Float, nullable=True)
    soil_temperature_c = Column(Float, nullable=True)
    wind_speed_kmh = Column(Float, nullable=True)
    pressure_hpa = Column(Float, nullable=True)
    predicted_evaporation_mm_day = Column(Float, nullable=False)
    unit = Column(String(30), nullable=False, default='mm/day')
    provider_type = Column(String(60), nullable=False, default='mock')
    status = Column(String(50), nullable=False, default='demo')
    explanation = Column(Text, nullable=True)
    uncertainty = Column(Float, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
