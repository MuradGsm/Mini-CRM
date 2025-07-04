from fastapi import HTTPException, status
from app.schemas.user_schema import UserCreate, UserLogin
from app.models.user_model import User
from app.utils.security import hash_password, verify_password
from app.utils.jwt import create_access_token
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


async def login_service(user: UserLogin, db: AsyncSession):
    stmt = select(User).filter(or_(User.username == user.username_or_email, User.email == user.username_or_email))
    result = await db.execute(stmt)
    log_user = result.scalars().first()
    if log_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User nof found')
    if not verify_password(user.password, log_user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="The password or email is incorrect !")
    access_token = create_access_token(data={"sub": str(log_user.id)})
    return {"access_token": access_token, "token_type": "bearer"}