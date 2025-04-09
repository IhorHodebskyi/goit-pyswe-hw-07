from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession


async def create_object(session: AsyncSession, model, **kwargs):
    obj = model(**kwargs)
    session.add(obj)
    await session.commit()
    return obj

async def list_objects(session: AsyncSession, model):
    result = await session.execute(select(model))
    return result.scalars().all()

async def update_object(session: AsyncSession, model, obj_id: int, **kwargs):
    obj = await session.get(model, obj_id)
    if obj:
        for key, value in kwargs.items():
            setattr(obj, key, value)
        await session.commit()
        return obj
    return None

async def remove_object(session: AsyncSession, model, obj_id: int):
    obj = await session.get(model, obj_id)
    if obj:
        await session.delete(obj)
        await session.commit()
        return obj
    return None
