#Flight Resource __init__

__routes__ = []
__route_name__ = 'food'

from apistar import Route
from ...lib.loader import Loader
#Load and expose all the classes
loader = Loader(globals())

#resources
_fo = FoodResource()

__routes__ = [
    Route('/food/organic/', method='GET', handler=_fo.eat_nicely),
    Route('/food/fancy/', method='GET', handler=_fo.eat_fancy),
    Route('/food/back/', method='GET', handler=_fo.backy)
]


