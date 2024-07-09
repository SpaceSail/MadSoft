from typing import Any
from database import new_session, MemORM
from sqlalchemy import select, delete, update
from schemas import MemAdd


# representation of main actions with database object
class MemStorage:
    # adding pic name to db
    @classmethod
    async def add_mem(cls, data: MemAdd) -> Any:
        async with new_session() as session:
            data = data.model_dump()

            mem = MemORM(**data)
            session.add(mem)
            await session.flush()
            await session.commit()
            return mem.id

    # updating existed string
    @classmethod
    async def update_mem(cls, id: int, name: str) -> Any:
        async with (new_session() as session):
            query = update(MemORM).where(MemORM.id == id)\
                .values(name=name)
            await session.execute(query)
            await session.flush()
            await session.commit()
            return

    # return all data added
    @classmethod
    async def get_mem_all(cls) -> list:
        async with new_session() as session:
            query = select(MemORM)
            result = await session.execute(query)
            mem_models = result.scalars().all()
            return mem_models

    # checking if file already exists in db
    @classmethod
    async def check_mem(cls, name: str):
        async with new_session() as session:
            query = select(MemORM.name).where(MemORM.name == name)
            result = await session.execute(query)
            mem_models = result.scalars().all()
            if mem_models:
                return True
        return False
    # getting an exact pic name
    @classmethod
    async def get_mem(cls, id: int) -> str:
        async with new_session() as session:
            query = select(MemORM.name).where(MemORM.id == id)
            result = await session.execute(query)
            mem_models = result.scalars().first()
            return mem_models
    # deleting record from db
    @classmethod
    async def delete_mem(cls, id: int) -> None:
        async with new_session() as session:
            query = delete(MemORM).where(MemORM.id == id)
            await session.execute(query)
            await session.commit()
            return

