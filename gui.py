import raylib
from blocks import blocks_hp
from buildings import buildings_cost

class ActionButton:
    def __init__(self, x, y, type_, action, tl):
        self.x = x
        self.y = y
        self.type = type_
        self.texture = tl[type_]
        self.action = action
        self.is_mouse_on = False
        
    def draw(self, action_bar, player, camera):
        raylib.DrawTextureEx(self.texture, (self.x, self.y), 0, 1, raylib.WHITE)
        self.__update(player, action_bar, camera)
        
    def draw_info_bar(self, player, action_bar, camera):
        action_bar.action_bar_y = 780
        
    def __update(self, player, action_bar, camera):
        xm, ym = raylib.GetMouseX(), raylib.GetMouseY()
        if xm >= self.x and xm <= self.x + self.texture.width and ym >= self.y and ym <= self.y + self.texture.height:
            self.is_mouse_on = True
            if raylib.IsMouseButtonPressed(raylib.MOUSE_BUTTON_LEFT):
                if self.action == 0: action_bar.page = 1
                elif self.action == 4: action_bar.page = 0
                elif self.action == 1: action_bar.page = 2
                elif self.action == 5: camera.current_building = {'type': 'city', 'team': player.team, 'hp': blocks_hp['city']}
                elif self.action == 6: camera.current_building = {'type': 'mine', 'team': player.team, 'hp': blocks_hp['mine']}
                elif self.action == 7: camera.current_building = {'type': 'field', 'team': player.team, 'hp': blocks_hp['field']}
                else: print('WORK IN PROGRESS')
            if self.action >= 5:
                self.draw_info_bar(player, action_bar, camera)
        else:
            self.is_mouse_on = False
class ActionBar:
    def __init__(self, tl):
        self.action_bar_y = 860
        self.page = 0
        self.pages_info = [
            [ActionButton(65, 900, 'new_city', 0, tl), # <--- ГЛАВНАЯ СТРАНИЦА (0)
             ActionButton(135, 900, 'factory', 1, tl),
             ActionButton(205, 900, 'sword', 2, tl),
             ActionButton(275, 900, 'research', 3, tl),
            ],
            
            [ActionButton(65, 900, 'undo', 4, tl),  # <---  МИРНЫЕ ЗДАНИЯ (1)
             ActionButton(135, 900, 'city', 5, tl),
             ActionButton(205, 900, 'field', 7, tl),
            ],
            
            [ActionButton(65, 900, 'undo', 4, tl), # <--- ЗАВОДСКИЕ ЗДАНИЯ (2)
             ActionButton(135, 900, 'mine', 6, tl),
            ],
                                  ]
    
    def draw(self, player, camera, tl):
        raylib.DrawRectangleRounded([15, self.action_bar_y - 10, 500, 280], 0.3, 10, (28, 28, 28, 200))
    
        raylib.DrawRectangleRounded([25, self.action_bar_y, 480, 280], 0.25, 10, (28, 28, 28, 255))

        for button in self.pages_info[self.page]:
            button.draw(self, player, camera)
        
        for button in self.pages_info[self.page]:
            if button.is_mouse_on:
                if button.action >= 5:
                    raylib.DrawTextureEx(tl['iron'], (135, 785), 0, 0.75, raylib.WHITE)
                    raylib.DrawTextureEx(tl['apple'], (135, 835), 0, 0.75, raylib.WHITE)
                    raylib.DrawTextureEx(tl[button.type], (50, 800), 0, 1.5, raylib.WHITE)
                    
                    iron_color = (raylib.WHITE if player.iron >= buildings_cost[button.type][0] else raylib.RED)
                    food_color = (raylib.WHITE if player.food >= buildings_cost[button.type][1] else raylib.RED)
                    raylib.DrawText(str(buildings_cost[button.type][0]).encode(), 185, 800, 25, iron_color)
                    raylib.DrawText(str(buildings_cost[button.type][1]).encode(), 185, 850, 25, food_color)
                    
                    
                break
        else: self.action_bar_y = 860
            
            
        
class RecoursesBar:
    def __init__(self):
        pass
    
    def draw(self, tl, player):
        raylib.DrawRectangleRounded([1250 + 95, 10, 245, 64], 0.25, 10, (28, 28, 28, 255))
        
        raylib.DrawRectangleRounded([1243 + 95, 3, 259, 78], 0.3, 10, (28, 28, 28, 200))
        raylib.DrawTextureEx(tl['iron'], (1255 + 95, 20), 0, 1, raylib.WHITE)
        raylib.DrawTextureEx(tl['apple'], (1255 + 215, 20), 0, 1, raylib.WHITE)
        
        raylib.DrawText(str(int(player.iron)).encode(), 1255 + 95 + 52, 20, 36, raylib.WHITE)
        raylib.DrawText(str(int(player.food)).encode(), 1255 + 200 + 67, 20, 36, raylib.WHITE)
        raylib.DrawText((str(round(player.iron_speed, 2))+'/s').encode(), 1255 + 95 + 58, 55, 20, raylib.WHITE)
        raylib.DrawText((str(round(player.food_speed, 2))+'/s').encode(), 1255 + 200 + 73, 55, 20, raylib.WHITE)
        
class DebugInfoBar:
    def __init__(self):
        pass
    
    def draw(self, client_socket):
        current_fps = raylib.GetFPS()
        raylib.DrawText(str(current_fps).encode(), 3, 3, 20, raylib.WHITE)
        raylib.DrawText(str(client_socket.tcp_ping).encode(), 3, 25, 20, raylib.WHITE)
        raylib.DrawText(str(client_socket.udp_ping).encode(), 3, 47, 20, raylib.WHITE)
        