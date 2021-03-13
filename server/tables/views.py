from flask import Blueprint,  jsonify
from flask.globals import request
from server.tables import func


tables = Blueprint('tables', __name__)


@tables.route('/tables/list')
def tbl_list():
    # ストレージからテーブル情報を取得する
    return jsonify(func.get_tables_from_storage())


@tables.route('/tables/upload', methods=['GET', 'PUT', 'POST'])
def tbl_upload():
    # テーブル情報をストレージに書き込む
    return func.save_tables_to_storage(request.get_json())


@tables.route('/tables/init')
def tbl_init():
    # テーブルの初期化
    func.initial_tables()
    return "Done"
