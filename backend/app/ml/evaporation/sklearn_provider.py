from __future__ import annotations

import os
from typing import Any, Optional

import joblib

from .base import BaseEvaporationProvider, PredictionResult


class SklearnEvaporationProvider(BaseEvaporationProvider):
    """ML INTEGRATION POINT: Replace this adapter when a trained sklearn artifact is ready. It expects a joblib model and matching feature ordering."""

    provider_type = 'sklearn'

    def __init__(self, model_path: Optional[str] = None, version: str = 'dev') -> None:
        self.model_path = model_path or os.getenv('EVAPORATION_MODEL_PATH', '')
        self.version = version or os.getenv('EVAPORATION_MODEL_VERSION', 'development')
        self.model = None
        self.feature_order = ['rainfall_mm', 'temperature_c', 'humidity_pct', 'sunshine_hours', 'soil_temperature_c', 'wind_speed_kmh', 'pressure_hpa']
        self._initialized = False

    def initialize(self) -> None:
        if not self.model_path:
            raise FileNotFoundError('No model artifact path configured')
        if not os.path.exists(self.model_path):
            raise FileNotFoundError(f'Model artifact not found at {self.model_path}')
        self.model = joblib.load(self.model_path)
        self._initialized = True

    def inspect_schema(self) -> list[str]:
        return list(self.feature_order)

    def validate_inputs(self, payload: dict[str, Any]) -> None:
        missing = [field for field in self.feature_order if payload.get(field) is None]
        if missing:
            raise ValueError(f'Missing required ML features: {missing}')

    def predict(self, payload: dict[str, Any]) -> PredictionResult:
        if not self._initialized or self.model is None:
            raise RuntimeError('Real model not loaded')
        feature_vector = [float(payload.get(field)) for field in self.feature_order]
        value = float(self.model.predict([feature_vector])[0])
        return PredictionResult(
            value=round(value, 2),
            unit='mm/day',
            provider_type=self.provider_type,
            model_version=self.version,
            status='real_model',
            explanation='Prediction produced using the configured trained ML model.',
            uncertainty=None,
            input_type=payload.get('input_type', 'manual'),
            location=payload.get('location'),
            observed_date=payload.get('observation_date'),
        )

    @property
    def model_status(self) -> dict[str, Any]:
        if not self.model_path:
            return {'provider': self.provider_type, 'status': 'not_configured', 'model_version': self.version, 'available': False, 'configured': False, 'message': 'Model not configured'}
        if not self._initialized:
            return {'provider': self.provider_type, 'status': 'configured_unavailable', 'model_version': self.version, 'available': False, 'configured': True, 'message': 'Model configured but unavailable'}
        return {'provider': self.provider_type, 'status': 'real_model_loaded', 'model_version': self.version, 'available': True, 'configured': True, 'message': 'Model loaded successfully'}

    @property
    def model_version(self) -> str:
        return self.version
