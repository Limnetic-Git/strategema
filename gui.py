import raylib
from blocks import blocks_hp

class ActionButton:
    def __init__(self, x, y, texture, action):
        self.x = x
        self.y = y
        self.texture = texture
        self.action = action
        
    def draw(self, action_bar, player, camera):
        raylib.DrawTextureEx(self.texture, (self.x, self.y), 0, 1, raylib.WHITE)
        self.__check_press(player, action_bar, camera)
        
    def __check_press(self, player, action_bar, camera):
        if raylib.IsMouseButtonPressed(raylib.MOUSE_BUTTON_LEFT):
            xm, ym = raylib.GetMouseX(), raylib.GetMouseY()
            if xm >= self.x and xm <= self.x + self.texture.width and ym >= self.y and ym <= self.y + self.texture.height:
                if self.action == 0: action_bar.page = 1
                elif self.action == 4: action_bar.page = 0
                elif self.action == 1: action_bar.page = 2
                elif self.action == 5: camera.current_building = {'type': 'city', 'team': player.team, 'hp': blocks_hp['city']}
                elif self.action == 6: camera.current_building = {'type': 'mine', 'team': player.team, 'hp': blocks_hp['mine']}
                elif self.action == 7: camera.current_building = {'type': 'field', 'team': player.team, 'hp': blocks_hp['field']}
                else: print('WORK IN PROGRESS')
                
class ActionBar:
    def __init__(self, tl):
        self.page = 0
        self.pages_info = [
            [ActionButton(65, 900, tl['new_city'], 0), # <--- ГЛАВНАЯ СТРАНИЦА (0)
             ActionButton(135, 900, tl['factory'], 1),
             ActionButton(205, 900, tl['sword'], 2),
             ActionButton(275, 900, tl['research'], 3),
            ],
            
            [ActionButton(65, 900, tl['undo'], 4),  # <---  МИРНЫЕ ЗДАНИЯ (1)
             ActionButton(135, 900, tl['city'], 5),
             ActionButton(205, 900, tl['field'], 7),
            ],
            
            [ActionButton(65, 900, tl['undo'], 4), # <--- ЗАВОДСКИЕ ЗДАНИЯ (2)
             ActionButton(135, 900, tl['mine'], 6),
            ],
                                  ]
        
    def draw(self, player, camera):
        raylib.DrawRectangleRounded([15, 850, 500, 280], 0.3, 10, (28, 28, 28, 200))
    
        raylib.DrawRectangleRounded([25, 860, 480, 280], 0.25, 10, (28, 28, 28, 255))

        for button in self.pages_info[self.page]:
            button.draw(self, player, camera)
            
        
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
        