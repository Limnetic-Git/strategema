import raylib

class ActionButton:
    def __init__(self, x, y, texture, action):
        self.x = x
        self.y = y
        self.texture = texture
        self.action = action
        
    def draw(self, action_bar):
        raylib.DrawTextureEx(self.texture, (self.x, self.y), 0, 1, raylib.WHITE)
        self.__check_press(action_bar)
        
    def __check_press(self, action_bar):
        if raylib.IsMouseButtonPressed(raylib.MOUSE_BUTTON_LEFT):
            xm, ym = raylib.GetMouseX(), raylib.GetMouseY()
            if xm >= self.x and xm <= self.x + self.texture.width and ym >= self.y and ym <= self.y + self.texture.height:
                if self.action == 0: action_bar.page = 1
                elif self.action == 4: action_bar.page = 0
                elif self.action == 1: action_bar.page = 2
                else: print('WORK IN PROGRESS')
                
class ActionBar:
    def __init__(self, tl):
        self.page = 0
        self.pages_info = [
            [ActionButton(65, 900, tl['city'], 0), # <--- ГЛАВНАЯ СТРАНИЦА (0)
             ActionButton(135, 900, tl['factory'], 1),
             ActionButton(205, 900, tl['sword'], 2),
             ActionButton(275, 900, tl['research'], 3),
            ],
            
            [ActionButton(65, 900, tl['undo'], 4),  # <---  МИРНЫЕ ЗДАНИЯ (1)
             ActionButton(135, 900, tl['new_city'], 5),
             ActionButton(205, 900, tl['field'], 7),
            ],
            
            [ActionButton(65, 900, tl['undo'], 4), # <--- ЗАВОДСКИЕ ЗДАНИЯ (2)
             ActionButton(135, 900, tl['mine'], 6),
            ],
                                  ]
        
    def draw(self):
        #raylib.DrawRectangle(15, 850, 500, 280, (28, 28, 28))
        raylib.DrawRectangleRounded([15, 850, 500, 280], 0.3, 10, (28, 28, 28, 200))
    
        raylib.DrawRectangleRounded([25, 860, 480, 280], 0.25, 10, (28, 28, 28, 255))

        for button in self.pages_info[self.page]:
            button.draw(self)
            
        
        