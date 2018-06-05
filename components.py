from apistar import Component
from intermediate import End

class Backend(End):
    def __init__(self, wealth):
        super().__init__(wealth)
        
class BackendComponent(Component):
    def get_car(self):
        return "Maserati"
    def get_home(self):
        return "Mansion"
    def get_vacation(self):
        return "St. Lucia"
    def resolve(self) ->Backend:
        wealth = {
            'car': self.get_car(),
            'residence': self.get_home(),
            'vacation': self.get_vacation()
        }
        return Backend(wealth)

class Organic(object):
    
    def __init__(self, eats: dict):
        self.eats = eats
        self.vacation = vacation

class OrganicComponent(Component):
    def resolve(self, backend: Backend) -> Organic:
        """
        Determine the user associated with a request, using HTTP Basic Authentication.
        """
        vacation = backend.wealth['vacation']
        eats = {'fruits': ['apple', 'mango', 'cherries', 'avacado'],
                'vegetables': ['carrots', 'bitter-melon', 'cucumbers', 'egg-plant']
        }
        
        return Organic(eats, vacation)
