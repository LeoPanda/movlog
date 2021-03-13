from google.cloud import storage
from abc import ABCMeta, abstractclassmethod
from server import config
from google.api_core.exceptions import NotFound
# Storage Handler 生成ファクトリ
# 本番環境ではgoogle storage、開発環境ではローカルファイルシステムを
# 使用するようストレージのハンドラを自動生成する。
#
# google storageの制約により、アップロードするオブジェクトはjson形式にする必要がある。


class StorageHandler(metaclass=ABCMeta):
    # storage object handler abstract class
    json_object: str

    @abstractclassmethod
    def save(self, object, file_name: str):
        pass

    @abstractclassmethod
    def load(self, file_name: str) -> str:
        return self.json_object


class StorageHanlderFactory():
    # storage handler creator
    storage_handler: StorageHandler

    def __init__(self):

        if config.IS_DEVELOPMENT:
            self.storage_handler = LocalStorageHandler()
        else:
            self.storage_handler = GoogleStorageHandler()

    def get(self):
        return self.storage_handler


class LocalStorageHandler(StorageHandler):
    # local storage handler class

    def __init__(self):
        if config.STORAGE_LOCATION is None:
            raise NameError('Storage location not defined.')

    def save(self, source, file_name):
        with open(self.get_file_locate(file_name), mode="w", encoding='utf_8') as f:
            f.write(source)

    def load(self, file_name: str) -> str:
        try:
            with open(self.get_file_locate(file_name), mode="r") as f:
                self.json_object = f.read()
        except FileNotFoundError:
            return "[]"

        return self.json_object

    def get_file_locate(self, file_name: str) -> str:
        return config.STORAGE_LOCATION + file_name


class GoogleStorageHandler(StorageHandler):
    # google storage handler class

    def __init__(self):
        self.client = storage.Client()
        self.bucket = self.client.bucket(config.BUCKET_NAME)

    def save(self, source, file_name):
        blob = self.get_blob(file_name)
        blob.upload_from_string(source, content_type="application/json")

    def load(self, file_name: str) -> str:
        blob = self.get_blob(file_name)
        try:
            self.json_object = blob.download_as_string().decode("utf-8")
        except NotFound:
            return "[]"
        return self.json_object

    def get_blob(self, file_name):
        return self.bucket.blob(file_name)
