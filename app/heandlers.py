from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery, FSInputFile
import asyncio
import os

import WB_Position_Monitor.app.keyboards as kb
from WB_Position_Monitor.WB_scrapper import WBMonitor
from WB_Position_Monitor.table_work import (get_searching_data, union_table, path_to_table,
                                            path_to_add_table, path_to_result_table)

router = Router()
bot = Bot(token='7192705317:AAHYlGUZTtmB7v5AtRyegt8neYMkTf1kmvg')

search_filter = {}


@router.message(F.text == 'Начать')
async def catalog(message: Message):
    await message.answer('Старт работы бота:', reply_markup=kb.begin)


@router.message(F.document)
async def get_csv(message: Message):
    document = message.document
    file_id = document.file_id
    file_name = document.file_name

    file = await bot.get_file(file_id)
    file_path = file.file_path

    await bot.download_file(file_path, destination=f"./{file_name}")
    await message.reply(f"Файл {file_name} успешно сохранен.")


@router.callback_query(lambda callback_query: callback_query.data.startswith('begin'))
async def step_1(callback: CallbackQuery, bot):
    if os.path.exists(path_to_table):
        print(f"Файл {path_to_table} существует.")
        await callback.answer('Есть таблица', show_alert=False)
        await callback.message.answer(f'Есть таблица')
        await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)
        await bot.send_message(chat_id=callback.from_user.id, text="Выберите, что делать с таблицей:",
                               reply_markup=kb.step2_v1)
    else:
        print(f"Файл {path_to_table} не существует.")
        await callback.answer('Таблицы нет', show_alert=False)
        await callback.message.answer(f'Таблицы нет')
        await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)
        await bot.send_message(chat_id=callback.from_user.id, text="Выберите, что делать с таблицей:",
                               reply_markup=kb.step2_v2)


@router.callback_query(lambda callback_query: callback_query.data.startswith('write'))
async def write_csv(callback: CallbackQuery, bot):
    if os.path.exists(path_to_table):
        os.remove(path_to_table)

    await callback.message.answer(f'Загрузите csv-таблицу')
    await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)
    await bot.send_message(chat_id=callback.from_user.id, text="Добавьте csv-таблицу и запускайте мониторинг:",
                           reply_markup=kb.start_monitoring)


@router.callback_query(lambda callback_query: callback_query.data.startswith('append'))
async def cb_choice_year(callback: CallbackQuery, bot):
    await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)
    await bot.send_message(chat_id=callback.from_user.id, text='Добавьте csv-таблицу с именем "Добавление.csv", и '
                                                               'кликните "Подтвердить":', reply_markup=kb.step3_v1)


@router.callback_query(lambda callback_query: callback_query.data.startswith('confirm_add'))
async def cb_choice_year(callback: CallbackQuery, bot):
    if os.path.exists(path_to_add_table):
        await union_table()
        await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)
        await bot.send_message(chat_id=callback.from_user.id, text='Начните мониторинг',
                               reply_markup=kb.start_monitoring)
    else:
        await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)
        await callback.answer('Добавьте таблицу', show_alert=False)
        await callback.message.answer(f'Таблица "Добавление.csv" не найдена')
        await bot.send_message(chat_id=callback.from_user.id, text='Добавьте csv-таблицу с именем "Добавление.csv", и '
                                                                   'кликните "Подтвердить":', reply_markup=kb.step3_v1)


async def monitoring():
    searching_data = await get_searching_data()
    positions = {}
    for article in searching_data:
        wbm = WBMonitor(target_article=article)
        qwery_positions = []
        for qwery in searching_data.get(article):
            num_position = await wbm.hoarder(qwery)
            print(f'Позиция артикула {article} по запросу "{qwery}" - {num_position}')
            qwery_positions.append((qwery, num_position))
        positions[f'{article}'] = qwery_positions

    return positions


@router.callback_query(lambda callback_query: callback_query.data.startswith('start_monitoring'))
async def start_monitoring(callback: CallbackQuery, bot):
    user_id = callback.from_user.id

    if os.path.exists(path_to_table):
        print('Файл найден, можно мониторить')
        await bot.delete_message(chat_id=user_id, message_id=callback.message.message_id)
        await bot.send_message(chat_id=user_id, text='Начинаю мониторинг выдачи')

        while True:
            positions = await monitoring()
            await bot.send_message(chat_id=user_id, text=str(positions))

            print(positions)

            if os.path.exists(path_to_result_table):
                file_input = FSInputFile(path_to_result_table)
                await bot.send_document(
                    callback.from_user.id, file_input,
                    caption=f'Текущий результат мониторинга')

            for min_ in range(60):
                print(f'{60 - min_}')
                await asyncio.sleep(60)

    else:
        print('Файл не найден, мониторить нельзя')
        await bot.send_message(chat_id=user_id, text='Файла с именем "Позиции по поисковым запросам.csv" не найдено!')
        await bot.send_message(chat_id=callback.from_user.id, text="Добавьте csv-таблицу и запускайте мониторинг:",
                               reply_markup=kb.start_monitoring)


@router.callback_query(lambda callback_query: callback_query.data.startswith('download'))
async def cb_choice_year(callback: CallbackQuery, bot):
    await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)
    if os.path.exists(path_to_result_table):
        file_input = FSInputFile(path_to_result_table)
        await bot.send_document(
            callback.from_user.id, file_input,
            caption=f'Текущий результат мониторинга')
    else:
        await bot.send_message(chat_id=callback.from_user.id, text="Таблица пока не готова!")
        await bot.send_message(chat_id=callback.from_user.id, text="Скачать результат:",
                               reply_markup=kb.download_csv)


@router.message(F.text == '/my_id')
async def cmd_start(message: Message):
    await message.answer(f'Ваш ID: {message.from_user.id}')
    await message.reply(f'Ваше имя: {message.from_user.first_name}')


@router.message()
async def echo(message: Message):
    await message.answer('Введенный текст не является командой...')
