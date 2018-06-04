from apistar import Component
from intermediate import End
class Organic(object):

    def __init__(self, eats: dict):
        self.eats = eats


class OrganicComponent(Component):
    def resolve(self) -> Organic:
        """
        Determine the user associated with a request, using HTTP Basic Authentication.
        """
        eats = {'fruits': ['apple', 'mango', 'cherries', 'avacado'],
                'vegetables': ['carrots', 'bitter-melon', 'cucumbers', 'egg-plant']
        }
        
        return Organic(eats)


class Backend(End):
    def __init__(self, car, residence, vacation):
        super().__init__(car, residence, vacation)
        
class BackendComponent(Component):
    def get_car(self):
        return "Maserati"
    def get_home(self):
        return "Mansion"
    def get_vacation(self):
        return "St. Lucia"
    def resolve(self) ->Backend:
        car = self.get_car()
        residence = self.get_home()
        vacation = self.get_vacation()
        return Backend(car, residence, vacation)
