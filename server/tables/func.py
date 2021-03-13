from server.model.tablesSchema import TablesSchema
from flask import jsonify

tables_schema = TablesSchema(schema_name="tables")


def get_tables_from_storage():
    # ストレージからキーワード情報を読み込む
    return tables_schema.loads_from_storage()


def save_tables_to_storage(tableJson):
    # キーワード情報をストレージへ書き込む
    tables_schema.save_to_storage(tableJson)
    return jsonify({"success": "Tables are successfuly saved to storage."})


def initial_tables():
    # テーブルの初期化
    SCREEN_TYPES = ['4K', '3D', 'IMAX', '4DX']
    PROVIDERS = ['NETFLIX', 'AmazonPrime', 'U-NEXT', 'AppleTV', 'DesneyPlus']
    KEY_WORDS = ["TOHOシネマズ", "シネマ", "MOVIX京都", "１０９", "109シネマズ", "ＴＯＨＯシネマズ",
                 "テアトル", "シネ・リーブル", "キネカ", "Ｔ・ジョイ", "ピカデリー", "武蔵野館"]
    return save_tables_to_storage(
        {"keywords": KEY_WORDS, "screenTypes": SCREEN_TYPES, "providers": PROVIDERS})
