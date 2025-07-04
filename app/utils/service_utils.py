from fastapi import HTTPException, status
from app.models.user_model import User
from app.models.client_model import Client
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

async def get_client_utils(user: User, client_id: int, db: AsyncSession):
    stmt = select(Client).filter(Client.id == client_id)
    result = await db.execute(stmt)
    client = result.scalars().first()
    if client is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Client no found')
    if client.owner_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    return client