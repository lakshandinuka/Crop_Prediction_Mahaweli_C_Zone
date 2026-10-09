from pydantic import BaseModel, Field


class WaterEstimateInput(BaseModel):
    crop: str
    stage: str
    etc_mm_day: float = Field(..., gt=0)
    effective_rainfall_mm_day: float = Field(..., ge=0)
    field_area_m2: float = Field(..., gt=0)
    irrigation_efficiency: float = Field(..., gt=0, le=100)


class WaterEstimateOutput(BaseModel):
    crop: str
    stage: str
    etc_mm_day: float
    net_irrigation_mm_day: float
    gross_irrigation_depth_mm: float
    net_volume_litres: float
    gross_volume_litres: float
    irrigation_efficiency_pct: float
    assumptions: str
