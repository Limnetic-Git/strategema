import raylib
import random
from generate_map import MapGenerator
from units import *
from blocks import blocks_hp

class World:
    def __init__(self, world_size=256, seed=random.randint(0, 99999)):
        random.seed(seed)
        self.size = world_size
        self.seed = seed
        world_generator_object = MapGenerator(world_size, seed)

        self.world = world_generator_object.world
        self.world_objects = world_generator_object.world_objects
        self.block_size = 48
        
    def spawn_team(self, team_id: int, player):
        while True:
            rx, ry = random.randint(1, self.size-1), random.randint(1, self.size-1)
            if self.world[rx][ry] == 1 and self.world[rx+1][ry] == 1:
                break
        self.world_objects[rx][ry] = {'type': 'city', 'team': team_id, 'hp': blocks_hp['city']}
        if team_id == player.team:
            player.buildings.append((rx, ry))
        self.world_objects[rx+1][ry] = {'type': 'metal_cluster', 'hp': None}
        return rx, ry
    
    def spawn_teams(self, team_number: int, player):
        for i in range(team_number):
            bx, by = self.spawn_team(i, player)
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
                            
                            if camera.grid:
                                raylib.DrawRectangleLines(int(screen_x), int(screen_y), int(self.block_size), int(self.block_size), raylib.BLACK)
                            raylib.DrawRectangleRounded([int(screen_x) + 5, int(screen_y) + 5, int(self.block_size) - 10, int(self.block_size) - 10], 0.3, 10, (28, 28, 28, 35))
                    color = [raylib.RED, raylib.BLUE, raylib.PURPLE, raylib.YELLOW]
                    
                    if isinstance(loaded_map.load_world[x][y][1], dict):
                        if 'team' in loaded_map.load_world[x][y][1] and loaded_map.load_world[x][y][1]['type'] != 'field':
                            raylib.DrawTextureEx(tl[loaded_map.load_world[x][y][1]['type']], (screen_x, screen_y), 0, 1,
                                                 color[loaded_map.load_world[x][y][1]['team']])
                        else:
                            raylib.DrawTextureEx(tl[loaded_map.load_world[x][y][1]['type']], (screen_x, screen_y), 0, 1, raylib.WHITE)

                        
                    if loaded_map.now_loaded[x][y] == 1:
                        raylib.DrawRectangle(int(screen_x),
                            int(screen_y),
                            int(self.block_size),
                            int(self.block_size),
                            [50, 50, 50, 100])
                else:
                    raylib.DrawTextureEx(tl['fog'], (screen_x, screen_y), 0, 1, raylib.WHITE)
                    

