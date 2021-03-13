from marshmallow import Schema, fields
from server.storage.factory import StorageHanlderFactory, StorageHandler


class MetaSchema(Schema):
    # ストレージハンドラを用いたsave,loadsをバインドした
    # Schemaメタクラス
    def __init__(
        self,
        schema_name=None,
        only=None,
        exclude=(),
        many=False,
        load_only=(),
        dump_only=(),
        unknown=None
    ):
        super().__init__(
            only=only,
            exclude=exclude,
            many=many,
            load_only=load_only,
            dump_only=dump_only,
            unknown=unknown
        )

        self.file_name = schema_name + ".json"
        self.handler: StorageHandler = StorageHanlderFactory().get()

    def save_to_storage(self, object):
        self.handler.save(self.dumps(object), self.file_name)

    def loads_from_storage(self):
        return super().loads(self.handler.load(self.file_name))

    def loads_from_json(self, json: str):
        return super().loads(json)


class DateSchema(Schema):
    # 日付項目サブスキーマ
    date_time = fields.DateTime()
