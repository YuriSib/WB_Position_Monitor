import requests


class WBMonitor:
    def __init__(self, key):
        self.key = key

    @staticmethod
    def settings(page, key):
        # Заголовок запроса
        headers = {
            'Accept': '*/*',
            'Accept-Language': 'ru,en;q=0.9',
            'Connection': 'keep-alive',
            'Origin': 'https://www.wildberries.ru',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'cross-site',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 YaBrowser/24.1.0.0 Safari/537.36',
            'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "YaBrowser";v="24.1", "Yowser";v="2.5"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',

        }

        # Параметры запроса
        params = {
            'page': f'{page}',
            # 'ab_testing': 'false',
            'appType': '1',
            'curr': 'rub',
            'dest': '-1257786',
            'query': f'{key}',
            'resultset': 'catalog',
            'sort': 'popular',
            'suppressSpellcheck': 'false',
            # 'limit': '300'
        }

        # К этому урлу мы делаем запрос
        url = 'https://search.wb.ru/exactmatch/ru/common/v5/search'

        response = requests.get(url, params=params, headers=headers, timeout=60)
        if response.status_code != 200:
            return 0
        return response.json()

    # Данный метод найдет артикулы на странице и вернет соотновения {артикул_1: позиция, ... артикул_N: позиция}
    @staticmethod
    def find_position(response, target_article, cnt=1):
        position_dict = {}
        products_raw = response.get('data', {}).get('products', None)

        if products_raw != None and len(products_raw) > 0:
            for product in products_raw:
                article = product.get('id', None)
                if article in target_article:
                    position_dict[article] = cnt
                cnt += 1

            return position_dict

    def hoarder(self, target_article_list):
        # Устанавливаем максимальное количество страниц для парсинга
        max_position = 4000
        page_num = 1
        position_num = 1
        # Когда значяение будет True, пора заканчивать итерацию
        finish_flag = False
        # Словарь с соотношением {артикул: позиция}
        full_position_dict = {}
        while True:
            response = self.settings(page=page_num, key=self.key)
            # Полчаем примерно такой ответ:
            # {'products': [
            #     {'time1': 8, 'time2': 28, 'wh': 120762, 'dtype': 4, 'dist': 105, 'id': 156587416, 'root': 142146198,
            #      'kindId': 5, 'brand': 'abcAge', 'brandId': 674605, 'siteBrandId': 0, 'colors': [], 'subjectId': 213,
            #      'subjectParentId': 4, 'name': 'Колготки детские с рисунком для девочек теплые хлопок',
            #      'supplier': 'Качественные товары', 'supplierId': 233776, 'supplierRating': 4.7, 'supplierFlags': 0,
            #      'pics': 15, 'rating': 5, 'reviewRating': 4.9, 'feedbacks': 10441, 'volume': 44, 'viewFlags': 80,
            #      'sizes': [{'name': '86-92', 'origName': '86-92', 'rank': 563134, 'optionId': 261198743, 'wh': 120762,
            #                 'dtype': 4,
            #                 'price': {'basic': 652700, 'product': 76300, 'total': 76300, 'logistics': 0, 'return': 0},
            #                 'saleConditions': 0,
            #                 'payload': 'g5bE0RO2h2KsCxoEX68Ft9KcstDyRIkrxsOkNckmCRC2TgkCjHpdJ2juaXfmCrV5iU1Uphp3F/txY2U'},
            #                ...],
            #      'log': {'cpm': 344, 'promotion': 1, 'promoPosition': 0, 'position': 11, 'advertId': 15250313,
            #              'tp': 'b'}, ...}

            try:
                # Получаем колчество карточек на странице
                quantity_cards = len(response['data']['products'])
            except Exception as e:
                print(e)
                return 'Не найдено из-за ошибки'
            # Если количество карточек равно 1, значит ответ пришел некорректный, делаем запрос снова.
            if quantity_cards == 1:
                continue
            # Если карточек на странице < 100, значит эта сраница последняя, меняем значение флага.
            if quantity_cards != 100:
                finish_flag = True

            # Ищем нужные артикулы на странице и выводим соотношение типа {166178436: 10, 166178164: 29, 200435939: 47}
            # , если их там нет, возвращаем пустой список
            position_dict = self.find_position(response=response, target_article=target_article_list, cnt=position_num) if response else []
            print(position_dict)

            # Помещаем найденые соотношения в наш основной словарь
            full_position_dict.update(position_dict)

            # Удаляем найденые артикулы из списка
            for id_ in position_dict:
                if id_ in target_article_list:
                    target_article_list.remove(id_)
            # Если список остался пустым, возвращаем словарь с соотношениями
            if not target_article_list:
                return full_position_dict

            # Если нет, проверяес, достигнута ли максимальная страница. Артикулам, позиции которрых не были найдены присваивается значение > 4000
            else:
                if finish_flag or (position_num+100) > max_position:
                    not_found_id_dict = {}
                    for id_ in target_article_list:
                        not_found_id_dict[id_] = f'>{max_position}'
                    full_position_dict.update(not_found_id_dict)
                    return full_position_dict

                page_num += 1
                position_num += 100
                print(f'Перебрано {position_num-1} карточек')


if __name__ == "__main__":
    key = 'Колготки для девочки набор'
    target_article = [166178136, 200435939, 166178164, 166178436]
    wbm = WBMonitor(key=key)
    num_position = wbm.hoarder(target_article)

    for key in num_position:
        print(f'Позиция артикула {key} - {num_position[key]}')
