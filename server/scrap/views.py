from server.scrap import imdb, eiga_db, tmdb
from flask import Blueprint, jsonify

scrap = Blueprint('scrap', __name__)


@scrap.route('/scrap/eiga_db/search/<title>')
def search_eigadb(title):
    # 映画DBから映画タイトルを検索する
    return jsonify(eiga_db.search_by_title(title))


@scrap.route('/scrap/eiga_db/get/<id>')
def get_eiga_detail(id):
    # 映画DBから映画の詳細情報を取得する
    return jsonify(eiga_db.get_detail(id))


@scrap.route('/scrap/imdb/search/<title>')
def search_imdb(title):
    # IMDBから映画タイトルを検索する
    return jsonify(imdb.search_by_title(title))


@scrap.route('/scrap/imdb/get/<id>')
def get_imdb_detail(id):
    # IMDBから映画の詳細情報を取得する
    return jsonify(imdb.get_detail(id))


@scrap.route('/scrap/tmdb/search/<title>')
def search_tmdb(title):
    # TMDBから映画タイトルを検索する
    return jsonify(tmdb.search_by_title(title))


@scrap.route('/scrap/tmdb/get/<id>')
def get_tmdb_detail(id):
    # TMDBから映画の詳細情報を取得する
    return jsonify(tmdb.get_detail(id))


@scrap.route('/scrap/tmdb/credit/<id>')
def get_tmdb_credits(id):
    # TMDBから映画のクレジット情報を取得する
    return jsonify(tmdb.get_credits(id))
