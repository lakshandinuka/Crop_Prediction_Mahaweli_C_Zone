from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ...core.dependencies import get_db
from ...schemas.evaporation import EvaporationInput, EvaporationPredictionResponse, ModelStatusResponse
from ...services.evaporation_service import EvaporationService

router = APIRouter(prefix='/api/v1/evaporation', tags=['evaporation'])


@router.post('/predict', response_model=EvaporationPredictionResponse)
def predict(payload: EvaporationInput, db: Session = Depends(get_db)):
    service = EvaporationService(db)
    try:
        result = service.predict(payload.model_dump())
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    return EvaporationPredictionResponse(
        value=result.value,
        unit=result.unit,
        provider_type=result.provider_type,
        model_version=result.model_version,
        status=result.status,
        explanation=result.explanation,
        uncertainty=result.uncertainty,
        input_type=result.input_type,
        location=result.location,
        observed_date=result.observed_date,
    )


@router.get('/model-status', response_model=ModelStatusResponse)
def model_status(db: Session = Depends(get_db)):
    service = EvaporationService(db)
    status_info = service.get_status()
    return ModelStatusResponse(**status_info)


@router.get('/history')
def history(db: Session = Depends(get_db), limit: int = 10):
    from ...models.prediction import EvaporationPrediction
    rows = db.query(EvaporationPrediction).order_by(EvaporationPrediction.created_at.desc()).limit(limit).all()
    return [{'id': r.id, 'value': r.predicted_evaporation_mm_day, 'provider_type': r.provider_type, 'status': r.status, 'location': r.location, 'created_at': str(r.created_at)} for r in rows]
