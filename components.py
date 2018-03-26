from apistar import typesystem
import service
# Flight Component

class FlightComponent(object):
    properties = {
        'flight_id': typesystem.integer(),
        'from_location': typesystem.string(max_length=100),
        'to_location': typesystem.string(max_length=100),
        'schedule': service.date(),
    }
