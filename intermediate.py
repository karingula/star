#consider this as a utility file

from abc import abstractmethod

class End(object):
    def __init__(self, wealth):
        self.wealth = wealth