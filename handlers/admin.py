from aiogram.types import Message, ReplyKeyboardRemove
from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

from create_bot import db_worker
from keyboards.admin.accept import accept_kb
from keyboards.admin.admin_delete import compile_admin_delete_kb
from keyboards.admin.cakes_names import compile_cakes_names_kb
from keyboards.admin.admin_panel_ru import admin_panel


async def is_admin(admin_id):
    admins = await db_worker.get_admins()
    admins_ids = [i[1] for i in admins]
    return admin_id in admins_ids


class AuthorizationFSM(StatesGroup):
    wait_for_password = State()


# or show admin panel
async def cmd_admin_login(message: Message, state: FSMContext):
    if await is_admin(message.from_user.id):
        await message.answer(f'Я помню Вас, {message.from_user.full_name}, '
                             f'вот панель администратора',
                             reply_markup=admin_panel)  # admin panel kb
        return
    await message.answer("Хм, не могу вспомнить Вас... Введите пожалуйста пароль\U0001F511, чтобы я убедился"
                         "или отмените\u21A9 действие с помощью /cancel или /отмена",
                         reply_markup=ReplyKeyboardRemove())
    await state.set_state(AuthorizationFSM.wait_for_password.state)


async def get_password(message: Message, state: FSMContext):
    admin_password = await db_worker.get_password('admin_password')
    if len(admin_password) != 1:
        await message.answer('Теперь я Вас запомнил, будем знакомы\U0001F44B, новый администратор')
        await db_worker.add_admin(message.from_user.id, f"{message.from_user.full_name}")
        await message.answer('О нет! Кажется пароль\U0001F511 для администраторов не установлен или'
                             ' оказался не действительным',
                             reply_markup=admin_panel)  # admin panel kb
    elif message.text == admin_password[0][1]:
        await message.answer('Теперь я Вас запомнил, будем знакомы, новый администратор',
                             reply_markup=admin_panel)  # admin panel kb)
        await db_worker.add_admin(message.from_user.id, f"{message.from_user.full_name}")
    else:
        await message.answer('Меня не проведешь! Это не тот пароль\U0001F511. '
                             'Вы можете обратиться к администрации, чтобы встать в их ряды!')
    await state.finish()


async def cmd_show_admins(message: Message):
    admins = await db_worker.get_admins()
    for index in range(len(admins)):
        await message.answer(f"админ №{index + 1}: {admins[index][2]}")


# Delete admin FSM
class AdminDeleteFSM(StatesGroup):
    wait_for_choose_person_to_delete = State()


async def cmd_del_admin(message: Message, state: FSMContext):
    if await is_admin(message.from_user.id):
        admin_delete_kb = await compile_admin_delete_kb()
        await message.answer('Кого хотите удалить? '
                             'Вы можете отменить\u21A9 действие с помощью /cancel или /отмена',
                             reply_markup=admin_delete_kb)  # admin's user names
        await state.set_state(AdminDeleteFSM.wait_for_choose_person_to_delete.state)


async def delete_admins(message: Message, state: FSMContext):
    if await is_admin(message.from_user.id):
        admins = await db_worker.get_admins()
        admins_usernames = [i[2] for i in admins]
        admin_for_delete = message.text
        if admin_for_delete == 'всех администраторов':
            for admin_username in admins_usernames:
                await db_worker.del_admin(admin_username)
            await message.answer('Успешно\u2705! все администраторы, включая Вас удалены. '
                                 'Чтобы вернуться в администрацию Вам придется снова ввести пароль\U0001F511',
                                 reply_markup=admin_panel)  # admin panel kb
            await state.finish()
        elif admin_for_delete in admins_usernames:
            await db_worker.del_admin(admin_for_delete)
            await message.answer(f'Успешно\u2705! {admin_for_delete} был удален из администрации. '
                                 f'Чтобы вернуться в администрацию '
                                 f'этому пользователю придется '
                                 f'снова ввести пароль\U0001F511', reply_markup=admin_panel)  # admin panel kb
            await state.finish()
        else:
            await message.answer('Я не знаю такого человека в администрации... '
                                 'Вы можете использовать предоставленные Вам кнопки, '
                                 'чтобы выбрать человека, которого знаете не только Вы, но и я тоже. '
                                 'Или вы можете использовать /отмена или /cancel для возврата\u21A9')


# Update password FSM
class PasswordUpdateFSM(StatesGroup):
    wait_for_new_password = State()


async def cmd_update_admin_password_start(message: Message, state: FSMContext):
    if await is_admin(message.from_user.id):
        await message.answer('Меняем пароль? Напишите в чат новый пароль\U0001F511 '
                             'или отмените\u21A9 действие с помощью /cancel или /отмена',
                             reply_markup=ReplyKeyboardRemove())
        await state.set_state(PasswordUpdateFSM.wait_for_new_password.state)


async def update_admin_password(message: Message, state: FSMContext):
    if await is_admin(message.from_user.id):
        await db_worker.update_password(message.text, 'admin_password')
        await message.answer(f'Успешно\u2705! Новый пароль\U0001F511 теперь - {message.text}',
                             reply_markup=admin_panel)  # admin panel kb
        await state.finish()


async def cmd_show_admin_password(message: Message):
    if await is_admin(message.from_user.id):
        password = await db_worker.get_password('admin_password')
        if len(password) != 1:
            await message.answer('Пароля\U0001F511 не существует. Или он оказался не действительным')
        else:
            await message.answer(f"Вот текущий пароль\U0001F511 - {password[0][1]}",
                                 reply_markup=admin_panel)  # admin panel kb)


# Cake adding FSM
class AddCakeFSM(StatesGroup):
    wait_for_cake_name = State()
    wait_for_cake_text_description = State()
    wait_for_cake_photo = State()
    wait_for_cake_price_per_kg = State()
    wait_for_accept = State()


async def cmd_add_cake(message: Message, state: FSMContext):
    if await is_admin(message.from_user.id):
        await message.answer('Новый торт\U0001F370? Отлично! Введите его название в чат',
                             reply_markup=ReplyKeyboardRemove())
        await state.set_state(AddCakeFSM.wait_for_cake_name.state)


async def get_cake_name(message: Message, state: FSMContext):
    cake_name = message.text
    cakes = await db_worker.get_cakes()
    available_cake_names = [i[1] for i in cakes]
    if cake_name not in available_cake_names:
        await state.update_data(cake_name=cake_name)
        await message.answer('Теперь мне нужно получить текстовое описание торта\U0001F370. '
                             'Это может быть что угодно, например его начинка или цвет')
        await state.set_state(AddCakeFSM.wait_for_cake_text_description.state)
    else:
        await message.answer('Кажется это название уже занято другим тортом\U0001F370. Введите другое имя')


async def get_cake_text_description(message: Message, state: FSMContext):
    cake_text_description = message.text
    await state.update_data(cake_text_description=cake_text_description)
    await message.answer('Отправьте фотографию нового торта\U0001F370')
    await state.set_state(AddCakeFSM.wait_for_cake_photo.state)


async def get_cake_photo(message: Message, state: FSMContext):
    cake_photo_id = message.photo[-1].file_id
    await state.update_data(cake_photo_id=cake_photo_id)
    await message.answer('Последний шаг. Введите цену за килограмм\uFE0F, которая будет отображаться')
    await state.set_state(AddCakeFSM.wait_for_cake_price_per_kg.state)


async def get_cake_price_per_kg(message: Message, state: FSMContext):
    cake_price_per_kg = message.text
    await state.update_data(cake_price_per_kg=cake_price_per_kg)
    # add in db and show result
    data = await state.get_data()
    cake_name = data.get('cake_name', 'not_found')
    cake_text_description = data.get('cake_text_description', 'not_found')
    cake_photo_id = data.get('cake_photo_id', 'not_found')
    cake_price_per_kg = data.get('cake_price_per_kg', 'not_found')
    # await db_worker.add_cake(cake_name, cake_text_description, cake_photo_id, cake_price_per_kg)
    if 'not_found' in [cake_name, cake_text_description, cake_photo_id, cake_price_per_kg]:
        await message.answer('Кажется что-то пошло не так... Попробуйте еще раз',
                             reply_markup=admin_panel)  # admin panel kb
        await state.finish()
        return
    message_caption = (f'Название торта\U0001F370: {cake_name}\n'
                       f'Описание: {cake_text_description}\n'
                       f'Цена за килограмм: {cake_price_per_kg}')
    await message.answer_photo(photo=cake_photo_id, caption=message_caption)
    await message.answer('Вот что будет видеть пользователь об этом торте\U0001F370. '
                         'Оставляем эту карточку торта?',
                         reply_markup=accept_kb)  # y/n
    await state.set_state(AddCakeFSM.wait_for_accept.state)


async def get_accept(message: Message, state: FSMContext):
    if message.text == 'Оставить':
        await message.answer('Красивый торт получился! '
                             'Я добавил его к остальным\u2705, пусть пользователи увидят его\U0001F440',
                             reply_markup=admin_panel)  # admin panel kb
        data = await state.get_data()
        cake_name = data.get('cake_name', 'not_found')
        cake_text_description = data.get('cake_text_description', 'not_found')
        cake_photo_id = data.get('cake_photo_id', 'not_found')
        cake_price_per_kg = data.get('cake_price_per_kg', 'not_found')
        await db_worker.add_cake(cake_name, cake_text_description, cake_photo_id, cake_price_per_kg)
        await state.finish()
    elif message.text == 'Изменить':
        await message.answer('Хорошо, вы можете добавить торт\U0001F370 заново, когда пожелаете',
                             reply_markup=admin_panel)  # admin panel kb
        await state.finish()
    else:
        await message.answer('Вам были выданы кнопки, пожалуйста, используйте их или отмените'
                             '\u21A9 действие, используя\n'
                             '/отмена или /cancel')


# Cake delete FSM
class DeleteCakeFSM(StatesGroup):
    wait_for_cake_name = State()


async def cmd_delete_cake(message: Message, state: FSMContext):
    if await is_admin(message.from_user.id):
        cakes_names_kb = await compile_cakes_names_kb()
        cakes_names = await db_worker.get_cakes()
        if not cakes_names:
            await message.answer('Не могу найти ни одного торта\U0001F370 в своей библиотеке\U0001F4DA. '
                                 'Сначала нужно добавить новый торт\U0001F370')
        else:
            await message.answer('Ладно, давайте удалим 1 торт. '
                                 'Выберите из предложенных варинтов торт\U0001F370, '
                                 'который Вы хотите удалить '
                                 'или отмените\u21A9 действие с помощью /cancel или /отмена',
                                 reply_markup=cakes_names_kb)  # names of cakes
            await state.set_state(DeleteCakeFSM.wait_for_cake_name.state)


async def get_cake_for_delete(message: Message, state: FSMContext):
    cake_name = message.text
    cakes = await db_worker.get_cakes()
    available_cake_names = [i[1] for i in cakes]
    if cake_name in available_cake_names:
        await db_worker.del_cake(cake_name)
        await message.answer(f"{cake_name} был удален", reply_markup=admin_panel)  # admin panel kb
        await state.finish()
    else:
        await message.answer('Вам были выданы кнопки, пожалуйста, используйте их для выбора торта\U0001F370 '
                             'или отмените\u21A9 действие, используя\n'
                             '/отмена или /cancel')


def register_admin_handlers(dp: Dispatcher):
    dp.register_message_handler(cmd_admin_login,
                                commands=['login', 'admin', 'admin_panel',
                                          'логин', 'ввести_пароль', 'администратор', 'ставть_администратором'])
    dp.register_message_handler(get_password,
                                state=AuthorizationFSM.wait_for_password)
    dp.register_message_handler(cmd_show_admins,
                                commands=['show_admins', 'показать_администраторов'])
    dp.register_message_handler(cmd_del_admin,
                                commands=['delete_admin', 'удалить_администратора'])
    dp.register_message_handler(delete_admins, state=AdminDeleteFSM.wait_for_choose_person_to_delete)
    dp.register_message_handler(cmd_update_admin_password_start,
                                commands=['update_password', 'change_password', 'обновить_пароль', 'поменять_пароль'])
    dp.register_message_handler(update_admin_password,
                                state=PasswordUpdateFSM.wait_for_new_password)
    dp.register_message_handler(cmd_show_admin_password,
                                commands=['show_password', 'показать_пароль'])
    dp.register_message_handler(cmd_add_cake,
                                commands=['add_cake', 'добавить_торт'])
    dp.register_message_handler(get_cake_name,
                                state=AddCakeFSM.wait_for_cake_name)
    dp.register_message_handler(get_cake_text_description,
                                state=AddCakeFSM.wait_for_cake_text_description)
    dp.register_message_handler(get_cake_photo,
                                state=AddCakeFSM.wait_for_cake_photo,
                                content_types=['photo'])
    dp.register_message_handler(get_cake_price_per_kg,
                                state=AddCakeFSM.wait_for_cake_price_per_kg)
    dp.register_message_handler(get_accept,
                                state=AddCakeFSM.wait_for_accept)
    dp.register_message_handler(cmd_delete_cake,
                                commands=['delete_cake', 'удалить_торт'])
    dp.register_message_handler(get_cake_for_delete,
                                state=DeleteCakeFSM.wait_for_cake_name)
