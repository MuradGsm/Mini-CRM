from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_
from app.models.user_model import User
from app.models.client_model import Client
from app.schemas.client_schema import ClientCreate, ClientOut, ClientUpdate
from typing import List
from app.utils.service_utils import get_client_utils

async def create_client_service(user: User, client: ClientCreate, db: AsyncSession) -> Client:
    stmt = select(Client).filter(or_(Client.email == client.email, Client.owner_id == user.id))
    result = await db.execute(stmt)
    new_client = result.scalars().first()
    if new_client is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Client is already')
    new_client = Client(
        full_name=client.full_name,
        email=client.email,
        phone = client.phone,
        notes=client.notes,
        owner_id = user.id
    )
    db.add(new_client)
    await db.commit()
    await db.refresh(new_client)
    return new_client

async def get_all_clients_service(user: User, db: AsyncSession) -> List[Client]:
    stmt = select(Client).filter(Client.owner_id == user.id)
    result = await db.execute(stmt)
    client_list = result.scalars().all()
    return client_list

async def get_client_by_id_service(user: User, client_id: int, db: AsyncSession) -> Client:
    client = await get_client_utils(user, client_id, db)
    return client
    
async def update_client_service(user: User, client_id: int, client_update: ClientUpdate, db: AsyncSession) -> Client:
    client = await get_client_utils(user, client_id, db)
    for field ,value in client_update.dict(exclude_unset=True).items():
        setattr(client, field, value)

    await db.commit()
    await db.refresh(client)
    return client


async def delete_client_service(user: User, client_id: int, db: AsyncSession) -> dict:
    client = await get_client_utils(user, client_id, db)
    await db.delete(client)
    await db.commit()
    return {'Message': "Delete succefully"}