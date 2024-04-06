import csv
import os


path_to_table = r"C:\Users\Administrator\PycharmProjects\WB_bot\WB_Position_Monitor\Позиции по поисковым запросам.csv"
path_to_add_table = r"C:\Users\Administrator\PycharmProjects\WB_bot\WB_Position_Monitor\Добавление.csv"
path_to_result_table = r"C:\Users\Administrator\PycharmProjects\WB_bot\WB_Position_Monitor\Результат.csv"


async def get_searching_data(table='Позиции по поисковым запросам.csv'):
    searching_data = {}

    with open(table, newline='', encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        for row in reader:
            try:
                article = int(row['\ufeffАртикул'])
            except KeyError:
                article = int(row['Артикул'])
            qwery_list = row['Поисковые запросы'].split(', ')
            searching_data[article] = qwery_list

    return searching_data


async def union_table():
    old_searching_data = await get_searching_data()
    new_searching_data = await get_searching_data(path_to_add_table)

    merged_dict = {**old_searching_data, **new_searching_data}
    for key, value in new_searching_data.items():
        if key in old_searching_data:
            merged_dict[key] = list(set(old_searching_data[key] + value))

    os.remove(path_to_table)
    with open(path_to_table, 'w', newline='', encoding="utf-8") as csvfile:
        wither = csv.writer(csvfile, delimiter=";")
        wither.writerow(['Артикул', 'Поисковые запросы'])
        for key in merged_dict:
            qwery = ', '.join(merged_dict[key])
            wither.writerow([key, qwery])


async def create_result_table(result_dict):
    with open(path_to_result_table, 'w', newline='', encoding="utf-8") as csvfile:
        wither = csv.writer(csvfile, delimiter=";")
        wither.writerow(['Артикул', 'Поисковый запрос', 'Позиция в выдаче'])
        for key in result_dict:
            for value in result_dict[key]:
                qwery_key, position = value[0], value[1]
                wither.writerow([key, qwery_key, position])
