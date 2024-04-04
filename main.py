from WB_scrapper import get_searching_data, WBMonitor


def main():
    searching_data = get_searching_data()
    for article in searching_data:
        wbm = WBMonitor(target_article=article)
        for qwery in searching_data.get(article):
            num_position = wbm.hoarder(qwery)
            print(f'Позиция артикула {article} по запросу "{qwery}" - {num_position}')


main()

