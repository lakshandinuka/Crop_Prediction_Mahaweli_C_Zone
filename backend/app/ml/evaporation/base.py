from abc import ABC, abstractmethod
from dataclasses import asdict, dataclass
from typing import Any, Optional


@dataclass
class PredictionResult:
    value: float
    unit: str = 'mm/day'
    provider_type: str = 'base'
    model_version: str = 'unknown'
    status: str = 'unknown'
    explanation: str = ''
    uncertainty: Optional[float] = None
    input_type: str = 'manual'
    location: Optional[str] = None
    observed_date: Optional[str] = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class BaseEvaporationProvider(ABC):
    """ML INTEGRATION POINT: Replace/configure this provider when the trained evaporation model is ready."""

    provider_type: str = 'base'

    @abstractmethod
    def initialize(self) -> None:
        pass

    @abstractmethod
    def inspect_schema(self) -> list[str]:
        pass

    @abstractmethod
    def validate_inputs(self, payload: dict[str, Any]) -> None:
        pass

    @abstractmethod
    def predict(self, payload: dict[str, Any]) -> PredictionResult:
        pass

    @property
    @abstractmethod
    def model_status(self) -> dict[str, Any]:
        pass

    @property
    @abstractmethod
    def model_version(self) -> str:
        pass
