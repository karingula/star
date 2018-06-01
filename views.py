from components import Organic

#views
def eat_nicely(eatery: Organic=None) -> dict:
    return {
        'my_eats': eatery.eats,
    }

def eat_fancy(sample: Organic):
    print(type(sample))
    return "welcome to fancy eating"