from components import Organic

#views
class FoodResource():
    def eat_nicely(self, eatery: Organic=None) -> dict:
        print(type(eatery))
        return {
        'my_eats': eatery.eats,
        }
    
    def eat_fancy(self, sample: Organic) -> str:
        print(type(sample))
        return "welcome to fancy eating"