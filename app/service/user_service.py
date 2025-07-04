from fastapi import HTTPException, status
from app.schemas.user_schema import UserCreate
from app.models.user_model import User
from app.utils.security import hash_password
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_

async def register_service(user: UserCreate, db: AsyncSession) -> User:
    stmt = select(User).filter(or_(User.username == user.username, User.email == user.email))
    result  = await db.execute(stmt) 
    new_user = result.scalars().first()
    if new_user is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='A user with this email is already registered')
    hashed_pw = hash_password(user.password)
    new_user = User(username=user.username, email=user.email, hashed_password=hashed_pw)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user
