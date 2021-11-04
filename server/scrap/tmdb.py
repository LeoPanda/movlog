from server.scrap import func
import re
from server.secret import TMDB_KEY
from server.exceptions import MovlogException
import json
import requests

URL = {"site": "https://api.themoviedb.org/3",
       "search": "/search/movie?query=",
       "detail": "/movie/"}

IMG_URL = {"base": "https://image.tmdb.org/t/p",
           "tumb": "/w45", "small": "/w92", "middle": "/w154", "large": "/w300", "big": "/w500"}


def search_by_title(title):
    # TMDBからタイトルに一致する作品のリストを取得する
    items = []
    for element in __get_api_ret("search", title)['results']:
        items.append(__get_detail_common_item(element, 'tumb'))
    return items


def get_detail(id):
    # TMDBから映画の詳細情報を得る
    response = __get_api_ret("detail", id)
    detail = __get_detail_common_item(response)

    if 'vote_average' in response:
        rating = response['vote_average']
        detail.update({"rate": "{:.1f}".format(rating)})

    if 'original_title' in response:
        detail.update({'en_title': response['original_title']})

    if 'overview' in response:
        detail.update({'outline': response['overview']})

    if 'imdb_id' in response:
        detail.update(
            {'imdb_id': re.sub(r'tt(\d+)$', '\\1', response['imdb_id'])})

    return detail


def __get_detail_common_item(element, img_size='middle'):
    # 詳細情報の共通アイテムを生成する
    item = {"id": element['id'], "title": element['title']}
    img_src_item = __get_img_src_item('poster_path', element, img_size)
    if img_src_item is not None:
        item.update(img_src_item)
    return item


def get_credits(id):
    # TMDBからクレジット情報（映画のキャストとクルーの一覧）を取り出す
    response = __get_api_ret("credit", id)

    if not 'credits' in response:
        raise MovlogException('credits not found.')

    credits_response = response['credits']

    return {"casts": __get_casts(credits_response),
            "crews": __get_crews(credits_response)}


def __element_setter(response, credit):
    # クレジット情報を生成する共通ロジック
    def decolator(func) -> list:
        credits = []
        if credit in response:
            for element in response[credit]:
                item = __get_credit_common_item(element)
                extra_item = func(element)
                if len(extra_item) > 0:
                    item.update(extra_item)
                credits.append(item)
        return credits
    return decolator


def __get_credit_common_item(element):
    # クレジット情報の共通アイテムを生成する
    item = {"id": element['id'], "name": element['name']}
    if "original_name" in element:
        item.update({"original_name": element['original_name']})
    img_src_item = __get_img_src_item("profile_path", element, "tumb")
    if img_src_item is not None:
        item.update(img_src_item)
    return item


def __get_casts(response):
    # クレジット情報（キャスト）を生成
    @ __element_setter(response, "cast")
    def item_setter(element):
        # キャスト独自アイテムの生成
        item = {}
        if "character" in element:
            item.update({"role": element['character']})
        return item
    return item_setter


def __get_crews(response):
    # クレジット情報（クルー）を生成
    @ __element_setter(response, "crew")
    def item_setter(element):
        # クルー独自アイテムの生成
        item = {}
        if "job" in element:
            item.update({"role": element['job']})
        return item
    return item_setter


def __get_img_src_item(key, element, size):
    # TMDB画像イメージのdict要素を生成する
    img_src_item = None
    if key in element:
        if element[key] is not None:
            img_src_item = {
                "img_src": IMG_URL['base'] + IMG_URL[size] + element[key]}
    return img_src_item


def __get_api_ret(usage, keyword):
    # tmdb apiの処理結果をdictで受け取る
    if usage == "credit":
        url = __get_urls("detail", keyword) + "&append_to_response=credits"
    else:
        url = __get_urls(usage, keyword)

    ret = json.loads(requests.get(url).text)
    if "success" in ret:
        success = ret['success']
        if success is False:
            raise MovlogException(ret['status_message'])

    return ret


def __get_urls(usage, keyword):
    # tmdb api URLSを生成する
    params = ("&" if usage == 'search' else "?") + \
        "api_key=" + TMDB_KEY + "&language=ja"
    return func.get_url(URL, usage) + keyword + params
