from fastapi import APIRouter, Depends

from ...core.dependencies import require_roles
from ...models.user import User

router = APIRouter(prefix='/api/v1/admin', tags=['admin'])


@router.get('/dashboard')
def dashboard(current_user: User = Depends(require_roles('admin'))):
    return {'users': 17, 'active_users': 11, 'audit_events': 42, 'status': 'ok', 'user': current_user.email}


@router.get('/audit-logs')
def audit_logs(current_user: User = Depends(require_roles('admin'))):
    return {'logs': [{'event': 'login', 'actor': 'admin@demo.org'}], 'user': current_user.email}


@router.get('/model-status')
def model_status(current_user: User = Depends(require_roles('admin'))):
    return {'provider': 'mock', 'status': 'mock_active', 'configured': True, 'available': True, 'version': 'demo-0.1'}
