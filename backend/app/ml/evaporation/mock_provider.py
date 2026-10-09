from __future__ import annotations

from typing import Any

from .base import BaseEvaporationProvider, PredictionResult


class MockEvaporationProvider(BaseEvaporationProvider):
    """ML INTEGRATION POINT: Demo provider used for development and UI validation; must not be used as a production model."""

    provider_type = 'mock'

    def __init__(self) -> None:
        self._initialized = True
        self._schema = [
            'observation_date',
            'location',
            'rainfall_mm',
            'temperature_c',
            'humidity_pct',
            'sunshine_hours',
            'soil_temperature_c',
            'wind_speed_kmh',
            'pressure_hpa',
        ]

    def initialize(self) -> None:
        self._initialized = True

    def inspect_schema(self) -> list[str]:
        return list(self._schema)

    def validate_inputs(self, payload: dict[str, Any]) -> None:
        required = ['temperature_c', 'humidity_pct', 'sunshine_hours', 'wind_speed_kmh']
        missing = [field for field in required if payload.get(field) is None]
        if missing:
            raise ValueError(f'Missing required fields: {missing}')

    def predict(self, payload: dict[str, Any]) -> PredictionResult:
        self.validate_inputs(payload)
        rainfall = float(payload.get('rainfall_mm') or 0)
        temp = float(payload.get('temperature_c'))
        humidity = float(payload.get('humidity_pct'))
        sunshine = float(payload.get('sunshine_hours'))
        wind = float(payload.get('wind_speed_kmh'))
        soil_temp = float(payload.get('soil_temperature_c') or temp)

        base = 0.18 + (temp * 0.045) + (sunshine * 0.09) + (wind * 0.02) - (humidity * 0.01) + ((soil_temp - temp) * 0.015)
        estimate = max(0.5, min(15.0, base - rainfall * 0.03))
        return PredictionResult(
            value=round(estimate, 2),
            unit='mm/day',
            provider_type=self.provider_type,
            model_version='demo-0.1',
            status='demo',
            explanation='Deterministic demo evaporation estimate for development and UI testing. This is not a scientifically validated ML prediction.',
            uncertainty=0.9,
            input_type=payload.get('input_type', 'manual'),
            location=payload.get('location'),
            observed_date=payload.get('observation_date'),
        )

    @property
    def model_status(self) -> dict[str, Any]:
        return {'provider': self.provider_type, 'status': 'mock_active', 'model_version': 'demo-0.1', 'available': True, 'configured': True, 'message': 'Mock provider active'}

    @property
    def model_version(self) -> str:
        return 'demo-0.1'
