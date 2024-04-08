from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from create_bot import db_worker


async def compile_cakes_names_kb():
    cakes_names_kb = ReplyKeyboardMarkup(resize_keyboard=True)
    all_btn = ['all admins']

    cakes = await db_worker.get_cakes()
    cakes_names = [i[1] for i in cakes]

    for i in range((len(cakes_names) // 3) + 1):
        if len(cakes_names) - i * 3 > 0:
            cur_btns = []
            for j in range(min(3, len(cakes_names) - i * 3)):
                cur_btns.append(KeyboardButton(cakes_names[i * 3 + j]))
            cakes_names_kb.row(*cur_btns)

    return cakes_names_kb
