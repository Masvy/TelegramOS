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


async def show_user_ids(session_maker: sessionmaker):
    async with session_maker() as session:
        async with session.begin():
            result = await session.execute(select(profile_table.c.user_id))
            user_ids = [row[0] for row in result]
            return user_ids


async def show_first_names(session_maker: sessionmaker):
    async with session_maker() as session:
        async with session.begin():
            result = await session.execute(select(profile_table.c.name))
            first_names = [row[0] for row in result]
            return first_names


async def show_user_names(session_maker: sessionmaker):
    async with session_maker() as session:
        async with session.begin():
            result = await session.execute(select(profile_table.c.user_name))
            user_names = [row[0] for row in result]
            return user_names


async def show_registration_date(session_maker: sessionmaker):
    async with session_maker() as session:
        async with session.begin():
            result = await session.execute(select(profile_table.c.registration_date))
            registration_date = [row[0] for row in result]
            return registration_date
