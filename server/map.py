import random
from generate_map import MapGenerator
from units import Scout


class World:
    def __init__(self, world_size=256, seed=random.randint(0, 99999)):
        random.seed(seed)
        self.size = world_size
        self.seed = seed
        world_generator_object = MapGenerator(world_size, seed)
        print('OK')
        self.world = world_generator_object.world
        self.world_objects = world_generator_object.world_objects
        self.block_size = 48
        
    def spawn_team(self, team_id: int):
        while True:
            rx, ry = random.randint(1, self.size-1), random.randint(1, self.size-1)
            if self.world[rx][ry] == 1 and self.world[rx+1][ry] == 1:
                break
        self.world_objects[rx][ry] = team_id + 4
        self.world_objects[rx+1][ry] = 2
        return rx, ry
    
    def spawn_teams(self, team_number: int, units_list):
        for i in range(team_number):
            bx, by = self.spawn_team(i)
            units_list.add(Scout(bx*48, by*48, i, units_list))



