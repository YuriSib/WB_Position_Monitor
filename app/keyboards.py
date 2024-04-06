from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Начать')]
],
                           resize_keyboard=True,
                           input_field_placeholder='Выберите пункт ниже')


begin = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Начало', callback_data='begin')],
])


start_monitoring = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Запуск мониторинга', callback_data='start_monitoring')],
    [InlineKeyboardButton(text='В начало', callback_data='begin')]
])


step2_v1 = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Перезаписать таблицу', callback_data='write'),
     InlineKeyboardButton(text='Дополнить таблицу', callback_data='append')],
    [InlineKeyboardButton(text='Запуск мониторинга', callback_data='start_monitoring')],
    [InlineKeyboardButton(text='В начало', callback_data='begin')]
])


step3_v1 = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Подтвердить', callback_data='confirm_add')],
    [InlineKeyboardButton(text='В начало', callback_data='begin')]
])


step2_v2 = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Загрузить таблицу', callback_data='write')],
    ])

download_csv = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Скачать сsv', callback_data='download')],
    [InlineKeyboardButton(text='В начало', callback_data='begin')],
])

year_range = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='2000 - 2005', callback_data='year_2000-2005'),
     InlineKeyboardButton(text='2000 - 2010', callback_data='year_2000-2010')],
    [InlineKeyboardButton(text='2005 - 2010', callback_data='year_2005-2010'),
     InlineKeyboardButton(text='2005 - 2015', callback_data='year_2005-2015')],
    [InlineKeyboardButton(text='2010 - 2015', callback_data='year_2010-2015'),
     InlineKeyboardButton(text='2010 - 2020', callback_data='year_2010-2020')],
    [InlineKeyboardButton(text='2015 - 2020', callback_data='year_2015-2020'),
     InlineKeyboardButton(text='от 2015', callback_data='year_2015')],
    [InlineKeyboardButton(text='от 2020', callback_data='year_2020')]
])

manufacturer = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Русские и иномарки', callback_data='from_all'),
     InlineKeyboardButton(text='Иномарки', callback_data='from_foreign')],
])

confirmation = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Продолжить', callback_data='confirmation_yes'),
     InlineKeyboardButton(text='Назад', callback_data='confirmation_no')],
])