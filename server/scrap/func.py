import requests
import re
from bs4 import BeautifulSoup

URLS = {"eiga_db":
        {"site": "https://eigadb.com",
         "search": "/search-cinema/result?AllSearchForm%5Bkeyword%5D=",
         "detail": "/", },
        "imdb":
        {"site": "https://www.imdb.com",
         "search": "/find?&s=tt&ttype=ft&ref_=fn_tt&&q=",
         "detail": "/title/tt"}}

EIGA_IMG_PATERN = re.compile(r'.*(http.*)\'')
IMDB_ID_PATERN = re.compile(r'^\/title\/tt(\d+)\/$')


def get_url(site, usage):
    # スクレイプ先サイトのURLを取得する
    site_url = str(URLS.get(site).get("site"))
    usage_path = str(URLS.get(site).get(usage))
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


def search_eiga_by_title(title):
    # 映画DBからタイトルに一致する作品のリストを取得する
    @searched_item_list_maker(get_url("eiga_db", "search") + title,
                              tag='li', class_='searchResult-movie__listItem p-listItem')
    def get_eiga_item(element):
        id = element.h3.a['href'][1:]
        title = element.h3.a.text
        item = {"id": id, "title": title}
        img_src = EIGA_IMG_PATERN.match(element.span['style'])
        if(img_src is not None):
            item.update({"img_src": img_src[1]})
        return item
    return get_eiga_item


def search_imdb_by_title(title):
    # imdbからタイトルに一致する作品のリストを取得する
    @searched_item_list_maker(get_url("imdb", "search") + title,
                              tag='tr', class_='findResult')
    def get_imdb_item(element):
        title_section = element.find('td', class_='result_text')
        id_match = IMDB_ID_PATERN.match(title_section.a['href'])
        if not(id_match):
            return None
        else:
            id = id_match[1]

        title = ""
        for string in title_section.strings:
            title += string

        item = {"id": id, "title": title}

        img_src_segment = element.find('td', class_='primary_photo')
        if img_src_segment is not None:
            item.update({"img_src": img_src_segment.find('img')['src']})
        return item
    return get_imdb_item


def get_eiga_detail(id):
    # 映画DBから映画の詳細情報を取得する
    res = requests.get(get_url("eiga_db", "detail") + id)
    soup = BeautifulSoup(res.text, 'html.parser')

    title_section = soup.find('div', class_="movieDetail-top-heading")
    if title_section is not None:
        title = title_section.h2.text if title_section.h2 is not None else None

        en_title_section = title_section.find('span', class_="en")
        en_title = en_title_section.text if en_title_section is not None else None
    else:
        title = None
        en_title = None

    rate_section = soup.find('div', class_='movieDetail-top-score')
    rate = rate_section.find('span', class_='en').text

    outline_section = soup.find(
        'div', class_='movieDetail-top-highlight__desc')
    outline = outline_section.text.strip('\n').strip(
        ' ') if outline_section is not None else None

    img_src_section = soup.find('span', class_="figure__img")["style"]
    img_src_match = EIGA_IMG_PATERN.match(
        img_src_section) if img_src_section is not None else None

    detail = {"id": id}
    if title is not None:
        detail.update({"title": title})
    if outline is not None:
        detail.update({"outline": outline})
    if en_title is not None:
        detail.update({"en_title": en_title})
    if img_src_match is not None:
        detail.update({"img_src": img_src_match[1]})
    if rate_section is not None:
        if rate != '- ':
            detail.update({"rate": rate})
    return detail


def get_imdb_detail(id):
    # IMDBから映画の詳細情報を得る
    res = requests.get(get_url("imdb", "detail") + id)
    soup = BeautifulSoup(res.text, 'html.parser')

    rating_section = soup.find('div', class_='ratingValue')
    title_section = soup.find('div', class_='titleBar')

    img_src_section = soup.find('div', class_='poster')

    detail = {"id": id}
    if rating_section is not None:
        detail.update({"rate": rating_section.find(
            'span', itemprop="ratingValue").text})

    if title_section is not None:
        original_title_section = title_section.find(
            'div', class_='originalTitle')
        if original_title_section is not None:
            en_title = list(original_title_section.strings)[0]
        else:
            en_title = str.rstrip(list(title_section.find(
                'div', class_='title_wrapper').h1.strings)[0])

        detail.update({'en_title': en_title})

    if img_src_section is not None:
        detail.update({'img_src': img_src_section.find('img')['src']})

    return detail
