import os

from ...config import get_settings
from .mock_provider import MockEvaporationProvider
from .sklearn_provider import SklearnEvaporationProvider

settings = get_settings()


def get_evaporation_provider():
    provider_name = (os.getenv('EVAPORATION_PROVIDER') or settings.evaporation_provider or 'mock').lower()
    if provider_name == 'mock':
        provider = MockEvaporationProvider()
        provider.initialize()
        return provider
    if provider_name == 'sklearn':
        provider = SklearnEvaporationProvider(model_path=settings.evaporation_model_path or os.getenv('EVAPORATION_MODEL_PATH'), version=settings.evaporation_model_version)
        try:
            provider.initialize()
        except Exception:
            raise
        return provider
    raise ValueError(f'Unsupported evaporation provider: {provider_name}')
