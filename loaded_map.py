

class LoadedMap:
    def __init__(self, world):
        self.load_world = [[[None, None] for _ in range(world.size)] for _ in range(world.size)]
        self.now_loaded = [[1 for _ in range(world.size)] for _ in range(world.size)]
        
    def update(self, world):
        for x in range(world.size):
            for y in range(world.size):
                if self.now_loaded[x][y] == 0: self.now_loaded[x][y] = 1