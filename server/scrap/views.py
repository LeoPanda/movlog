from server.scrap import func
from flask import Blueprint, jsonify

scrap = Blueprint('scrap', __name__)


@scrap.route('/scrap/eiga_db/search/<title>')
def search_eigadb(title):
    # 映画DBから映画タイトルを検索する
    return jsonify(func.search_eiga_by_title(title))


@scrap.route('/scrap/eiga_db/get/<id>')
def get_eiga_detail(id):
    # 映画DBから映画の詳細情報を取得する
    return jsonify(func.get_eiga_detail(id))


@scrap.route('/scrap/imdb/search/<title>')
def search_imdb(title):
    # IMDBから映画タイトルを検索する
    return jsonify(func.search_imdb_by_title(title))


@scrap.route('/scrap/imdb/get/<id>')
def get_imdb_detail(id):
    # IMDBから映画の詳細情報を取得する
    return jsonify(func.get_imdb_detail(id))
