from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from ...core.dependencies import get_current_user, get_db
from ...core.security import create_access_token, hash_password, verify_password
from ...models.user import User
from ...schemas.auth import AuthToken, LoginRequest, UserOut

router = APIRouter(prefix='/api/v1/auth', tags=['auth'])


@router.post('/login', response_model=AuthToken)
def login(payload: LoginRequest, db: Session = Depends(get_db), response: Response = None):
    user = db.query(User).filter(User.email == payload.email).first()
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid credentials')
    token = create_access_token(user.email, {'role': user.role, 'user_id': user.id})
    response.set_cookie('agriwater_access', token, httponly=True, samesite='lax', secure=False)
    return AuthToken(access_token=token, user={'id': user.id, 'email': user.email, 'role': user.role, 'username': user.username, 'full_name': user.full_name})


@router.get('/me', response_model=UserOut)
def me(current_user: User = Depends(get_current_user)):
    return UserOut(id=current_user.id, email=current_user.email, username=current_user.username, full_name=current_user.full_name, role=current_user.role, is_active=current_user.is_active)


@router.post('/logout')
def logout(response: Response):
    response.delete_cookie('agriwater_access')
    return {'status': 'logged_out'}


@router.post('/bootstrap-admin')
def bootstrap_admin(email: str, password: str, full_name: str, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == email).first():
        return {'status': 'already_exists'}
    user = User(email=email, username=email.split('@')[0], full_name=full_name, hashed_password=hash_password(password), role='admin', is_active=True)
    db.add(user)
    db.commit()
    return {'status': 'created', 'email': email}
