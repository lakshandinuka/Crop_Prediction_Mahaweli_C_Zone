from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ...core.dependencies import get_db
from ...schemas.crop import CropRecommendationInput, CropRecommendationResult
from ...services.crop_service import CropService

router = APIRouter(prefix='/api/v1', tags=['crops'])


@router.get('/crops')
def list_crops(db: Session = Depends(get_db)):
    del db
    return [
        {'id': 1, 'name': 'Rice', 'zone': 'Lowland', 'season': 'Maha', 'description': 'Verified sample crop profile for demonstration.', 'is_verified': False},
        {'id': 2, 'name': 'Maize', 'zone': 'Intermediate', 'season': 'Yala', 'description': 'Sample crop profile for demonstration.', 'is_verified': False},
    ]


@router.get('/crops/{crop_id}')
def crop_detail(crop_id: int):
    return {'id': crop_id, 'name': 'Sample crop', 'description': 'Sample crop profile'}


@router.post('/crops/recommend', response_model=list[CropRecommendationResult])
def recommend(payload: CropRecommendationInput):
    results = CropService().get_recommendations(payload.model_dump())
    return [CropRecommendationResult(**item) for item in results]
