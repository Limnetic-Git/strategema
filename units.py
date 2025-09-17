import raylib
import random
import math

class UnitsList:
    def __init__(self):
        self.units_list = []
        self.selected_units_ids = []
        
    def draw_all(self, camera, tl, world, loaded_map, player):
        for unit in self.units_list:
            unit.draw(camera, tl, world, loaded_map, player)
            
    def update_world_load(self, world, player, loaded_map):
        for unit in self.units_list:
            if unit.team == player.team:
                loaded_map.load(world, unit.x, unit.y, 5)
                
    def update(self, units_dict):
        self.units_list = []
        for unit in units_dict:
            self.units_list.append(Unit(unit['id'], unit['x'], unit['y'], unit['team'], unit['name'], unit['hp']))
            if unit['id'] in self.selected_units_ids:
                self.units_list[-1].selected = True
            
class Unit:
    def __init__(self, id, x, y, team, name, hp):
        self.id = id
        self.x = x
        self.y = y
        self.team = team
        self.name = name
        self.hp = hp
        
        self.selected = False

    def draw(self, camera, tl, world, loaded_map, player):
        color = [raylib.RED, raylib.BLUE, raylib.PURPLE, raylib.YELLOW]
        bx, by = self.x // 48, self.y // 48
            
        if loaded_map.now_loaded[bx][by] == 0:
            if self.name == 'Scout':
                raylib.DrawTextureEx(tl['scout'], (self.x - camera.pos[0] - 6, self.y - camera.pos[1] - 8), 0, 1.5, color[self.team])
                #raylib.DrawCircle(self.x - camera.pos[0], self.y - camera.pos[1], 10, color[self.team])
                if self.selected:
                    for i in range(2):
                        if self.team != 3:
                            raylib.DrawRectangleLines(int(self.x - camera.pos[0] - 8), int(self.y - camera.pos[1] - 9),
                                                                                int(24), int(26), raylib.YELLOW)
                        else:
                            raylib.DrawRectangleLines(int(self.x - camera.pos[0] - 8), int(self.y - camera.pos[1] - 9),
                                                                                int(24), int(26), raylib.BLACK)

        