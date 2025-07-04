from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.client_schema import ClientOut, ClientCreate, ClientUpdate
from app.dependencies.auth import get_current_user
from app.core.database import get_session
from app.models.user_model import User
from typing import List
from app.service.client_service import (create_client_service, 
                                        get_all_clients_service, 
                                        get_client_by_id_service, 
                                        update_client_service, 
                                        delete_client_service)


router = APIRouter(prefix='/clients', tags=['Clients'])

@router.post('/create', response_model=ClientOut)
async def create_client(client: ClientCreate,user: User = Depends(get_current_user), db: AsyncSession = Depends(get_session)):
    return await create_client_service(user, client, db)

@router.get('/all',response_model=List[ClientOut])
async def get_all_clients(user: User = Depends(get_current_user), db: AsyncSession = Depends(get_session)):
    return await get_all_clients_service(user, db)

@router.get('/{client_id}', response_model=ClientOut)
async def get_client_by_id(client_id:int ,user: User = Depends(get_current_user), db: AsyncSession = Depends(get_session)):
    return await get_client_by_id_service(user, client_id, db)

@router.put('/{client_id}', response_model=ClientOut)
async def update_client(client: ClientUpdate,client_id:int ,user: User = Depends(get_current_user), db: AsyncSession = Depends(get_session)):
    return await update_client_service(user, client_id, client, db)

@router.delete('/{client_id}', response_model=dict)
async def delete_client(client_id:int ,user: User = Depends(get_current_user), db: AsyncSession = Depends(get_session)):
    return await delete_client_service(client_id, user,db)