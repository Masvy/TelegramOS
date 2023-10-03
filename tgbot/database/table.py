from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, BigInteger, String, func, Date, Table

BaseModel = declarative_base()

profile_table = Table(
    'account_profile',
    BaseModel.metadata,
    Column('id', BigInteger, primary_key=True),
    Column('user_id', BigInteger, nullable=False),
    Column('name', String(64), nullable=True),
    Column('user_name', String(32), nullable=True),
    Column('registration_date', Date, server_default=func.now())
)
