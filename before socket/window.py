import raylib


class Window:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.game_version = '0.1'
        self.MAX_FPS = 60
        
        raylib.InitWindow(width, height, f"Strategro v{self.game_version}".encode())
        raylib.SetTargetFPS(self.MAX_FPS)
        