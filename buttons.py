from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup

def main_inline_keyboard(no_volume: bool = False, mp3: bool = False, image: bool = False):

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [

           InlineKeyboardButton(text=f"🎬Выбрать качество", callback_data="quality"),
           InlineKeyboardButton(text=f"{'✔️' if no_volume else '✖'} Без звука", callback_data="no_volume"),

        ],

        [
            InlineKeyboardButton(text=f" {'️✔️' if mp3 else '✖'} Mp3", callback_data='mp3'),
            InlineKeyboardButton(text=f" {'️✔️' if image else '✖️'} Картинка", callback_data='image'),


        ],

        [
            InlineKeyboardButton(text="📥Скачать", callback_data="get")

        ]
    ]
    )
    return keyboard

def quality_inline_keyboard(quality):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[

        [
            InlineKeyboardButton(text=f"{'✔️' if quality == 1080 else '✖️'} 1080p", callback_data="1080p"),
            InlineKeyboardButton(text=f"{'✔️' if quality == 720 else '✖️'} 720p", callback_data="720p"),
            InlineKeyboardButton(text=f"{'✔️' if quality == 360 else '✖️'} 360p", callback_data="360p")

        ],

        [

            InlineKeyboardButton(text=f"🔙Вернуться Назад", callback_data="back")

        ]

    ])
    return keyboard

def url_github():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[

        [
            InlineKeyboardButton(text=f"Перейти на гитхаб создателя", url="https://github.com/tuxarith")
        ]
    ])
    return keyboard
