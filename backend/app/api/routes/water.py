from fastapi import APIRouter

from ...schemas.water import WaterEstimateInput, WaterEstimateOutput
from ...services.water_balance_service import WaterBalanceService

router = APIRouter(prefix='/api/v1', tags=['water'])


@router.post('/water/estimate', response_model=WaterEstimateOutput)
def estimate(payload: WaterEstimateInput):
    estimate_data = WaterBalanceService.estimate_water(
        crop=payload.crop,
        stage=payload.stage,
        etc_mm_day=payload.etc_mm_day,
        effective_rainfall_mm_day=payload.effective_rainfall_mm_day,
        field_area_m2=payload.field_area_m2,
        irrigation_efficiency=payload.irrigation_efficiency,
    )
    return WaterEstimateOutput(**estimate_data)
