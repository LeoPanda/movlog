from marshmallow import Schema, fields
from server.model.metaSchema import MetaSchema
import re


class LatLngSchema(Schema):
    # 位置情報
    lat = fields.Str()
    lng = fields.Str()


class LocationSchema(MetaSchema):
   # google map place items
    place_id = fields.Str()
    name = fields.Str()
    location = fields.Nested(LatLngSchema())
    photo_url = fields.Str()


def get_photo_url(self, size=300):
    return re.sub(r'\d$', size, self.photo_url)
