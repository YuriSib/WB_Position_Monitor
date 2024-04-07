from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Начать')]
],
                           resize_keyboard=True,
                           input_field_placeholder='Выберите пункт ниже')


step1 = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Начало', callback_data='begin')]
])


start_monitoring = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Запуск мониторинга', callback_data='start_monitoring')],
    [InlineKeyboardButton(text='В начало', callback_data='begin')]
])

stop_monitoring = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Остановить мониторинг', callback_data='stop_monitoring')]
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
