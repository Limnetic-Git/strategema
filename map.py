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
            
    def draw(self, window, tl, camera, loaded_map, player):
        raylib.BeginDrawing()
        raylib.ClearBackground(raylib.BLUE)

        start_x = max(0, int(camera.pos[0] / self.block_size))
        start_y = max(0, int(camera.pos[1] / self.block_size))
        visible_blocks_x = int(window.width / (self.block_size * camera.zoom)) + 4
        visible_blocks_y = int(window.height / (self.block_size * camera.zoom)) + 4
        end_x = min(self.size, start_x + visible_blocks_x)
        end_y = min(self.size, start_y + visible_blocks_y)

        for x in range(start_x, end_x):
            for y in range(start_y, end_y):

                screen_x = round((x * self.block_size - camera.pos[0]) * camera.zoom)
                screen_y = round((y * self.block_size - camera.pos[1]) * camera.zoom)

                scaled_block_size = round(self.block_size * camera.zoom) + 1
                
                if (-scaled_block_size < screen_x < window.width + scaled_block_size and 
                    -scaled_block_size < screen_y < window.height + scaled_block_size):
                    
                    if loaded_map.load_world[x][y] != [None, None]:
                        if loaded_map.load_world[x][y][0] == 1:
                            raylib.DrawRectangle(screen_x,
                                                screen_y,
                                                scaled_block_size,
                                                scaled_block_size,
                                                raylib.GREEN
                                                )
                            
                            if camera.grid:
                                grid_size = round(self.block_size * camera.zoom)
                                raylib.DrawRectangleLines(screen_x, 
                                                        screen_y, 
                                                        grid_size, 
                                                        grid_size, raylib.BLACK)
                                
                            raylib.DrawRectangleRounded([screen_x + 5, 
                                                       screen_y + 5, 
                                                       scaled_block_size - 10, 
                                                       scaled_block_size - 10], 0.3, 10, (28, 28, 28, 35))
                        
                        elif loaded_map.load_world[x][y][0] == 0:  # вода
                            raylib.DrawRectangle(screen_x,
                                                screen_y,
                                                scaled_block_size,
                                                scaled_block_size,
                                                raylib.BLUE
                                                )
                        
                        color = [raylib.RED, raylib.BLUE, raylib.PURPLE, raylib.YELLOW]
                        
                        if isinstance(loaded_map.load_world[x][y][1], dict):
                            if 'team' in loaded_map.load_world[x][y][1] and loaded_map.load_world[x][y][1]['type'] != 'field':
                                texture_size = round(self.block_size * camera.zoom) + 1
                                texture_scale = (self.block_size * camera.zoom + 1) / (self.block_size * camera.zoom)
                                raylib.DrawTextureEx(tl[loaded_map.load_world[x][y][1]['type']], 
                                                   (screen_x, screen_y), 
                                                   0, camera.zoom * texture_scale,
                                                   color[loaded_map.load_world[x][y][1]['team']])
                            else:
                                texture_scale = (self.block_size * camera.zoom + 1) / (self.block_size * camera.zoom)
                                raylib.DrawTextureEx(tl[loaded_map.load_world[x][y][1]['type']], 
                                                   (screen_x, screen_y), 
                                                   0, camera.zoom * texture_scale, raylib.WHITE)

                            
                        if loaded_map.now_loaded[x][y] == 1:
                            raylib.DrawRectangle(screen_x,
                                screen_y,
                                scaled_block_size,
                                scaled_block_size,
                                [50, 50, 50, 100])
                        if isinstance(camera.current_building, dict):
                            if self.world[x][y] == 1:
                                if self.world_objects[x][y] == 0:
                                    if player.city_borders[x][y] == 1 and camera.current_building['type'] != 'city' or \
                                       player.city_borders[x][y] == 2 and camera.current_building['type'] == 'city':
                                        
                                        raylib.DrawRectangle(screen_x,
                                            screen_y,
                                            scaled_block_size,
                                            scaled_block_size,
                                            [190, 255, 50, 120])
                                elif isinstance(self.world_objects[x][y], dict):
                                    if self.world_objects[x][y]['type'] == 'metal_cluster' and camera.current_building['type'] == 'mine':
                                        raylib.DrawRectangle(screen_x,
                                            screen_y,
                                            scaled_block_size,
                                            scaled_block_size,
                                            [190, 255, 50, 120])
                    else:
                        fog_size = round(self.block_size * camera.zoom) + 1
                        fog_scale = (self.block_size * camera.zoom + 1) / (self.block_size * camera.zoom)
                        raylib.DrawTextureEx(tl['fog'], 
                                           (screen_x, screen_y), 
                                           0, camera.zoom * fog_scale, raylib.WHITE)
