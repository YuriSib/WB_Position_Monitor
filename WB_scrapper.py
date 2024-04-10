import requests


class WBMonitor:
    def __init__(self, key):
        # self.id_list = id_list
        self.key = key
        # self.target_article = target_article

    @staticmethod
    def settings(page, key):
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

        url = 'https://search.wb.ru/exactmatch/ru/common/v5/search'

        response = requests.get(url, params=params, headers=headers, timeout=60)
        if response.status_code != 200:
            return 0
        return response.json()

    @staticmethod
    def find_position(response, target_article, cnt=1):
        position_dict = {}
        products_raw = response.get('data', {}).get('products', None)
        if products_raw != None and len(products_raw) > 0:
            for product in products_raw:
                # name = product.get('name', None)
                article = product.get('id', None)
                if article in target_article:
                    position_dict[article] = cnt
                cnt += 1
            return position_dict

    def hoarder(self, target_article_list):
        max_position = 4000
        page_num = 1
        position_num = 1
        finish_flag = False
        full_position_dict = {}
        while True:
            response = self.settings(page=page_num, key=self.key)

            try:
                quantity_cards = len(response['data']['products'])
            except Exception as e:
                print(e)
                return 'Не найдено из-за ошибки'
            if quantity_cards == 1:
                continue
            if quantity_cards != 100:
                finish_flag = True

            position_dict = self.find_position(response=response, target_article=target_article_list, cnt=position_num) if response else []
            full_position_dict.update(position_dict)
            for id_ in position_dict:
                if id_ in target_article_list:
                    target_article_list.remove(id_)

            if not target_article_list:
                return full_position_dict

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
