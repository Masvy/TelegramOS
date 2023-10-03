from aiogram.fsm.state import State, StatesGroup


# Создал класс для группы состояний
class InputNews(StatesGroup):
    news = State()
