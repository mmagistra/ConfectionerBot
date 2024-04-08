from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from create_bot import db_worker


async def compile_admin_delete_kb():
    admin_delete_kb = ReplyKeyboardMarkup(resize_keyboard=True)

    all_btn = ['всех администраторов']

    admins = await db_worker.get_admins()
    admins_usernames = [i[2] for i in admins]

    buttons_names = admins_usernames + all_btn

    for i in range((len(buttons_names) // 3) + 1):
        if len(buttons_names)-i*3 > 0:
            cur_btns = []
            for j in range(min(3, len(buttons_names)-i*3)):
                cur_btns.append(KeyboardButton(buttons_names[i*3+j]))
            admin_delete_kb.row(*cur_btns)

    return admin_delete_kb
