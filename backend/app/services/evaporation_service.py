from __future__ import annotations

from sqlalchemy.orm import Session

from ..ml.evaporation.base import PredictionResult
from ..ml.evaporation.registry import get_evaporation_provider
from ..models.prediction import EvaporationPrediction


class EvaporationService:
    def __init__(self, db: Session):
        self.db = db

    def predict(self, payload: dict) -> PredictionResult:
        provider = get_evaporation_provider()
        result = provider.predict(payload)
        record = EvaporationPrediction(
            source_type='request',
            model_version=result.model_version,
            input_type=payload.get('input_type', 'manual'),
            location=payload.get('location'),
            observed_date=payload.get('observation_date'),
            rainfall_mm=payload.get('rainfall_mm'),
            temperature_c=payload.get('temperature_c'),
            humidity_pct=payload.get('humidity_pct'),
            sunshine_hours=payload.get('sunshine_hours'),
            soil_temperature_c=payload.get('soil_temperature_c'),
            wind_speed_kmh=payload.get('wind_speed_kmh'),
            pressure_hpa=payload.get('pressure_hpa'),
            predicted_evaporation_mm_day=result.value,
            unit=result.unit,
            provider_type=result.provider_type,
            status=result.status,
            explanation=result.explanation,
            uncertainty=result.uncertainty,
        )
        self.db.add(record)
        self.db.commit()
        return result

    def get_status(self):
        provider = get_evaporation_provider()
        return provider.model_status
