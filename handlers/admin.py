from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup


class AddNewInstitute(StatesGroup):
    waiting_for_photo = State()
    waiting_for_name_of_institute = State()
    waiting_for_name_of_direction = State()
    waiting_for_passing_score = State()
    waiting_for_count_of_budget_places = State()
    waiting_for_description = State()


async def add_new_institute_start(message: types.Message):
    await message.answer('Send photo of institute')
    await AddNewInstitute.waiting_for_photo.set()


async def institute_add_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.photo[0].file_id
    await AddNewInstitute.next()
    await message.answer('Awesome! Now send name of institute')


async def institute_add_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name_of_institute'] = message.text
    await AddNewInstitute.next()
    await message.answer('Awesome! Now send name of direction')


async def institute_add_name_of_direction(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name_of_direction'] = message.text
    await AddNewInstitute.next()
    await message.answer('Awesome! Now send passing score')


async def institute_add_passing_score(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['passing_score'] = message.text
    await AddNewInstitute.next()
    await message.answer('Awesome! Now send count of budget places')


async def institute_add_count_of_budget_places(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['count_of_budget_places'] = message.text
    await AddNewInstitute.next()
    await message.answer('Awesome! Now add some description')


async def institute_add_description(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['description'] = message.text
    await message.answer('We add your institute')
    # analizetion data
    await message.answer('analysis...')
    async with state.proxy() as data:
        await message.answer(str(data))
    await state.finish()


async def admin_command(message: types.Message):
    await message.bot.send_message(message.from_user.id, 'is an admin command')
    await message.delete()


async def cancel_command(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer('canceled', reply_markup=types.ReplyKeyboardMarkup())


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(admin_command, commands=['admin'])
    dp.register_message_handler(add_new_institute_start, commands=['add'])
    dp.register_message_handler(cancel_command, state='*', commands=['cancel', 'отмена'])
    dp.register_message_handler(institute_add_photo,
                                state=AddNewInstitute.waiting_for_photo, content_types=['photo'])
    dp.register_message_handler(institute_add_name,
                                state=AddNewInstitute.waiting_for_name_of_institute)
    dp.register_message_handler(institute_add_name_of_direction,
                                state=AddNewInstitute.waiting_for_name_of_direction)
    dp.register_message_handler(institute_add_passing_score,
                                state=AddNewInstitute.waiting_for_passing_score)
    dp.register_message_handler(institute_add_count_of_budget_places,
                                state=AddNewInstitute.waiting_for_count_of_budget_places)
    dp.register_message_handler(institute_add_description,
                                state=AddNewInstitute.waiting_for_description)
