from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from app.core.conf import setting
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, declared_attr
from sqlalchemy import func
from typing import Annotated
from datetime import datetime

engine = create_async_engine(setting.DATABASE_URL)

async_session = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session

int_pk = Annotated[int, mapped_column(primary_key=True)]
create_at = Annotated[datetime, mapped_column(server_default=func.now())]
update_at = Annotated[datetime, mapped_column(server_default=func.now(), server_onupdate=func.now())]

class Base(DeclarativeBase):
    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f"{cls.__name__.lower()}"
    
    create_at: Mapped[create_at]
    update_at: Mapped[update_at]
