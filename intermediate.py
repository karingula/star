#consider this as a utility file

from abc import abstractmethod

class End(object):
    def __init__(self, car, residence, vacation):
        self.car = car
        self.residence = residence
        self.vacation = vacation