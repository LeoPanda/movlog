from server.scrap import func
from server.exceptions import MovlogException
import re
from bs4 import BeautifulSoup
import json
import requests

URL = {"site": "https://www.imdb.com",
       "search": "/find?&s=tt&ttype=ft&ref_=fn_tt&&q=",
       "detail": "/title/tt"}

ID_PATERN = re.compile(r'^\/title\/tt(\d+)\/$')


def search_by_title(title):
    # imdbからタイトルに一致する作品のリストを取得する
    @func.searched_item_list_maker(func.get_url(URL, "search") + title,
                                   tag='tr', class_='findResult')
    def get_item(element):
        title_section = element.find('td', class_='result_text')
        id_match = ID_PATERN.match(title_section.a['href'])
        if not(id_match):
            return None
        else:
            id = id_match[1]

        title = ""
        for string in title_section.strings:
            title += string

        if "aka " in title:
            re_title = re.search('"(.*)"', title)
            if re_title:
                title = re_title.group(1)

        item = {"id": id, "title": title}

        img_src_segment = element.find('td', class_='primary_photo')
        if img_src_segment is not None:
            item.update({"img_src": img_src_segment.find('img')['src']})
        return item
    return get_item


def get_detail(id):
    # IMDBから映画の詳細情報を得る
    res = requests.get(func.get_url(URL, "detail") + id)
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
