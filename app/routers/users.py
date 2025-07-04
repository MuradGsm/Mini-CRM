from fastapi import APIRouter, Depends
from app.schemas.user_schema import UserOut, UserCreate
from app.service.user_service import register_service
from app.core.database import get_session

from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix='/users', tags=['Users'])


@router.post('/register', response_model=UserOut)
async def register(user: UserCreate, db: AsyncSession = Depends(get_session)):
    return await register_service(user, db)