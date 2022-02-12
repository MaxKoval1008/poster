from aiogram.dispatcher import FSMContext
from bot import dp
from aiogram import types
import keyboards as kb
from data_base import UsersBase
from states import PostersForm as poster
from states import AdminPassword, ShowPoster, ChangePoster
from .admin_settings import is_admin

db = UsersBase('data_base/posters.db')
admin = []


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply(f"Привет!", reply_markup=kb.markup_main)


@dp.message_handler(commands=['is_admin'])
async def process_start_command(message: types.Message):
    await message.answer(f"Для доступа в кабинет администратора нажмите кнопку и введите пароль",
                         reply_markup=kb.markup_is_admin)


@dp.callback_query_handler(lambda c: c.data == 'admin_keyboard')
async def process_callback_button1(callback_query: types.CallbackQuery):
    await callback_query.message.answer("Введите пароль:")
    await AdminPassword.Password.set()


@dp.message_handler(state=AdminPassword.Password)
async def process_start_command(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['Password'] = message.text
    data = await state.get_data()
    if is_admin(list(data.values())[0]):
        await message.answer('Добро пожаловать в кабинет администратора!', reply_markup=kb.markup_admin_keyboard)
        if message.from_user.id not in admin:
            admin.append(message.from_user.id)
    else:
        await message.answer('Неправильный пароль.')
    await state.finish()


@dp.message_handler(text='Выйти')
async def get_text_messages(message: types.Message):
    if message.from_user.id in admin:
        admin.remove(message.from_user.id)
        await message.answer('Выход', reply_markup=kb.markup_main)
    else:
        await message.answer('Отказано в доступе')


@dp.message_handler(text=['Объявления'])
async def process_start_command(message: types.Message):
    if message.from_user.id in admin:
        all_announcements = db.all_announcements()
        for i in all_announcements:
            text = f'''\n
                    ID: {i[0]}\n
                    Город: {i[1]}\n
                    Тип мероприятия: {i[2]}\n
                    Название: {i[3]}
                    Описание: {i[4]}\n
                    Место проведения: {i[5]}\n
                    Дата и время: {i[6]}\n
                    Стоимость: {i[7]}\n
                    Телефон: {i[8]} \n
                    Подтверждение: {i[9]}\n'''
            await message.answer(text)
        await message.answer('Выберите кнопку ниже', reply_markup=kb.markup_admin_change_ann)
    else:
        await message.answer('Отказано в доступе')


@dp.callback_query_handler(lambda c: c.data in ['markup_admin_activate_ann', 'more_ann'])
async def process_callback_button1(callback_query: types.CallbackQuery):
    text_value = db.disapproved_user_announcement()
    try:
        text = f'''\nID: {text_value[0][0]}
        Горд: {text_value[0][1]}
        Тип мероприятия: {text_value[0][2]}
        Название: {text_value[0][3]}
        Описание: {text_value[0][4]}
        Место проведения: {text_value[0][5]}
        Дата и время: {text_value[0][6]}
        Стоимость: {text_value[0][7]}
        Телефон: {text_value[0][8]}
        Подтверждение: {text_value[0][9]}'''
        await callback_query.message.answer(text, reply_markup=kb.markup_change_mode_ann)
    except IndexError:
        await callback_query.message.answer('Все объявления подтверждены.')


@dp.callback_query_handler(lambda c: c.data == 'markup_admin_change_ann')
async def process_callback_button1(callback_query: types.CallbackQuery):
    all_announcements = db.all_announcements()
    try:
        for i in all_announcements:
            text = f'''\n
                            ID: {i[0]}\n
                            Город: {i[1]}\n
                            Тип мероприятия: {i[2]}\n
                            Название: {i[3]}
                            Описание: {i[4]}\n
                            Место проведения: {i[5]}\n
                            Дата и время: {i[6]}\n
                            Стоимость: {i[7]}\n
                            Телефон: {i[8]} \n
                            Подтверждение: {i[9]}\n'''
            await callback_query.message.answer(text)
        await callback_query.message.answer('Введите ID объявления, которое хотели бы изменить')
        await ChangePoster.IdData.set()
    except IndexError:
        await callback_query.message.answer('Нет доступных объявлений.')


@dp.message_handler(state=ChangePoster.IdData)
async def process_start_command(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['IdData'] = message.text
    poster = db.one_announcement(message.text)
    text = f'''\n
                        №1 ID: {poster[0]}\n
                        №2 Город: {poster[1]}\n
                        №3 Тип мероприятия: {poster[2]}\n
                        №4 Название: {poster[3]}
                        №5 Описание: {poster[4]}\n
                        №6 Место проведения: {poster[5]}\n
                        №7 Дата и время: {poster[6]}\n
                        №8 Стоимость: {poster[7]}\n
                        №9 Телефон: {poster[8]} \n
                        №10 Подтверждение: {poster[9]}\n'''
    await message.answer(text)
    await message.answer('Укажите номер поля которое вы хотели бы изменить'
                                        ' и желаемое значение через пробел.')
    await ChangePoster.ChangeData.set()


@dp.message_handler(state=ChangePoster.ChangeData)
async def process_start_command(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['ChangeData'] = message.text
    data = await state.get_data()
    if list(data.values())[1][0] == '1':
        db.update_announcement(list(data.values())[0], 'id', list(data.values())[1][2:])
    if list(data.values())[1][0] == '2':
        db.update_announcement(list(data.values())[0], 'town', list(data.values())[1][2:])
    if list(data.values())[1][0] == '3':
        db.update_announcement(list(data.values())[0], 'type', list(data.values())[1][2:])
    if list(data.values())[1][0] == '4':
        db.update_announcement(list(data.values())[0], 'title', list(data.values())[1][2:])
    if list(data.values())[1][0] == '5':
        db.update_announcement(list(data.values())[0], 'description', list(data.values())[1][2:])
    if list(data.values())[1][0] == '6':
        db.update_announcement(list(data.values())[0], 'place', list(data.values())[1][2:])
    if list(data.values())[1][0] == '7':
        db.update_announcement(list(data.values())[0], 'date_time', list(data.values())[1][2:])
    if list(data.values())[1][0] == '8':
        db.update_announcement(list(data.values())[0], 'cost', list(data.values())[1][2:])
    if list(data.values())[1][0] == '9':
        db.update_announcement(list(data.values())[0], 'telephone', list(data.values())[1][2:])
    if list(data.values())[1][0] == '10':
        db.update_announcement(list(data.values())[0], 'approved', list(data.values())[1][2:])
    await state.finish()


@dp.callback_query_handler(lambda c: c.data == 'approve_ann')
async def process_callback_button1(callback_query: types.CallbackQuery):
    disapproved_user_announcement = db.disapproved_user_announcement()
    try:
        id = disapproved_user_announcement[0][0]
        db.approving_announcement(id)
        await callback_query.message.answer('Объявление подтверждено', reply_markup=kb.markup_more_ann)
    except IndexError:
        await callback_query.message.answer('Все объявления подтверждены.')


@dp.callback_query_handler(lambda c: c.data == 'disapprove_ann')
async def process_callback_button1(callback_query: types.CallbackQuery):
    disapproved_user_announcement = db.disapproved_user_announcement()
    try:
        id = disapproved_user_announcement[0][0]
        db.disapproving_announcement(id)
        await callback_query.message.answer('Объявление удалено', reply_markup=kb.markup_more_ann)
    except IndexError:
        await callback_query.message.answer('Все объявления удалены.')







@dp.message_handler(text=['Зарегистрировать событие'])
async def process_start_command(message: types.Message):
    db.create_table_announcement()
    await poster.Town.set()
    await message.answer("Пожалуйста, выберите Ваш город, используя клавиатуру ниже.",
                         reply_markup=kb.inline_keyboard())


@dp.callback_query_handler(state=poster.Town)
async def process_callback_button1(callback_query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['Town'] = callback_query.data
    await poster.Type.set()
    await callback_query.message.answer("Укажите тип мероприятия.")


@dp.message_handler(state=poster.Type)
async def process_start_command(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['Type'] = message.text
    await poster.Title.set()
    await message.answer("Укажите название мероприятия.")


@dp.message_handler(state=poster.Title)
async def process_start_command(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['Title'] = message.text
    await poster.Description.set()
    await message.answer("Укажите описание мероприятия.")


@dp.message_handler(state=poster.Description)
async def process_start_command(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['Description'] = message.text
    await poster.Place.set()
    await message.answer("Укажите место проведения мероприятия.")


@dp.message_handler(state=poster.Place)
async def process_start_command(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['Place'] = message.text
    await poster.DateTime.set()
    await message.answer("Укажите дату и время проведения мероприятия.")


@dp.message_handler(state=poster.DateTime)
async def process_start_command(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['DateTime'] = message.text
    await poster.Cost.set()
    await message.answer("Укажите стоимость за входной билет.")

@dp.message_handler(state=poster.Cost)
async def process_start_command(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['Cost'] = message.text
    await poster.TelNumber.set()
    await message.answer("Пожалуйста, укажите Ваш номер телефона.")


@dp.message_handler(state=poster.TelNumber)
async def process_start_command(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['TelNumber'] = message.text
        data['Approved'] = 'Disapproved'
    await message.answer("Спасибо, объявление сохранено.")
    data = await state.get_data()
    db.add_to_db_announcement(list(data.values()))
    await state.finish()


@dp.message_handler(commands='all')
async def process_start_command(message: types.Message):
    await message.answer(db.all_announcements())





@dp.message_handler(text=['Посмотреть события города'])
async def process_start_command(message: types.Message):
    await ShowPoster.Town.set()
    await message.answer("Пожалуйста, выберите Ваш город, используя клавиатуру ниже.",
                         reply_markup=kb.inline_keyboard())


@dp.callback_query_handler(state=ShowPoster.Town)
async def process_callback_button1(callback_query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['Town'] = callback_query.data
    data = await state.get_data()
    if not db.approved_user_announcement(list(data.values())[0]):
        await callback_query.message.answer('В данном городе нет объявлений')
    else:
        poster = db.approved_user_announcement(list(data.values())[0])
        for i in poster:
            text = f'''\n
                        ID: {i[0]}\n
                        Город: {i[1]}\n
                        Тип мероприятия: {i[2]}\n
                        Название: {i[3]}
                        Описание: {i[4]}\n
                        Место проведения: {i[5]}\n
                        Дата и время: {i[6]}\n
                        Стоимость: {i[7]}\n
                        Телефон: {i[8]} \n
                        Подтверждение: {i[9]}\n'''
            await callback_query.message.answer(text)
    await state.finish()
