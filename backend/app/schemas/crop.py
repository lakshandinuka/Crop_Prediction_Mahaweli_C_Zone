from typing import Optional

from pydantic import BaseModel, Field


class CropRecommendationInput(BaseModel):
    location: str
    planting_date: str
    season: str
    soil_type: Optional[str] = None
    water_availability: Optional[float] = Field(default=None, ge=0)
    field_size_ha: Optional[float] = Field(default=None, gt=0)
    rainfall_mm: Optional[float] = Field(default=None, ge=0)
    expected_temperature_c: Optional[float] = Field(default=None)


class CropRecommendationResult(BaseModel):
    crop_name: str
    suitability_score: Optional[float] = None
    suitable_season: Optional[str] = None
    zone: Optional[str] = None
    growth_duration_days: Optional[int] = None
    source: str = 'demo'
