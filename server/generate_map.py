import math, random
from blocks import blocks_hp

def neibs(world, x, y):
    a = 0
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if dx == 0 and dy == 0: pass
            else:
                nx, ny = x + dx, y + dy
                if 0 <= nx < len(world) and 0 <= ny < len(world[0]):
                    if world[nx][ny] != world[x][y]: a += 1
    return a

def most_common_element(arr):
    if not arr: return None
    frequency = {}
    for num in arr:
        frequency[num] = frequency.get(num, 0) + 1
    return max(frequency.items(), key=lambda x: x[1])[0]

class MapGenerator:
    def __init__(self, world_size, seed):
        self.size = world_size
        self.seed = seed
        self.world = [[0 for _ in range(self.size)] for _ in range(self.size)]
        self.world_objects = [[0 for _ in range(self.size)] for _ in range(self.size)]
        self.biom_clusters = []
        self.bioms_cout = 6
        self.__generate_world()
        
    def __generate_world(self):
        random.seed(self.seed)
        self.__generate_template()
        self.__cut_edges()
        for _ in range(16):
            self.__smoothing()
        self.__generate_bioms()
        for _ in range(self.size):
            self.__biom_grow_tick()
        self.__generate_rivers()
        self.__reset_bioms()
        for _ in range(2):
            self.__scale_water()
        for _ in range(8):
            self.__smoothing()
        self.__generate_trees()
        self.__generate_metal_clusters()
        
    def __generate_template(self):
        center_x, center_y = self.size // 2, self.size // 2
        for x in range(self.size):
            for y in range(self.size):
                dist = math.hypot(x - center_x, y - center_y) 
                if random.randint(0, 1000) <= 1000 - dist*5:
                    self.world[x][y] = 1
                      
    def __reset_bioms(self):
        for x in range(self.size):
            for y in range(self.size):
                if self.world[x][y] > 1:
                     self.world[x][y] = 1
                     
    def __scale_water(self):
        step_world = eval(str(self.world))
        for x in range(self.size):
            for y in range(self.size):
                if self.world[x][y] == 1:
                    near = [self.world[x + 1][y], self.world[x - 1][y], self.world[x][y + 1], self.world[x][y - 1]]
                    if 0 in near:
                        step_world[x][y] = 0
        self.world = step_world
                
    def __smoothing(self):
        step_world = [[0 for _ in range(self.size)] for _ in range(self.size)]
        for x in range(self.size):
            for y in range(self.size):
                step_world[x][y] = neibs(self.world, x, y)
        for x in range(self.size):
            for y in range(self.size):
                if step_world[x][y] >= 5:
                    self.world[x][y] = (0 if self.world[x][y] == 1 else 1)
        
    def __cut_edges(self):
        for i in range(self.size):
            for w in range(6):
                self.world[i][0+w] = 0
                self.world[0+w][i] = 0
                self.world[-1-w][i] = 0
                self.world[i][-1-w] = 0
    
    def __generate_rivers(self):
        step_world = eval(str(self.world))
        for x in range(self.size):
            for y in range(self.size):
                if step_world[x][y] > 1:
                    near = [step_world[x + 1][y], step_world[x - 1][y], step_world[x][y + 1], step_world[x][y - 1]]
                    if max(near) != step_world[x][y]:
                        self.world[x][y] = 0

    def __generate_bioms(self):
        for i in range(self.bioms_cout):
            rx, ry = random.randint(0, self.size - 1), random.randint(0, self.size - 1)
            while self.world[rx][ry] != 1: rx, ry = random.randint(0, self.size - 1), random.randint(0, self.size - 1)
            self.world[rx][ry] = i + 2
            self.biom_clusters.append([[rx, ry]])
            
    def __biom_grow_tick(self):
        for c in range(len(self.biom_clusters)):
            cluster = self.biom_clusters[c]
            for i in range(len(cluster)):
                try:
                    near = [self.world[cluster[i][0] + 1][cluster[i][1]], self.world[cluster[i][0] - 1][cluster[i][1]], self.world[cluster[i][0]][cluster[i][1] + 1], self.world[cluster[i][0]][cluster[i][1] - 1]]
                    near_coors = [[cluster[i][0] + 1, cluster[i][1]], [cluster[i][0] - 1, cluster[i][1]], [cluster[i][0], cluster[i][1] + 1], [cluster[i][0], cluster[i][1] - 1]]
                    if 1 in near:
                        r = random.randint(0, 3)
                        while near[r] != 1: r = random.randint(0, 3)
                        cluster.append(near_coors[r])
                        self.world[near_coors[r][0]][near_coors[r][1]] = c + 2
                    else: self.biom_clusters[c].pop(i)
                except IndexError: pass
                
    def __generate_trees(self):
        for x in range(self.size):
            for y in range(self.size):
                if self.world[x][y] == 1:
                    if random.randint(1, 100) <= 6:
                        self.world_objects[x][y] = {'type': 'tree', 'hp': blocks_hp['tree']}
                        
    def __generate_metal_clusters(self):
        for _ in range(random.randint(5, 6)):
            rx, ry = random.randint(0, self.size  - 1), random.randint(0, self.size  - 1)
            if self.world[rx][ry] == 1:
                self.world_objects[rx][ry] = {'type': 'metal cluster', 'hp': None}
            else:
                self.world_objects[rx][ry] = {'type': 'water metal cluster', 'hp': None}
                