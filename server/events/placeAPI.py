import requests
import json
from flask import jsonify
from collections import Counter
from server.model.locationSchema import LocationSchema
from server.secret import API_KEY

PLACE_URL = "https://maps.googleapis.com/maps/api/place"
SEARCH_URI = "/textsearch/json?query="
FIELDS = "&fields=name,geometry,photos"
PHOTO_URI = "/photo?maxwidth=300&photoreference="

location_schema = LocationSchema(schema_name="location", many=True)


def get_locations_from_storage():
    # ストレージからロケーション情報を取り出す
    return location_schema.loads_from_storage()


def save_locations(locations):
    # Json形式で受け取ったロケーション情報をストレージに保存する
    location_schema.save_to_storage(location_schema.loads_from_json(locations))
    return "success"


def add_new_locations_to_store(events):
    # 指定したイベント情報から抽出した劇場名のうち、ロケーションファイルに保管していないものがあれば
    # google place APIから情報を付加し、ロケーションファイルに追加する
    location_names_on_events = get_location_names(events)
    locations_on_storage = get_locations_from_storage()
    location_names_on_storage = list(map(
        lambda location: location["name"], locations_on_storage))
    new_names = get_new_location_names(
        location_names_on_events, location_names_on_storage)
    if new_names is not None:
        locations_on_storage.extend(get_location_info_by_names(new_names))
        location_schema.save_to_storage(locations_on_storage)
    return jsonify({"success": "locations are successfuly saved to storage."})


def get_location_info_by_names(names):
    # 劇場名リストを元にロケーション情報リストを得る
    locations = []
    for name in names:
        print(name, end=" ")
        # 補完するロケーション情報はname一件につき一件づつにする
        # nameはイベント情報から得たものの方を採用する
        locations.append(get_place_infos(name, isSingle=True)[0])
    return locations


def get_new_location_names(current_names, storage_names):
    # ストレージに保管されていないロケーション名を検出する
    new_names = []
    print("new locations:")
    for current in current_names:
        exsists = list(
            filter(lambda storage: storage == current, storage_names))
        if(len(exsists) == 0):
            print(current, end=" ")
            new_names.append(current)
    return new_names if len(new_names) > 0 else None


def get_place_infos(name, isSingle=False, isPhoto=True):
    # nameをkey にして google map  API からPlace情報を検索する
    req = PLACE_URL+SEARCH_URI+name+FIELDS+"&language=ja"+"&key="+API_KEY
    res = json.loads(requests.get(req).text)
    status = res.get('status')
    if status != 'OK':
        return [{"error": status}]
    else:
        results = res.get('results')
        infos = []
        if isSingle:
            infos.append(set_place_info(results[0], isPhoto))
        else:
            for result in results:
                infos.append(set_place_info(result, isPhoto))
        return infos


def set_place_info(result, isPhoto=True):
    # google place情報をdictにセットする
    info = {"place_id": result.get("place_id")}
    info.update({"name": result.get("name")})
    geometry = result.get("geometry")
    if geometry is not None:
        info.update({"location": geometry.get("location")})
    # アイコンイメージ取得(isPhoto=Trueの時のみ)
    photos = result.get("photos")
    photo_reference = photos[0].get(
        "photo_reference") if ((photos is not None) and isPhoto) else None
    if photo_reference is not None:
        photo_url = get_photo_url(photo_reference)
        if photo_url is not None:
            info.update({"photo_url": photo_url})

    return info


def get_photo_url(reference):
    # 場所の写真URLを取得する
    req = PLACE_URL+PHOTO_URI + reference + "&key=" + API_KEY
    return requests.get(req).url


def get_location_names(events) -> list:
    # イベント情報のロケーション名一覧を取得する
    locations = list(
        map(lambda event: event['location'].split(',')[0].replace(' ', ''), events))
    return list(Counter(locations))
