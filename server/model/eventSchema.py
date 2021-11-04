from marshmallow import Schema, fields
from server.model.metaSchema import MetaSchema, DateSchema
from datetime import datetime


class OuterSite(Schema):
    # 外部データソースサイト
    imdb = fields.Str()
    eiga_db = fields.Str()
    tmdb = fields.Str()


class CalendarSchema(MetaSchema):
   # google calendar items
    id = fields.Str()
    html_link = fields.Str()
    summary = fields.Str()
    location = fields.Str()
    start = fields.Nested(DateSchema())

    def get_start_date(self, event):
        # 開始日時を得る
        return event.get("start").get("date_time")

    def get_sorted_by_latest(self, events: list):
        # event listを最新日付順にソートする
        return sorted(events, reverse=True, key=lambda item: self.get_start_date(item))

    def get_time_max(self, events: list):
        # event listから最新イベントの日付を得る
        # google calendar apiの query key とするため、gae用の日付フォーマットに変換する
        if len(events) > 0:
            sorted = self.get_sorted_by_latest(events)
            time_max = datetime.strftime(
                self.get_start_date(sorted[0]), "%Y-%m-%dT%H:%M:%S%z")
        else:
            time_max = None
        return time_max


class EventsSchema(CalendarSchema):
    # メインスキーマ
    outer_id = fields.Nested(OuterSite())
    outer_rate = fields.Nested(OuterSite())
    my_rate = fields.Float()
    title_img = fields.Str()
    img_src = fields.Nested(OuterSite())
    outline = fields.Str()
    title = fields.Str()
    en_title = fields.Str()
    is_domestic = fields.Boolean()
    on_tv = fields.Boolean()
    streaming_provider = fields.Str()
    screen_type = fields.List(fields.Str())
