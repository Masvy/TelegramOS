from database.table import profile_table
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func, select


async def number_registered(session_maker: sessionmaker):
    async with session_maker() as session:
        async with session.begin():
            result = await session.execute(func.count(profile_table.c.user_id))
            users = result.scalar()
            return users


async def count_user_ids(session_maker: sessionmaker):
    async with session_maker() as session:
        async with session.begin():
            result = await session.execute(select(profile_table.c.user_id))
            count_user_ids = [row[0] for row in result.all()]
            return count_user_ids
