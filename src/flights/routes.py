from .resource import FlightResource
from apistar import Route, Include
__routes__ = []
_fr = FlightResource()

__routes__ = [
    Route('/flights', method='GET', handler=_fr.get_flight_details),
    Route('/flight/add', method='POST' , handler=_fr.add_flight),
]
