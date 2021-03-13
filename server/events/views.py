from flask import Blueprint,  jsonify
from flask.globals import request
from server.authorize.func import route_with_creds
from server.events import func
from server.events import placeAPI
from server.model.func import temporarry_event_rewrite


events = Blueprint('events', __name__)


@events.route('/events/list')
def evt_list():
    # ストレージからイベント情報を取得する
    return jsonify(func.get_events_from_storage())


@events.route('/events/upload', methods=['GET', 'PUT', 'POST'])
def evt_upload():
    # JSONデータを受け取ってストレージを更新する
    # marshmallowスキーマにロードし直すため、受信データをいったんJSONに戻している
    events = request.get_json()
    return func.save_events_by_schema(
        func.reload_post_events_into_schema(events))


@events.route('/events/add')
def evt_add():
    @route_with_creds('/events/add')
    def add_events_to_store(creds):
        # googleカレンダーから映画鑑賞イベントを抽出し、情報を補足して追加する
        return func.update_storage_by(func.add_from_google_calendar, creds=creds)
    return add_events_to_store


@events.route('/events/update/all')
def all_sync():
    # ストレージ上のイベント情報に補足情報を追加し上書きする
    # forceパラメータをつけると、すでにIDが確定したeventも強制的に上書きする
    if request.args.get('force') is not None:
        return func.update_storage_by(
            lambda events: func.do_every_events(events, func.update_with_all_sources, force=True))
    else:
        return func.update_storage_by(
            lambda events: func.do_every_events(events, func.update_with_all_sources))


@events.route('/events/update/eiga_db')
def eigadb_sync():
    # ストレージ上のイベント情報に映画DBから補足情報を追加し上書きする
    return func.update_storage_by(
        lambda events: func.do_every_events(events, func.update_with_eigadb))


@events.route('/events/update/imdb')
def imdb_sync():
    # ストレージ上のイベント情報にIMDBから補足情報を追加し上書きする
    return func.update_storage_by(
        lambda events: func.do_every_events(events, func.update_with_imdb))


@events.route('/events/temp')
# FIXME:情報のリライト用テンポラリ
def temp_sync():
    return func.update_storage_by(lambda events: temporarry_event_rewrite(events))


@events.route('/events/location/add')
def location_add():
    # FIXME:ロケーションファイル初期化用（本番時不要）
    # ストレージに補完済のイベント情報から劇場名を取り出し、ロケーション情報を付加した上で
    # ロケーションファイルとしてストレージに追加する
    return jsonify(placeAPI.add_new_locations_to_store(func.get_events_from_storage))


@events.route('/location/upload', methods=['GET', 'PUT', 'POST'])
def location_upload():
    # ロケーション情報のアップロードを受け取ってストレージに追加する
    return placeAPI.save_locations(request.get_json())


@events.route('/location/list')
def location_list():
    # ロケーション情報をストレージから取り出す
    return jsonify(placeAPI.get_locations_from_storage())


@events.route('/place/search/<name>')
def place_list(name):
    # プレース情報を表示する
    return jsonify(placeAPI.get_place_infos(name))
