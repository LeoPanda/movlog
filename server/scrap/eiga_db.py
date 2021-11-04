from server.scrap import func
from server.exceptions import MovlogException
import re
from bs4 import BeautifulSoup
import requests

URL = {"site": "https://eigadb.com",
       "search": "/search-cinema/result?AllSearchForm%5Bkeyword%5D=",
       "detail": "/", }

IMG_PATERN = re.compile(r'.*(http.*)\'')


def search_by_title(title):
    # 映画DBからタイトルに一致する作品のリストを取得する
    @func.searched_item_list_maker(func.get_url(URL, "search") + title,
                                   tag='li', class_='searchResult-movie__listItem p-listItem')
    def get_item(element):
        id = element.h3.a['href'][1:]
        title = element.h3.a.text
        item = {"id": id, "title": title}
        img_src = IMG_PATERN.match(element.span['style'])
        if(img_src is not None):
            item.update({"img_src": img_src[1]})
        return item
    return get_item


def get_detail(id):
    # 映画DBから映画の詳細情報を取得する
    res = requests.get(func.get_url(URL, "detail") + id)
    if res.ok is False:
        raise MovlogException(res.reason)

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
    img_src_match = IMG_PATERN.match(
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
