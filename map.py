import raylib
import random
from generate_map import MapGenerator


class World:
    def __init__(self, world_size=200, seed=random.randint(0, 99999)):
        self.size = world_size
        self.seed = seed
        world_generator_object = MapGenerator(world_size, seed)

        self.world = world_generator_object.world
        self.world_objects = world_generator_object.world_objects
        self.block_size = 48
        
        self.world_objects[100][100] = 4


    def draw(self, window, tl, camera):
        raylib.BeginDrawing()
        raylib.ClearBackground(raylib.BLUE)

        start_x = max(0, int(camera.pos[0] / self.block_size))
        start_y = max(0, int(camera.pos[1] / self.block_size))
        end_x = min(self.size, start_x + int(window.width / self.block_size) + 2)
        end_y = min(self.size, start_y + int(window.height / self.block_size) + 2)

        for x in range(start_x, end_x):
            for y in range(start_y, end_y):
                
                    screen_x = x * self.block_size - camera.pos[0]
                    screen_y = y * self.block_size - camera.pos[1]
                    if -self.block_size < screen_x < window.width and -self.block_size < screen_y < window.height:
                        if self.world[x][y] == 1:
                            raylib.DrawRectangle(int(screen_x),
                                                int(screen_y),
                                                int(self.block_size),
                                                int(self.block_size),
                                                raylib.GREEN
                                                )
                            raylib.DrawRectangleLines(int(screen_x), int(screen_y), int(self.block_size), int(self.block_size), raylib.BLACK)
                            
                    if self.world_objects[x][y] == 1:
                        raylib.DrawTextureEx(tl['tree'], (screen_x, screen_y), 0, 1, raylib.WHITE)
                    if self.world_objects[x][y] == 2:
                        raylib.DrawTextureEx(tl['metal_cluster'], (screen_x, screen_y), 0, 1, raylib.WHITE)
                    if self.world_objects[x][y] == 3:
                        raylib.DrawTextureEx(tl['water_metal_cluster'], (screen_x, screen_y), 0, 1, raylib.WHITE)
                    if self.world_objects[x][y] == 4:
                        raylib.DrawTextureEx(tl['city'], (screen_x, screen_y), 0, 1, raylib.RED)


