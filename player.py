
class Player:
    def __init__(self, team):
        self.team = team
        self.capital_cords = [None, None]
        self.food = 0
        self.iron = 1
        self.oil = 0
        
        self.load_zone = [[[None, None] for _ in range(256)] for _ in range(256)]
        self.fog = [[1 for _ in range(256)] for _ in range(256)]
    
    def fog_update(self):
        for x in range(256):
            for y in range(256):
                if self.fog[x][y] == 0: self.fog[x][y] = 1
        
