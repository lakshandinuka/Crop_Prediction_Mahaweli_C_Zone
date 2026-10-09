from typing import Literal, Optional

from pydantic import BaseModel, Field


class EvaporationInput(BaseModel):
    observation_date: str
    location: Optional[str] = None
    rainfall_mm: Optional[float] = Field(default=None, ge=0)
    temperature_c: Optional[float] = Field(default=None)
    humidity_pct: Optional[float] = Field(default=None, ge=0, le=100)
    sunshine_hours: Optional[float] = Field(default=None, ge=0)
    soil_temperature_c: Optional[float] = Field(default=None)
    wind_speed_kmh: Optional[float] = Field(default=None, ge=0)
    pressure_hpa: Optional[float] = Field(default=None, ge=0)
    input_type: Literal['observed', 'manual', 'simulated'] = 'manual'


class EvaporationPredictionResponse(BaseModel):
    value: float
    unit: str = 'mm/day'
    provider_type: str
    model_version: str
    status: str
    explanation: str
    uncertainty: Optional[float] = None
    input_type: str
    location: Optional[str] = None
    observed_date: Optional[str] = None


class ModelStatusResponse(BaseModel):
    provider: str
    status: str
    model_version: str
    configured: bool
    available: bool
    message: str
