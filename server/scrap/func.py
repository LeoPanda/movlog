import requests
import re
from bs4 import BeautifulSoup


def get_url(url, usage, *param):
    # スクレイプ先サイトのURLを取得する
    site_url = url.get("site")
    usage_path = (url.get(usage)).format(*param)
    return site_url + usage_path


def searched_item_list_maker(req, tag, **find_options):
    # 検索リスト作成用雛形デコレータ
    def decolator(func) -> list:
        res = requests.get(req)
        soup = BeautifulSoup(res.text, 'html.parser')
        elements = soup.find_all(tag, **find_options)
        items = []
        for element in elements:
            item = func(element)
            if item is not None:
                items.append(item)
        return items
    return decolator
