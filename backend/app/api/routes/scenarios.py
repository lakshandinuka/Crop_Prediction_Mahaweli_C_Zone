from fastapi import APIRouter

router = APIRouter(prefix='/api/v1', tags=['scenarios'])


@router.post('/scenarios/compare')
def compare():
    return {'scenarios': [{'name': 'Baseline', 'water_demand_mm_day': 4.2}, {'name': 'High efficiency', 'water_demand_mm_day': 3.1}]}


@router.get('/analytics/seasonal')
def seasonal():
    return {'labels': ['Jan', 'Feb', 'Mar'], 'rainfall': [110, 90, 75], 'temperature': [28, 29, 30]}
