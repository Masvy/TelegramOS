from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# Создал объект клавиатуры
admin_kb: InlineKeyboardMarkup = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Mailing list',
                                 callback_data='mailing_list_pressed')
        ],
        [
            InlineKeyboardButton(text='Statstics',
                                 callback_data='statistics_pressed')
        ],
        [
            InlineKeyboardButton(text='View database',
                                 callback_data='view_database_pressed')
        ]
    ]
)
