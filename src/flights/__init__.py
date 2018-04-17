#Flight Resource __init__


__routes__ = []
__route_name__ = 'flights'

from apistar import Route
from ...lib.loader import Loader
#Load and expose all the classes
loader = Loader(globals())

#resources
_fr = FlightResource()

__routes__ = [
    Route('/flights', method='GET', handler=_fr.get_flight_details),
    Route('/flight/add', method='POST' , handler=_fr.add_flight),
]


