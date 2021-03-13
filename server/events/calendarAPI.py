from re import S
from typing import Tuple
from googleapiclient.discovery import build
from server.model.func import c2s_hook, prevent_overwrite
from server.tables.func import get_tables_from_storage
import json

QUERY_PARMS = {'calendarId': 'primary', 'maxResults': '10', 'singleEvents': 'True',
               'fields': 'nextPageToken,items(id,summary,location,start(dateTime),htmlLink)'}


def get_calendar_service(creds):
    # カレンダーサービスを返す
    return build('calendar', 'v3', credentials=creds) if creds is not None else None


def get_event_units(service, q, time_min=None, next_token=None) -> Tuple[list, str]:
    # カレンダーからqに指定された検索文字にヒットするイベントをAPI Json形式で単位件数づつ取り出す
    query = {'q': q}
    if time_min is not None:
        query.update({'timeMin': time_min})
    query.update(QUERY_PARMS)
    if next_token is not (None or 'continue'):
        query.update({'pageToken': next_token})
    events = service.events()
    request = events.list(**query)
    result = request.execute()
    return result.get('items', []), result.get(('nextPageToken'), None)


def to_json_list(events):
    # camel name から snake nameに変換する
    # json listに変換する
    return json.loads(events, object_hook=c2s_hook)


def get_calendar_events(creds, time_min=None) -> list:
    # カレンダーからSERCH_WORDSにヒットするすべてのイベントをJson形式で取得する
    # time_maxをパラメータ指定された場合は、そのリストの最新日付以後のイベントを取得する。
    service = get_calendar_service(creds)
    if service is None:
        return []
    events = []
    for q in get_tables_from_storage()["keywords"]:
        next_token = "continue"
        while next_token is not None:
            event_units, next_token = get_event_units(
                service, q, next_token=next_token, time_min=time_min)
            events.extend(prevent_overwrite(events, event_units))

    return to_json_list(json.dumps(events))


def get_calendar_events_temp(creds, time_min=None) -> list:
    # FIXME:新宿武蔵野館を忘れていたのでデータ追加のための臨時ファンクション
    service = get_calendar_service(creds)
    if service is None:
        return []
    events = []
    for q in ["武蔵野館"]:
        next_token = "continue"
        while next_token is not None:
            event_units, next_token = get_event_units(
                service, q, next_token=next_token, time_min=time_min)
            events.extend(prevent_overwrite(events, event_units))

    return to_json_list(json.dumps(events))
