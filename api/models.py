
from apistar import types, validators
import sqlalchemy

class Flight(types.Type):
    from_location = validators.String(max_length=100, min_length=3, allow_null=False)
    to_location = validators.String(max_length=100, min_length=3, allow_null=False)
    schedule = validators.Date()
