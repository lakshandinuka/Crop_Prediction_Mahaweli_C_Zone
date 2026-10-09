from typing import Any

from ..ml.crop_recommendation.mock_provider import MockCropRecommendationProvider


class CropService:
    def get_recommendations(self, payload: dict[str, Any]) -> list[dict[str, Any]]:
        return MockCropRecommendationProvider().recommend(payload)
