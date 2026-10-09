from .base import CropRecommendationBase


class MockCropRecommendationProvider(CropRecommendationBase):
    def recommend(self, payload):
        base = [
            {'crop_name': 'Rice', 'suitability_score': 88, 'suitable_season': 'Maha', 'zone': 'Lowland', 'growth_duration_days': 140, 'source': 'demo'},
            {'crop_name': 'Maize', 'suitability_score': 81, 'suitable_season': 'Yala', 'zone': 'Intermediate', 'growth_duration_days': 110, 'source': 'demo'},
            {'crop_name': 'Chilli', 'suitability_score': 74, 'suitable_season': 'Yala', 'zone': 'Dry zone', 'growth_duration_days': 95, 'source': 'demo'},
        ]
        return base
