import math
import random

class Player:
    def __init__(self, team):
        self.team = team
        self.capital_cords = [None, None]
        self.food = 0
        self.iron = 0
        self.oil = 0
        