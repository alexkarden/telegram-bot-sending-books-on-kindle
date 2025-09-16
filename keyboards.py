from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Моя почта Kindle")],
    ],
    resize_keyboard=True,
)
