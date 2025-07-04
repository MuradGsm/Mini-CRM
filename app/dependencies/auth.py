from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_session
from app.models.user_model import User
from app.utils.jwt import decode_access_token
from sqlalchemy import select

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/users/login')

async def get_current_user(
        token: str = Depends(oauth2_scheme),
        db: AsyncSession =Depends(get_session),
) -> User:
    try:
        user_id = int(decode_access_token(token))
        stmt = select(User).where(User.id == user_id)
        result = await db.execute(stmt)
        user = result.scalars().first()
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
        return user
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid token')