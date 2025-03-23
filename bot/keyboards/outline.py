from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

phone_number = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="📞 Raqamni yuborish", request_contact=True)
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)





