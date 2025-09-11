

class LoadedMap:
    def __init__(self, world):
        self.load_world = [[[None, None] for _ in range(world.size)] for _ in range(world.size)]
        self.now_loaded = [[1 for _ in range(world.size)] for _ in range(world.size)]
        
    def update(self, world):
        for x in range(world.size):
            for y in range(world.size):
                if self.now_loaded[x][y] == 0: self.now_loaded[x][y] = 1
    
    def load(self, world, x, y, r):
        bx, by = int(x // world.block_size), int(y // world.block_size)
        for i in [-1, 1]:
            for k in [-1, 1]:
                for j in range(r):
                    for u in range(r):
                        cx, cy = bx + (j*i), by + (u*k)
                        self.load_world[cx][cy] = [world.world[cx][cy], world.world_objects[cx][cy]]
                        self.now_loaded[cx][cy] = 0