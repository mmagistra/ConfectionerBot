from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram import Dispatcher
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext

from create_bot import db_worker
from keyboards.client.cakes_names import compile_cakes_names_kb
from keyboards.client.request_contact import request_contact_kb
from keyboards.client.shipping import shipping_kb
from keyboards.client.start import start_kb
from keyboards.client.weight import weight_kb
from keyboards.client.confirm_weight import confirm_weight_kb
from keyboards.client.description_type import description_type_kb
from keyboards.client.package import package_kb


# цена не точная, доставка по называйску и прил. деревням,


class OrderFSM(StatesGroup):
    wait_for_cake_name = State()  # 1
    wait_for_cake_weight = State()  # 2
    wait_for_confirm_weight = State()  # 3
    wait_for_description_type = State()  # 4

    wait_for_text_description = State()  # 5.1
    wait_for_image_description = State()  # 5.2
    wait_for_image_with_text_description = State()  # 5.3

    wait_for_package_type = State()  # 6
    wait_for_shipping_type = State()  # 7
    # wait_for_person_name = State()
    wait_for_person_contact = State()  # отправляется с помощью message.bot.send_contact в коце FSM # 8


async def cmd_start(message: Message, state: FSMContext):
    await state.finish()
    await cmd_info(message, state)
    await message.answer('Выберите, что бы вы хотели сделать.',
                         parse_mode='HTML', reply_markup=start_kb)


async def cmd_info(message: Message, state: FSMContext):
    await state.finish()
    # info about cakes
    number = '7(000)000-00-00'
    text = (f'Здравствуйте\U0001F44B! Бот\U0001F916 '
            f'предоставляет возможность заказа тортов через телеграмм. '
            f'Для Вас мы можем предложить следующие торты\U0001F370:\n\n')
    # Подгрузка из бд await message.answer
    text += (f'\u2757\u2757\u2757<b>ВНИМАНИЕ</b>\u2757\u2757\u2757'
             f'\n - Доставка\U0001F4EC осуществляется только по городу Тюмень и'
             f' прилежащим к нему деревням.\n '
             f'- При выпечке торта\U0001F370 цена может меняться в зависимости от РЕАЛЬНОГО веса торта\n.'
             f'- После заказа торта с Вами '
             f'свяжутся для стоимости доставки.\n\n'
             f'<u>По всем интерисующим Вас вопросам можно связаться по номеру {number}</u>\n\n'
             f'Для отмены\u21A9 какого-либо действия используйте -\n'
             f'<u>/cancel</u> или <u>/отмена</u>. ')
    await message.answer(text, parse_mode='HTML')


async def cmd_show_cakes(message: Message):
    cakes = await db_worker.get_cakes()
    if not cakes:
        await message.answer('На данный момент в ассортименте нет тортов')
    else:
        for cake in cakes:
            cake_name = cake[1]
            description = cake[2]
            photo = cake[3]
            price_per_kg = cake[4]
            message_caption = (f'Название торта\U0001F370: {cake_name}\n'
                            f'Описание: {description}\n'
                            f'Цена за килограмм: {price_per_kg}')
            await message.answer_photo(photo=photo, caption=message_caption)


async def cmd_cancel(message: Message, state: FSMContext):
    await state.finish()
    await message.answer(f'Действие отменено. Может попробуем еще раз?\U0001F605',
                         reply_markup=start_kb)


# FSM
async def cmd_order(message: Message, state: FSMContext):
    # Запуск FSM
    cakes = await db_worker.get_cakes()
    if len(cakes) == 0:
        await message.answer('Кажется сейчас в ассортименте нет тортов')
        return
    cakes_names_kb = await compile_cakes_names_kb()
    await message.answer('Отлично! Выберите торт\U0001F370 из возможных.', reply_markup=cakes_names_kb)  # Загрузка и бд
    await state.set_state(OrderFSM.wait_for_cake_name.state)


async def get_cake_name(message: Message, state: FSMContext):
    cakes = await db_worker.get_cakes()
    available_cake_names = [cake[1] for cake in cakes]
    cake_name = message.text
    if cake_name.lower() in available_cake_names:
        await state.update_data(cake_name=cake_name)
        await state.set_state(OrderFSM.wait_for_cake_weight.state)
        await message.answer(f'Отличный выбор\u2705! Теперь выберите желаемый вес\uFE0F. Вы '
                             f'можете выбрать его с помощью предложенных '
                             f'\u2B07\u2B07\u2B07кнопок\u2B07\u2B07\u2B07 '
                             f'или написать сами. Учтите, что в '
                             f'процессе выпечки торта\U0001F370 вес может немного измениться, что '
                             f'также повлияет и на цену.', reply_markup=weight_kb)  # 1 2 3 4 5
    else:
        await message.answer('Хм... Я вас не понимаю :( Пожалуйста, используйте предложенные вам кнопки')


async def get_cake_weight(message: Message, state: FSMContext):
    try:
        msg = [i for i in message.text.split() if i.isdigit()]
        cake_weight = str(''.join(msg))
        if cake_weight == '':
            cake_weight = '0'
        await state.update_data(cake_weight=cake_weight)
        await state.set_state(OrderFSM.wait_for_confirm_weight.state)
        await message.answer(f'Подтвердите\u2705 ваши действия. Вы выбрали '
                             f'- {cake_weight} кг?', reply_markup=confirm_weight_kb)  # yes or no
    except:
        await message.answer('Пожалуйста, напишите желаемый вес торта в виде <<X кг>>, '
                             'где X - количество киллограмм, или выберите его на '
                             '\u2B07\u2B07\u2B07клавиатуре\u2B07\u2B07\u2B07.')


async def get_confirm_cake_weight(message: Message, state: FSMContext):
    if 'да, ' in message.text.lower():
        await state.set_state(OrderFSM.wait_for_description_type.state)
        await message.answer('Записано\u270F\U0001F4C3. '
                             'Далее по списку - пожелания по внешнему виду торта\U0001F370. '
                             'При желании Вы можете добавить к заказу описание внешнего вида будущего торта.',
                             reply_markup=description_type_kb)  # image / text / ...
    elif 'нет, ' in message.text.lower():
        await state.update_data(cake_weight='0')
        await state.set_state(OrderFSM.wait_for_cake_weight.state)
        await message.answer('Тогда давайте попробуем еще раз.'
                             'пожалуйста, используйте предложенные вам '
                             '\u2B07\u2B07\u2B07кнопки\u2B07\u2B07\u2B07 '
                             'или напишите желаемый вес торта\U0001F370 в виде <<X кг>>, '
                             'где X - количество киллограмм.', reply_markup=weight_kb)  # 1 2 3 4 5
    else:
        await message.answer('Я вас не понимаю, пожалуйста, используйте предложенные вам '
                             '\u2B07\u2B07\u2B07кнопки\u2B07\u2B07\u2B07.')


async def get_description_type(message: Message, state: FSMContext):
    description_type = message.text
    if description_type.lower() == 'добавить только изображение':
        await state.set_state(OrderFSM.wait_for_image_description.state)
        await message.answer('Отправьте картинку',
                             reply_markup=ReplyKeyboardRemove())
    elif description_type.lower() == 'добавить только текст':
        await state.set_state(OrderFSM.wait_for_text_description.state)
        await message.answer('Введите описание желаемого торта\U0001F370 в текстовом виде',
                             reply_markup=ReplyKeyboardRemove())
    elif description_type.lower() == 'добавить изображение и текст':
        await state.set_state(OrderFSM.wait_for_image_with_text_description.state)
        await message.answer('Отправьте картинку, а затем отправьте текстовое описание торта',
                             reply_markup=ReplyKeyboardRemove())
    elif description_type.lower() == 'не добавлять пожелания':
        await state.set_state(OrderFSM.wait_for_package_type.state)
        await message.answer('Идем дальше\u2705. Хотите ли Вы упаковку к своему торту\U0001F370?',
                             reply_markup=package_kb)
    else:
        await message.answer('Я Вас не понимаю, пожалуйста, используйте предложенные Вам '
                             '\u2B07\u2B07\u2B07кнопки\u2B07\u2B07\u2B07')


async def get_image_description(message: Message, state: FSMContext):
    image_id = message.photo[-1].file_id
    await state.update_data(image_id=image_id)
    await state.set_state(OrderFSM.wait_for_package_type.state)
    await message.answer('Идем дальше\u2705. Хотите ли Вы упаковку к своему торту\U0001F370?(+150 рублей к общей '
                         'стоимости заказа)',
                         reply_markup=package_kb)  # y/n


async def get_text_description(message: Message, state: FSMContext):
    text = message.text
    await state.update_data(text=text)
    await state.set_state(OrderFSM.wait_for_package_type.state)
    await message.answer('Идем дальше\u2705. Хотите ли Вы упаковку к своему торту\U0001F370?(+150 рублей к общей '
                         'стоимости заказа)',
                         reply_markup=package_kb)  # y/n


async def get_image_with_text_description(message: Message, state: FSMContext):
    text = message.text
    data = await state.get_data()
    if data.get('image_id', '-') == '-':
        try:
            image_id = message.photo[-1].file_id
            await state.update_data(image_id=image_id)
        except:
            await message.answer('Видимо Вы еще не добавили фотографию, поэтому мы не можем продолжить')
            return
    if text is not None:
        await state.update_data(text=text)
    else:
        await message.answer('Теперь, пожалуйста, добавьте текстовое описание торта')
        return
    await state.set_state(OrderFSM.wait_for_package_type.state)
    await message.answer('Идем дальше\u2705. Хотите ли Вы упаковку к своему торту\U0001F370? (+150 рублей к общей '
                         'стоимости заказа)',
                         reply_markup=package_kb)  # y/n


async def get_package_type(message: Message, state: FSMContext):
    if message.text.lower() == 'хочу':
        package_type = message.text.lower()
        await state.update_data(package_type='нужна')
        await state.set_state(OrderFSM.wait_for_shipping_type.state)
        await message.answer('Почти закончили\u2705. Давайте определимся с доставкой.'
                             'Выберите предпочтительный для Вас способ. На счет доставки с Вами свяжутся, как только '
                             'торт будет готов', reply_markup=shipping_kb)
    elif message.text.lower() == 'спасибо, не нужна':
        package_type = message.text.lower()
        await state.update_data(package_type='не нужна')
        await state.set_state(OrderFSM.wait_for_shipping_type.state)
        await message.answer('Почти закончили\u2705. Давайте определимся с доставкой. '
                             'Выберите предпочтительный для Вас способ. На счет доставки с Вами свяжутся, как только '
                             'торт будет готов', reply_markup=shipping_kb)
    else:
        await message.answer('Просьба использовать \u2B07\u2B07\u2B07кнопки\u2B07\u2B07\u2B07, предложенные вам')


async def get_shipping_type(message: Message, state: FSMContext):
    if message.text.lower() == 'доставка на дом':
        shipping_type = 'на дом'  # по тарифам такси(в инфе) АРДЕС ПРИДУМАТЬ!
        await state.update_data(shipping_type=shipping_type)
        await state.set_state(OrderFSM.wait_for_person_contact.state)
        await message.answer('Последний пункт\u2705. Для связи с Вами будет использован телеграм. Предоставьте, '
                             'пожалуйста свой номер, нажав на \u2B07\u2B07\u2B07кнопку\u2B07\u2B07\u2B07',
                             reply_markup=request_contact_kb)  # request contact
    elif message.text.lower() == 'самовывоз':
        shipping_type = 'самовывоз'
        await state.update_data(shipping_type=shipping_type)
        await state.set_state(OrderFSM.wait_for_person_contact.state)
        await message.answer('Последний пункт\u2705. Для связи с Вами будет использован телеграм. Предоставьте, '
                             'пожалуйста свой номер, нажав на \u2B07\u2B07\u2B07кнопку\u2B07\u2B07\u2B07',
                             reply_markup=request_contact_kb)  # request contact
    else:
        await message.answer('Возможно я забыл сказать - используйте '
                             '\u2B07\u2B07\u2B07кнопки\u2B07\u2B07\u2B07, предоставленные Вам')


async def get_person_contact(message: Message, state: FSMContext):
    await message.answer('Номер получен\u2705. Ваш заказ отправлен администратору. Ожидайте дальнейшей информации. '
                         'Позже с Вами свяжутся\U0001F4F2 для уточнения некоторых вопросов', reply_markup=ReplyKeyboardRemove())
    number = message.contact.phone_number
    first_name = message.contact.first_name
    # person_name = message.contact.full_name
    await state.update_data(number=number, first_name=first_name)
    data = await state.get_data()
    message_text = f'<b>Новый заказ!</b>\n\n' \
                   f'' \
                   f'Заказанный торт: {data.get("cake_name", "Not founded")}\n' \
                   f'Вес: {data.get("cake_weight", "Not founded")} кг\n'

    description_text = f'Описание торта: ' + data.get('text', '')
    if description_text != f'Описание торта: ':
        message_text += description_text + '\n'

    message_text += f'Упаковка: {data.get("package_type", "Not founded")}\n' \
                    f'Тип доставки: {data.get("shipping_type", "Not founded")}\n\n'  # +Примерная стоимость!

    admins = await db_worker.get_admins()
    admins_ids = [admin[1] for admin in admins]

    for admin_id in admins_ids:
        await message.bot.send_message(admin_id, message_text, parse_mode='HTML')
        image_id = data.get('image_id', '')
        if image_id != '':
            await message.bot.send_photo(admin_id, image_id)
        await message.bot.send_contact(message.from_user.id,
                                       phone_number=data.get('number'), first_name=data.get('first_name'))

    # await message.answer(message_text, parse_mode='HTML')
    # image_id = data.get('image_id', '')
    # if image_id != '':
    #     await message.bot.send_photo(message.from_user.id, image_id)
    # await message.bot.send_contact(message.from_user.id,
    #                                phone_number=data.get('number'), first_name=data.get('first_name'))
    await message.answer('Что дальше?', reply_markup=start_kb)
    await state.finish()


async def cmd_test(message: Message):
    await message.answer('\u270F\U0001F4C3')


async def get_contact(message: Message):
    await message.answer(f'u do this!, {message.contact.full_name, message.contact.phone_number}',
                         reply_markup=ReplyKeyboardRemove())


def register_client_handlers(dp: Dispatcher):
    dp.register_message_handler(cmd_test, commands=['test'])
    # dp.register_message_handler(get_contact, content_types='contact')
    dp.register_message_handler(cmd_start, commands=['start', 'help'], state='*')
    dp.register_message_handler(cmd_info, commands=['info', 'информация', 'Информация'])
    dp.register_message_handler(cmd_show_cakes, commands=['show_cakes', 'показать_торты'])
    dp.register_message_handler(cmd_cancel, commands=['cancel', 'отмена', 'Отмена'], state='*')
    dp.register_message_handler(cmd_order, commands=['order', 'заказать', 'Заказать'], state='*')
    # FSM
    dp.register_message_handler(get_cake_name, state=OrderFSM.wait_for_cake_name)
    dp.register_message_handler(get_cake_weight, state=OrderFSM.wait_for_cake_weight)
    dp.register_message_handler(get_confirm_cake_weight, state=OrderFSM.wait_for_confirm_weight)
    dp.register_message_handler(get_description_type, state=OrderFSM.wait_for_description_type)
    # 1 of 3 will work
    dp.register_message_handler(get_text_description, state=OrderFSM.wait_for_text_description)
    dp.register_message_handler(get_image_description, state=OrderFSM.wait_for_image_description,
                                content_types=['photo'])
    dp.register_message_handler(get_image_with_text_description, state=OrderFSM.wait_for_image_with_text_description,
                                content_types=['photo', 'text'])
    # next is standart
    dp.register_message_handler(get_package_type, state=OrderFSM.wait_for_package_type)
    dp.register_message_handler(get_shipping_type, state=OrderFSM.wait_for_shipping_type)
    dp.register_message_handler(get_person_contact, state=OrderFSM.wait_for_person_contact,
                                content_types='contact')
    # FSM end
