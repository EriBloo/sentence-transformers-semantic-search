from marshmallow import Schema, fields

class DatasetSchema(Schema):
    id = fields.String(required=True)
    name = fields.String(required=True)
    
class DatasetsSchema(Schema):
    datasets = fields.List(fields.Nested(DatasetSchema), required=True)

class IdsSchema(Schema):
    ids = fields.List(fields.String(), required=True)