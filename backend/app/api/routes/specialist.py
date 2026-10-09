from fastapi import APIRouter, Depends

from ...core.dependencies import get_current_user, require_roles
from ...models.user import User

router = APIRouter(prefix='/api/v1/specialist', tags=['specialist'])


@router.get('/dashboard')
def dashboard(current_user: User = Depends(require_roles('specialist', 'admin'))):
    return {'user': current_user.email, 'reports_count': 3, 'predictions_count': 15, 'status': 'ok'}


@router.get('/reports')
def reports(current_user: User = Depends(require_roles('specialist', 'admin'))):
    return {'reports': [{'title': 'Seasonal water plan', 'status': 'draft'}], 'user': current_user.email}
