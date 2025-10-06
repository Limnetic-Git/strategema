
class Player:
    
    @staticmethod
    def fill_rect(array, x, y, size, fill_in):
        bx, by = x, y
        for i in [-1, 1]:
            for k in [-1, 1]:
                for j in range(size):
                    for u in range(size):
                        cx, cy = bx + (j*i), by + (u*k)
                        array[cx][cy] = fill_in

    def __init__(self, team):
        self.team = team
        self.capital_cords = [None, None]
        self.food = 0
        self.iron = 1
        self.oil = 0
        
        self.food_speed = 0
        self.iron_speed = 0
        
        self.buildings = []
        
        self.load_zone = [[[None, None] for _ in range(256)] for _ in range(256)]
        #self.fog = [[1 for _ in range(256)] for _ in range(256)]
        self.city_borders = [[0 for _ in range(256)] for _ in range(256)]
    

    
    def update_buildings_info(self, world):
        self.food_speed = 0.33
        self.iron_speed = 0.33
        self.city_borders = [[0 for _ in range(256)] for _ in range(256)]
        for building in self.buildings:
            if isinstance(world.world_objects[building[0]][building[1]], dict):
                if 'team' in world.world_objects[building[0]][building[1]]:
                    if world.world_objects[building[0]][building[1]]['team'] == self.team:
                        if world.world_objects[building[0]][building[1]]['type'] == 'field':
                            self.food_speed += 0.15
                        elif world.world_objects[building[0]][building[1]]['type'] == 'mine':
                            self.iron_speed += 0.35
                        elif world.world_objects[building[0]][building[1]]['type'] == 'city':
                            self.fill_rect(self.city_borders, building[0], building[1], 6, 2)
                            self.fill_rect(self.city_borders, building[0], building[1], 4, 1)
                            
    def update_resources(self):
        self.food += self.food_speed
        self.iron += self.iron_speed
