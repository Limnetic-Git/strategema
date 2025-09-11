import raylib


class Camera:
    def __init__(self):
        self.pos = [0, 0]
        self.is_dragging = False
        self.drag_start_pos = [0, 0]
        self.focus_block = [0, 0]
        self.default_focus = None
        
    def drag_to_move(self, window, world):
        if not raylib.IsMouseButtonPressed(raylib.MOUSE_BUTTON_LEFT):
            if raylib.IsMouseButtonPressed(raylib.MOUSE_BUTTON_MIDDLE):
                self.is_dragging = True
                self.drag_start_pos = [raylib.GetMouseX(), raylib.GetMouseY()]
            if raylib.IsMouseButtonReleased(raylib.MOUSE_BUTTON_MIDDLE):
                self.is_dragging = False
                
            if self.is_dragging and raylib.IsMouseButtonDown(raylib.MOUSE_BUTTON_MIDDLE):
                mouse_pos = [raylib.GetMouseX(), raylib.GetMouseY()]
                self.pos[0] += self.drag_start_pos[0] - mouse_pos[0]
                self.pos[1] += self.drag_start_pos[1] - mouse_pos[1]
                self.focus_block = [(self.pos[0] + window.width // 2) // world.block_size, (self.pos[1] + window.height // 2) // world.block_size]
                self.drag_start_pos = mouse_pos
    
    def focus_camera_to(self, window, world, block_x, block_y):
        if self.default_focus == None:
            self.default_focus = [(window.width // 2) // world.block_size, (window.height // 2) // world.block_size]
        self.pos = [world.block_size * (block_x - self.default_focus[0]), world.block_size * (block_y - self.default_focus[1])]
    
    def select(self, units_list, player):
        if not raylib.IsMouseButtonPressed(raylib.MOUSE_BUTTON_MIDDLE):
            mouse_pos = [raylib.GetMouseX(), raylib.GetMouseY()]
            if raylib.IsMouseButtonPressed(raylib.MOUSE_BUTTON_LEFT):
                self.is_dragging = True
                self.drag_start_pos = [raylib.GetMouseX(), raylib.GetMouseY()]
                
            if raylib.IsMouseButtonReleased(raylib.MOUSE_BUTTON_LEFT):
                self.is_dragging = False
                 
                world_start_x = self.drag_start_pos[0] + self.pos[0]
                world_start_y = self.drag_start_pos[1] + self.pos[1]
                world_end_x = mouse_pos[0] + self.pos[0]
                world_end_y = mouse_pos[1] + self.pos[1]
                
                selection_left = min(world_start_x, world_end_x)
                selection_right = max(world_start_x, world_end_x)
                selection_top = min(world_start_y, world_end_y)
                selection_bottom = max(world_start_y, world_end_y)
                
                for i, unit in enumerate(units_list.units_list):
                    if unit.team == player.team:
                        if (selection_left <= unit.x <= selection_right and
                            selection_top <= unit.y <= selection_bottom):
                                unit.selected = True
                        else:
                            if unit.selected:
                                if mouse_pos[1] < 850:
                                    unit.go_to_pos = [world_start_x, world_start_y]
                                else:
                                    if mouse_pos[0] > 500:
                                        unit.go_to_pos = [world_start_x, world_start_y]
                                    
                
            if self.is_dragging and raylib.IsMouseButtonDown(raylib.MOUSE_BUTTON_LEFT):
                self.__draw_selection_rect(mouse_pos)
        if raylib.IsMouseButtonPressed(raylib.MOUSE_BUTTON_RIGHT):
            for unit in units_list.units_list:
                if unit.selected:
                    unit.selected = False
                
    def __draw_selection_rect(self, mouse_pos):
        for i in range(5):
            raylib.DrawRectangleLines(int(self.drag_start_pos[0] - i), int(self.drag_start_pos[1] - i),
                                                    int(mouse_pos[0] - self.drag_start_pos[0]), int(mouse_pos[1] - self.drag_start_pos[1]), raylib.YELLOW)

            