from fastapi import APIRouter, Depends
from app.schemas.user_schema import UserOut, UserCreate, UserLogin
from app.service.user_service import register_service,login_service
from app.core.database import get_session
from app.dependencies.auth import get_current_user
from app.models.user_model import User
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(prefix='/users', tags=['Users'])


@router.post('/register', response_model=UserOut)
async def register(user: UserCreate, db: AsyncSession = Depends(get_session)):
    return await register_service(user, db)

@router.post('/login')
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_session)) -> dict:
    user = UserLogin(username_or_email=form_data.username, password=form_data.password)
    return await login_service(user, db)

@router.get("/me", response_model=UserOut)
async def get_me(current_user: User = Depends(get_current_user)):
    return {"email": current_user.email, "id": current_user.id}