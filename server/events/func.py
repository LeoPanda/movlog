from flask import jsonify
from urllib.parse import quote
from server.model.eventSchema import EventsSchema
from server.scrap import imdb, eiga_db, tmdb
from server.model.func import prevent_overwrite, shape_event_info
from server.events.calendarAPI import get_calendar_events
from server.events.placeAPI import add_new_locations_to_store
import json

events_schema = EventsSchema(schema_name="events", many=True)


# main function

def add_from_google_calendar(events: list, creds):
    # googleカレンダーから映画鑑賞イベントを抽出し、既存のイベント情報に追加する
    latest_date = events_schema.get_time_max(events)  # メインスキーマの最終更新日の取得
    # FIXME:テスト用件数制限
    #latest_date = '2020-10-01T11:33:00+09:00'
    print(latest_date+"以降のイベントを抽出中..")
    calendar_events = get_calendar_events(
        creds, time_min=latest_date)  # google カレンダーから最新情報の取得

    new_event_candidates = events_schema.load(
        calendar_events, many=True)  # googleカレンダー情報をイベントスキーマに変換
    new_events = __finalize_new_events(  # カレンダー情報からイベント情報を構成する
        prevent_overwrite(events, new_event_candidates))  # カレンダー情報のうち、既存の情報とかぶるものは排除する

    events.extend(new_events)  # 新規イベントを追加
    add_new_locations_to_store(new_events)  # 新規イベントからロケーション情報を再構成する

    return events


def temp_add_event(events: list):
    # FIXME:手動でイベントデータを追加
    temp_event = [{"en_title": "Paterson", "id": "addedbyhand20211114",
                   "is_domestic": False, "location": "ヒューマントラストシネマ有楽町", "my_rate": 7, "outer_id": {"eiga_db": "", "imdb": "", "tmdb": ""},
                   "outline": "",
                   "screen_type": [], "start": {"date_time": "2017-09-05T11:15:00+09:30"}, "title": "パターソン", "title_img": ""}]
    new_event = events_schema.load(temp_event)
    events.extend(new_event)
    return events


def update_with_all_sources(event, force=False):
    # 外部ソースの情報をイベント情報に付加する
    update_with_tmdb(event, force)
    update_with_imdb(event, force)
    update_with_eigadb(event, force)
    __update_title_img(event)


def update_with_eigadb(event: dict, force=False):
    # 映画DBから情報を付加する
    @__search_and_update_with_outer_db(event, "eiga_db", eiga_db.get_detail, force)
    def searcher(queted_title):
        return eiga_db.search_by_title(queted_title)
    return searcher


def update_with_imdb(event: dict, force=False):
    # IMDBから情報を付加する
    @__search_and_update_with_outer_db(event, "imdb", imdb.get_detail, force)
    def searcher(queted_title):
        return imdb.search_by_title(queted_title+"&exact=true")
    return searcher


def update_with_tmdb(event: dict, force=False):
    # TMDBから情報を付加する
    @__search_and_update_with_outer_db(event, "tmdb", tmdb.get_detail, force)
    def searcher(queted_title):
        return tmdb.search_by_title(queted_title+"&exact=true")
    return searcher


def get_events_from_storage():
    # ストレージからイベント情報を取得する
    events = events_schema.get_sorted_by_latest(
        events_schema.loads_from_storage())
    return events


def do_every_events(events: list, func, **options):
    # リストに格納されたイベントに対して関数を逐次実行する
    print("doing every events on strage.")
    for event in events:
        print(event.get('title'), end=" ")
        func(event, **options)
    return events


def update_storage_by(update_func, **options):
    # ストレージ上のイベント情報にupdate_func関数で補足情報を追加し上書きする
    events = update_func(events_schema.loads_from_storage(), **options)
    return save_events_by_schema(events)


def reload_post_events_into_schema(events):
    # start(date-tmie)をstrのまま受け取ってしまうと
    # marshmallowのdumpsが変換エラーを起こすので
    # オブジェクトにされたresponseを一旦jsonにしてからschemaに読み込み直す
    json_events = json.dumps(events)
    return events_schema.loads_from_json(json_events)


def save_events_by_schema(events: str):
    # スキーマを使用してイベント情報をセーブする
    events_schema.save_to_storage(events)
    return jsonify({"success": "Events are successfuly saved to storage."})

# private functions


def __finalize_new_events(new_events):
    # 追加する新規情報を完成させる
    for new_event in new_events:
        shape_event_info(new_event)  # event情報の整形
        update_with_all_sources(new_event)  # 外部ソースの情報を付加
    return new_events


def __search_and_update_with_outer_db(event: dict, key: str, getter, force=False):
    # searcherで指定された関数を用いタイトル名で外部DBを検索し、該当するデータが1件のみ
    # だった場合、そのデータの詳細情報をgetterで指定された関数で取得して
    # イベント情報を更新する
    # event:更新するevent情報
    # key:外部データの識別 imdb or eiga_db or tmdb
    # getter:外部データの情報取得関数
    # force:外部IDがすでに追加済みであっても強制的に更新する
    def decolator(searcher):
        if __event_has_not_this_key(event, key):
            quoted_title = quote(__get_title(event))
            films = searcher(quoted_title)
            if len(films) == 1:
                detail = getter(str(films[0].get("id")))
                __update_event(event, key, detail)
        elif force:
            outer_ids = event["outer_id"]
            id = outer_ids[key] if outer_ids else None
            if id is not None:
                detail = getter(event["outer_id"][key])
                __update_event(event, key, detail)
        return event
    return decolator


def __nested_child_update(parent: dict, key: str, new_child: dict):
    # ネスティングされた辞書のkey値を持つ子アイテムをアップデートする
    if(key in parent):

        child = parent.get(key)
        child.update(new_child)
        parent.update({key: child})
    else:
        parent.update({key: new_child})


def __update_event(event: dict, key: str, detail: dict):
    # イベントをアップデートする
    for k, v in detail.items():
        if k in ('id', 'img_src', 'rate'):
            if(k == 'id'):
                nested_key = 'outer_id'
            elif (k == 'rate'):
                nested_key = 'outer_rate'
            else:
                nested_key = k
            __nested_child_update(event, nested_key, {key: v})
        else:
            if __is_able_overwirte(event, k, v):
                event.update({k: v})


def __is_able_overwirte(event: dict, k, v):
    # 上書してもいい項目かどうかチェックする
    overwite_protected_key = {"title", "en_title", "outline"}
    if not (k in overwite_protected_key):
        return True
    if k in event:
        if len(event.get(k)) > 0:
            return False
    else:
        return True


def __update_title_img(event: dict):
    # タイトルに表示するポスターイメージのURLを選定する
    if 'img_src' not in event:
        return
    if 'title_img' in event:
        return

    img_src = event.get('img_src')
    imdb_src = img_src.get('imdb')
    title_src = imdb_src if imdb_src is not None else img_src.get('tmdb')
    return event.update({"title_img": title_src})


def __event_has_not_this_key(event: dict, key: str):
    # 対象情報の外部IDがイベントに存在しないことを確認する
    id_item = event.get("outer_id")
    if id_item is None:
        return True
    else:
        if id_item.get(key) is None:
            return True
        else:
            return False


def __get_title(event: dict):
    # 検索用映画タイトルの取得
    return event.get('title').replace('\u3000', ' ')
