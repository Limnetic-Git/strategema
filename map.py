import raylib
import random
from generate_map import MapGenerator
from units import *


class World:
    def __init__(self, world_size=256, seed=random.randint(0, 99999)):
        random.seed(seed)
        self.size = world_size
        self.seed = seed
        world_generator_object = MapGenerator(world_size, seed)

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
    
    def spawn_teams(self, team_number: int, player):
        for i in range(team_number):
            bx, by = self.spawn_team(i)
            if i == player.team: player.capital_cords = [bx, by]
            
    def update(self, client_socket):
        for change in client_socket.world_changes:
            self.world_objects[change['x']][change['y']] = change['building']
            client_socket.world_changes.remove(change)
            
    def draw(self, window, tl, camera, loaded_map):
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
                if loaded_map.load_world[x][y] != [None, None]:
                    if -self.block_size < screen_x < window.width and -self.block_size < screen_y < window.height:
                        if loaded_map.load_world[x][y][0] == 1:
                            raylib.DrawRectangle(int(screen_x),
                                                int(screen_y),
                                                int(self.block_size),
                                                int(self.block_size),
                                                raylib.GREEN
                                                )
                            raylib.DrawRectangleLines(int(screen_x), int(screen_y), int(self.block_size), int(self.block_size), raylib.BLACK)
                            
                    if loaded_map.load_world[x][y][1] == 1:
                        raylib.DrawTextureEx(tl['tree'], (screen_x, screen_y), 0, 1, raylib.WHITE)
                    if loaded_map.load_world[x][y][1] == 2:
                        raylib.DrawTextureEx(tl['metal_cluster'], (screen_x, screen_y), 0, 1, raylib.WHITE)
                    if loaded_map.load_world[x][y][1] == 3:
                        raylib.DrawTextureEx(tl['water_metal_cluster'], (screen_x, screen_y), 0, 1, raylib.WHITE)
                    if loaded_map.load_world[x][y][1] == 4:
                        raylib.DrawTextureEx(tl['new_city'], (screen_x, screen_y), 0, 1, raylib.RED)
                    if loaded_map.load_world[x][y][1] == 5:
                        raylib.DrawTextureEx(tl['new_city'], (screen_x, screen_y), 0, 1, raylib.BLUE)
                    if loaded_map.load_world[x][y][1] == 6:
                        raylib.DrawTextureEx(tl['new_city'], (screen_x, screen_y), 0, 1, raylib.PURPLE)
                    if loaded_map.load_world[x][y][1] == 7:
                        raylib.DrawTextureEx(tl['new_city'], (screen_x, screen_y), 0, 1, raylib.YELLOW)
                        
                    if loaded_map.now_loaded[x][y] == 1:
                        raylib.DrawRectangle(int(screen_x),
                            int(screen_y),
                            int(self.block_size),
                            int(self.block_size),
                            [50, 50, 50, 100])
                else:
                    raylib.DrawTextureEx(tl['fog'], (screen_x, screen_y), 0, 1, raylib.WHITE)
                    

