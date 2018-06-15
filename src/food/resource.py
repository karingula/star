from components import Organic, Backend

#views
class FoodResource():
    def eat_nicely(self, eatery: Organic=None) -> dict:
        print("Eat Nicely:",type(eatery))
        return {
        'my_eats': eatery.eats,
        'vacation': eatery.vacation
        }
    
    def eat_fancy(self, sample: Organic) -> str:
        print(type(sample))
        return "welcome to fancy eating"

    def backy(self, backend: Backend):
        print(backend.wealth)
        return "Backend testing"
    
    
