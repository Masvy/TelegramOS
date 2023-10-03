import asyncio

from environs import Env
from aiogram import Router, F
from sqlalchemy.orm import sessionmaker
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, and_f, StateFilter

from filters.admin_filters import IsAdmin
from states.admin_states import InputNews
from keyboards.inline_admib import admin_kb
from database.users import number_registered, count_user_ids

admin_router: Router = Router()

env = Env()
env.read_env()


@admin_router.message(and_f(CommandStart(), IsAdmin(env('ADMIN_IDS'))))
async def start_bot_admin(message: Message):
    await message.answer('Choose an action:',
                         reply_markup=admin_kb)


@admin_router.callback_query(F.data == 'mailing_list_pressed',
                             StateFilter(default_state))
async def request_mailing(callback: CallbackQuery,
                          state: FSMContext):
    await callback.message.answer('Submit content')
    await state.set_state(InputNews.news)


@admin_router.message(StateFilter(InputNews.news))
async def input_news(message: Message, state: FSMContext,
                     session_maker: sessionmaker):
    '''
    Хэндлер срабатывает на введение контента.

    Начинает рассылку по пользователям.
    '''
    await state.update_data(news=message.text)
    count_user_ids_ = await count_user_ids(session_maker=session_maker)
    await state.clear()
    users = 0
    for count_user_id in count_user_ids_:
        try:
            await message.copy_to(count_user_id)
            users += 1
        except Exception:
            pass
        await asyncio.sleep(0.1)
    await message.answer('Рассылка завершена. Пользователи, '
                         f'которым пришла рассылка: {users}')


@admin_router.callback_query(F.data == 'statistics_pressed')
async def show_statistics(callback: CallbackQuery,
                          session_maker: sessionmaker):
    registered = await number_registered(session_maker=session_maker)
    await callback.message.answer(f'Registered: {registered}')
