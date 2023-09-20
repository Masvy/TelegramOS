import logging
import asyncio

from environs import Env
import betterlogging as bl
from aiogram import Bot, Dispatcher

from handlers import routers_list


class ErrorFilter(logging.Filter):
    def filter(self, record):
        return record.levelno == logging.ERROR


def setup_logging():
    '''Функция конфигурации логирования'''
    log_level = logging.INFO
    bl.basic_colorized_config(level=log_level)

    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname)-8s'
               ' [%(asctime)s] - %(name)s - %(message)s',
    )
    logger = logging.getLogger(__name__)
    logger.info('Starting bot')


async def main():
    '''
    Функция конфигурирования и запуска бота

    Создал объекты бота и диспетчера
    Зарегистрировал роутеры в диспетчере
    Создал url для соединения с базой
    Пропускаем накопившиеся апдейты и запускаем polling
    '''
    setup_logging()

    env = Env()
    env.read_env()

    bot: Bot = Bot(token=env('BOT_TOKEN'),
                   parse_mode='HTML')
    dp: Dispatcher = Dispatcher()

    # await set_main_menu(bot)

    dp.include_routers(*routers_list)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.error('Stopping bot')
