from apistar import Component
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

