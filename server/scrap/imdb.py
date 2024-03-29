from server.scrap import func
from server.exceptions import MovlogException
import re
from bs4 import BeautifulSoup
import json
import requests

URL = {"site": "https://www.imdb.com",
       "search": "/find/?q={0}&s=tt&ttype=ft&ref_=fn_tt",
       "detail": "/title/tt{0}"}

ID_PATERN = re.compile(r'^\/title\/tt(\d+)\/.*$')


def search_by_title(title):
    # imdbからタイトルに一致する作品のリストを取得する
    @func.searched_item_list_maker(func.get_url(URL, "search", title),
                                   tag='li', class_='ipc-metadata-list-summary-item')
    def get_item(element):
        title_section = element.find(
            'div', class_='ipc-metadata-list-summary-item__c')
        id_match = ID_PATERN.match(title_section.a['href'])
        if not(id_match):
            return None
        else:
            id = id_match[1]

        title = title_section.find(
            'a', class_='ipc-metadata-list-summary-item__t')

        item = {"id": id, "title": title}

        img_src_segment = element.find('div', class_='gLsKcY')
        if img_src_segment is not None:
            item.update({"img_src": img_src_segment.find('img')['src']})
        return item
    return get_item


def get_detail(id):
    # IMDBから映画の詳細情報を得る
    ua = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
    headers = {'User-Agent': ua}
    res = func.get_by_pretended_browser(func.get_url(URL, "detail", id))
    soup = BeautifulSoup(res.text, 'html.parser')

    script_section = soup.find('script', type='application/ld+json')

    detail = {"id": id}

    if script_section is None:
        raise MovlogException("not Found")
    else:
        json_content = json.loads(script_section.contents[0])

        if 'aggregateRating' in json_content:
            if 'ratingValue' in json_content['aggregateRating']:
                rating = json_content['aggregateRating']['ratingValue']
                detail.update({"rate": "{:.1f}".format(rating)})

        if 'name' in json_content:
            if 'alternateName' in json_content:
                detail.update({'title': json_content['alternateName']})
                detail.update({'en_title': json_content['name']})
            else:
                detail.update({'title': json_content['name']})
                detail.update({'en_title': json_content['name']})

        if 'image' in json_content:
            detail.update({'img_src': json_content['image']})

    return detail
