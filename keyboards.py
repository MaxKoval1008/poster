from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

admin_button = InlineKeyboardButton('Кабинет администратора', callback_data='admin_keyboard')
markup_is_admin = InlineKeyboardMarkup().insert(admin_button)
admin_activate_ann = InlineKeyboardButton('Режим активации объявлений', callback_data='markup_admin_activate_ann')
admin_change_ann = InlineKeyboardButton('Режим редактирования объявлений', callback_data='markup_admin_change_ann')
markup_admin_change_ann = InlineKeyboardMarkup(row_width=1).row(admin_activate_ann,admin_change_ann)
button_change_ann_1 = InlineKeyboardButton('Подтвердить', callback_data='approve_ann')
button_change_ann_2 = InlineKeyboardButton('Отклонить', callback_data='disapprove_ann')
button_change_ann_3 = InlineKeyboardButton('Еще', callback_data='more_ann')

button_0 = KeyboardButton('Зарегистрировать событие')
button_1 = KeyboardButton('Посмотреть события города')


markup_change_mode_ann = InlineKeyboardMarkup(row_width=2).row(button_change_ann_1, button_change_ann_2)
markup_more_ann = InlineKeyboardMarkup().row(button_change_ann_3)

admin_button_1 = KeyboardButton('Объявления')
admin_button_2 = KeyboardButton('Выйти')

markup_admin_keyboard = ReplyKeyboardMarkup(
    resize_keyboard=True,
    one_time_keyboard=False
)
markup_admin_keyboard.row(admin_button_1, admin_button_2)

markup_main = ReplyKeyboardMarkup(row_width=2,
                                  resize_keyboard=True,
                                  one_time_keyboard=False
                                  ).row(button_0, button_1)


button_work = InlineKeyboardButton('Работа', callback_data='Работа')
button_half_work = InlineKeyboardButton('Подработка', callback_data='Подработка')

markup_choice = InlineKeyboardMarkup(row_width=2).insert(button_work)
markup_choice.insert(button_half_work)


towns = ['Заславль', 'Боровляны', 'Сеница', 'Юбилейный', 'Прилуки', 'Михановичи',
         'Мачулищи', 'Гатово', 'Ждановичи', 'Колодищи', 'Березино', 'Борисов',
         'Жодино', 'Копыль', 'Логойск', 'Любань', 'Марьина Горка', 'Мядель',
         'Фаниполь', 'Дзержинск', 'Несвиж', 'Слуцк', 'Смолевичи', 'Червень', 'Осиповичи',
         'Быхов', 'Горки', 'Климовичи', 'Кричев', 'Чериков', 'Гродно', 'Волковыск',
         'Новогрудок', 'Речица', 'Рогачев', 'Поставы']


def inline_keyboard():
    markup = InlineKeyboardMarkup()
    for i in towns:
        markup.add(InlineKeyboardButton(text=f'{i}', callback_data=f'{i}'))
    return markup
