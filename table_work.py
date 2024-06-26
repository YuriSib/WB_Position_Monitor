import csv
import os


path_to_table = r"C:\Users\Administrator\PycharmProjects\WB_bot\WB_Position_Monitor\Позиции по поисковым запросам.csv"
path_to_add_table = r"C:\Users\Administrator\PycharmProjects\WB_bot\WB_Position_Monitor\Добавление.csv"
path_to_result_table = r"C:\Users\Administrator\PycharmProjects\WB_bot\WB_Position_Monitor\Результат.csv"

# path_to_table = r"C:\Users\User\PycharmProjects\WB_Position_Monitoring\Позиции по поисковым запросам.csv"
# path_to_add_table = r"C:\Users\User\PycharmProjects\WB_Position_Monitoring\Добавление.csv"
# path_to_result_table = r"C:\Users\User\PycharmProjects\WB_Position_Monitoring\Результат.csv"

# # Пути для сервера
# path_to_table = r"/root/WB_checker/WB_Position_Monitor/Позиции по поисковым запросам.csv"
# path_to_add_table = r"/root/WB_checker/WB_Position_Monitor/Добавление.csv"
# path_to_result_table = r"/root/WB_checker/WB_Position_Monitor/Результат.csv"


async def get_searching_data(table='Позиции по поисковым запросам.csv'):
    with open(table, newline='', encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile, delimiter=";")
        reader_list = [row for row in reader]

        qwery_list = []
        for row in reader_list:
            cnt = 0
            for i in row:
                if cnt == 0:
                    cnt += 1
                    continue
                if i not in qwery_list:
                    qwery_list.append(i)

        qwery_list.remove('')

        searching_data = {}
        for qwery in qwery_list:
            for row_2 in reader_list:
                art = int(row_2[0].replace('\ufeff', ''))
                row_2.remove('') if '' in row_2 else row_2
                if qwery in row_2:
                    if searching_data:
                        if qwery in searching_data:
                            searching_data[qwery].append(art)
                        else:
                            searching_data[qwery] = [art]
                    else:
                        searching_data[qwery] = [art]

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
        for key in merged_dict:
            qwery = ', '.join(merged_dict[key])
            wither.writerow([key, qwery])


async def create_result_table(result_dict):
    with open(path_to_result_table, 'w', newline='', encoding="utf-8") as csvfile:
        wither = csv.writer(csvfile, delimiter=";")
        for key in result_dict:
            for value in result_dict[key]:
                try:
                    qwery_key, position = value[0], value[1]
                    print(qwery_key, position)
                    wither.writerow([key, qwery_key, position])
                except AttributeError:
                    print(value)


