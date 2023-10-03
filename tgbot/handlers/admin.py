import os
import asyncio

from environs import Env
from aiogram import Router, F, Bot
from sqlalchemy.orm import sessionmaker
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.filters import CommandStart, and_f, StateFilter
from aiogram.types import Message, CallbackQuery, FSInputFile

from filters.admin_filters import IsAdmin
from states.admin_states import InputNews
from utils.excel_file import generate_excel_file
from keyboards.inline_admib import admin_kb
from database.users import number_registered, count_user_ids, show_user_ids, \
    show_first_names, show_user_names, \
    show_registration_date

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


@admin_router.callback_query(F.data == 'view_database_pressed')
async def show_users(callback: CallbackQuery,
                     session_maker: sessionmaker,
                     bot: Bot):
    show_user_ids_ = await show_user_ids(session_maker=session_maker)
    show_first_names_ = await show_first_names(session_maker=session_maker)
    show_user_names_ = await show_user_names(session_maker=session_maker)
    show_registration_date_ = await show_registration_date(session_maker=session_maker)
    excel_file = await generate_excel_file(show_user_ids_, show_first_names_,
                                           show_user_names_, show_registration_date_)

    temp_file_path = "temp_user_database.xlsx"
    with open(temp_file_path, "wb") as temp_file:
        temp_file.write(excel_file.read())

    await bot.send_document(callback.from_user.id,
                            document=FSInputFile(temp_file_path))
    os.remove(temp_file_path)
