from aiogram.types import (
    BotCommand,
    ReplyKeyboardMarkup, KeyboardButton
)

BOT_COMMANDS = [
    BotCommand(command="catalog", description="📚 Каталог товаров"),
    BotCommand(command="sale",    description="🔥 Акции и скидки"),
]

main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [ 
            KeyboardButton(text="Каталог"),
            KeyboardButton(text="Акции"),
        ],
        [
            KeyboardButton(text="Наш канал"),
        ],
        [KeyboardButton(text="Задать вопрос")]
    ],
    resize_keyboard=True,
    input_field_placeholder="Выберите действие",
)
