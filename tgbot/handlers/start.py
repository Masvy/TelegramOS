from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message


start_router: Router = Router()


@start_router.message(CommandStart())
async def start_bot(message: Message):
    ...
