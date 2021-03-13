from marshmallow import fields
from server.model.metaSchema import MetaSchema


class TablesSchema(MetaSchema):
   # keyword
    keywords = fields.List(fields.String)
    screenTypes = fields.List(fields.String)
    providers = fields.List(fields.String)
