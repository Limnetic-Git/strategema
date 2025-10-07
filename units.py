import raylib

class UnitsList:
    def __init__(self):
        self.units_list = []
        self.selected_units_ids = []
        
    def draw_all(self, camera, tl, loaded_map):
        for unit in self.units_list:
            unit.draw(camera, tl, loaded_map)
            
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

    def draw(self, camera, tl, loaded_map):
        color = [raylib.RED, raylib.BLUE, raylib.PURPLE, raylib.YELLOW]
        bx, by = int(self.x // 48), int(self.y // 48)

        if (0 <= bx < len(loaded_map.now_loaded) and 0 <= by < len(loaded_map.now_loaded[0])):
            if loaded_map.now_loaded[bx][by] == 0:
                screen_x = round((self.x - camera.pos[0]) * camera.zoom)
                screen_y = round((self.y - camera.pos[1]) * camera.zoom)
                
                if self.name == 'Scout':
                    offset_x = round(6 * camera.zoom)
                    offset_y = round(8 * camera.zoom)
                    
                    raylib.DrawTextureEx(tl['scout'], 
                                       (screen_x - offset_x, 
                                        screen_y - offset_y), 
                                       0, 1.5 * camera.zoom, color[self.team])
                    
                    if self.selected:
                        for _ in range(2):
                            selection_size = round(24 * camera.zoom)
                            selection_offset = round(8 * camera.zoom)
                            if self.team != 3:
                                raylib.DrawRectangleLines(screen_x - selection_offset, 
                                                        screen_y - selection_offset,
                                                        selection_size, 
                                                        selection_size + round(2 * camera.zoom), raylib.YELLOW)
                            else:
                                raylib.DrawRectangleLines(screen_x - selection_offset, 
                                                        screen_y - selection_offset,
                                                        selection_size, 
                                                        selection_size + round(2 * camera.zoom), raylib.BLACK)
