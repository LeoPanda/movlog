import re
from server.tables.func import get_tables_from_storage


def c2s_hook(d):
    # google api serviceから得られるJsonデータのkey名はcamel case
    # このcamel case のkey名をsnake case に変換するmethodを与える
    # (exsample)
    # dict = json.load(json_object,object_hook=c2s_hook)
    converted = {__camel2snake(key): value for key, value in d.items()}
    return __ObjectLike(converted)


class __ObjectLike(dict):
    __getattr__ = dict.get


def __camel2snake(word):
    return re.sub("([A-Z])", "_\\1", word).lower().lstrip("_")


def prevent_overwrite(org_events: list, new_events: list) -> list:
    # 既存のイベント情報を上書きしないようチェックする
    #
    # start要素がないeventは許可しない
    # すでにオリジナルに存在するイベントは許可しない
    permitted_events = []
    for new_event in new_events:
        if new_event.get("start") is None:
            continue
        if new_event.get("id") not in [org_event.get("id") for org_event in org_events]:
            print(new_event.get("summary"), end=" ")
            permitted_events.append(new_event)
    return permitted_events


JIMAKU_PATERN = [re.compile(r'\（.*字.*\）'),
                 re.compile(r'\(.*字.*\)'), re.compile(r'.*字幕.*')]  # 字幕判別パターン
OMMIT_PATERN = [re.compile(r'\(.*\)'), re.compile(r'（.*）'),
                re.compile(r'【.*】'), re.compile(r'\[.*\]'), re.compile(r'字幕 ')]  # 省略する文字のパターン


def get_screen_types(summary: str) -> list:
    # サマリータイトルからスクリーンタイプを検出し、セットする
    retrun_types = []
    for keyword in get_tables_from_storage()["screenTypes"]:
        if keyword in summary or __to_zenkaku(keyword) in __to_zenkaku(summary):
            retrun_types.append(keyword)
    return retrun_types


def __to_zenkaku(text):
    # 半角文字を全角に
    return text.translate(str.maketrans({chr(0x0021 + i): chr(0xFF01 + i) for i in range(94)}))


def __is_domestic(summary: str) -> bool:
    # サマリータイトルに字幕の文字が含まれるかどうかを判定する
    ret = False
    for r in JIMAKU_PATERN:
        ret = ret or bool(re.search(r, summary))
    return not ret


def organized_event_info(events):
    # event情報を再構成する
    for event in events:
        summary = event.get('summary')
        event["title"] = __get_clean_title(summary)
        event["is_domestic"] = __is_domestic(summary)
        event["screen_type"] = get_screen_types(summary)
        location = __transHankaku(event.get('location'))
        event["location"] = location.split(',')[0].replace(
            ' ', '') if location is not None else location
    return events


def __get_clean_title(title: str):
    # 映画タイトルから括弧などを取り除いて検索にヒットしやすい形に整形する
    for regex in OMMIT_PATERN:
        title = re.sub(regex, '', title)
    return title


def temporarry_event_rewrite(events):
    # FIXME:location情報のための一時ロジック
    for event in events:
        event["location"] = __transHankaku(event["location"])
        print(event["location"])
    return events


def __transHankaku(zenkaku):
    # 全角英文字を半角に変換する
    if zenkaku is None:
        return None
    return zenkaku.translate(str.maketrans({chr(0xFF01 + i): chr(0x21 + i) for i in range(94)}))
