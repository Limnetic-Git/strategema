import raylib

class ActionButton:
    def __init__(self, x, y, texture, action):
        self.x = x
        self.y = y
        self.texture = texture
        self.action = action
        
    def draw(self):
        raylib.DrawTextureEx(self.texture, (self.x, self.y), 0, 1, raylib.WHITE)
        self.__check_press()
        
    def __check_press(self):
        if raylib.IsMouseButtonPressed(raylib.MOUSE_BUTTON_LEFT):
            xm, ym = raylib.GetMouseX(), raylib.GetMouseY()
            if xm >= self.x and xm <= self.x + self.texture.width and ym >= self.y and ym <= self.y + self.texture.height:
                print('!')
            
class ActionBar:
    def __init__(self, tl):
        self.page = 0
        self.pages_info = [
            [ActionButton(65, 900, tl['city'], 0)], # <--- ГЛАВНАЯ СТРАНИЦА
            ]
        
    def draw(self):
        #raylib.DrawRectangle(15, 850, 500, 280, (28, 28, 28))
        raylib.DrawRectangleRounded([15, 850, 500, 280], 0.3, 10, (28, 28, 28, 200))
    
        raylib.DrawRectangleRounded([25, 860, 480, 280], 0.25, 10, (28, 28, 28, 255))

        for i, button in enumerate(self.pages_info[self.page]):
            button.draw()
            
        
        