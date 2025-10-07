import raylib


class Camera:
    def __init__(self):
        self.pos = [0, 0]
        self.is_dragging = False
        self.drag_start_pos = [0, 0]
        self.focus_block = [0, 0]
        self.grid = True
        
        self.current_building = None
        
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
        #wheel_move = raylib.GetMouseWheelMove()
   
    
    def focus_camera_to(self, window, world, block_x, block_y):
        if not hasattr(self, 'default_focus'): 
            self.default_focus = [(window.width // 2) // world.block_size, (window.height // 2) // world.block_size]
        self.pos = [world.block_size * (block_x - self.default_focus[0]), world.block_size * (block_y - self.default_focus[1])]
    
    def select(self, window, world, units_list, player, client_socket):
        if raylib.IsKeyPressed(raylib.KEY_C):
            self.focus_camera_to(window, world, player.capital_cords[0], player.capital_cords[1]) 
        if raylib.IsKeyPressed(raylib.KEY_G):
            self.grid = not self.grid
            
        if not raylib.IsMouseButtonPressed(raylib.MOUSE_BUTTON_MIDDLE):
            
            mouse_pos = [raylib.GetMouseX(), raylib.GetMouseY()]
            if not self.current_building:
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
                    
                    for unit in units_list.units_list:
                        if unit.team == player.team:
                            if (selection_left <= unit.x <= selection_right and selection_top <= unit.y <= selection_bottom):
                                if not unit.id in units_list.selected_units_ids:
                                    units_list.selected_units_ids.append(unit.id)
                                unit.selected = True
                                    
                            else: 
                                if unit.selected:
                                    if mouse_pos[1] > 850 and mouse_pos[0] > 500 or mouse_pos[1] < 850:
                                        if world_start_x > 0 and world_start_y > 0:
                                            client_socket.tasks.append({'task_id': client_socket.tasks_id_counter, 'unit_id': unit.id,
                                                                                        'x': world_start_x, 'y': world_start_y})    
                                            client_socket.tasks_id_counter += 1
                                        
                if self.is_dragging and raylib.IsMouseButtonDown(raylib.MOUSE_BUTTON_LEFT):
                    self.__draw_selection_rect(mouse_pos)
        if raylib.IsMouseButtonPressed(raylib.MOUSE_BUTTON_RIGHT):
            for unit in units_list.units_list:
                if unit.selected:
                    units_list.selected_units_ids = []
                    unit.selected = False
                    
    def build(self, tl, world, player, client_socket, loaded_map):
        if self.current_building:
            mouse_pos = [raylib.GetMouseX(), raylib.GetMouseY()]
            if mouse_pos[1] > 850 and mouse_pos[0] > 500 or mouse_pos[1] < 850:
                block_to_build = [(self.pos[0] + mouse_pos[0]) // world.block_size, (self.pos[1] + mouse_pos[1]) // world.block_size]
                if loaded_map.now_loaded[block_to_build[0]][block_to_build[1]] == 0:
                    if self.current_building['type'] != 'city' and player.city_borders[block_to_build[0]][block_to_build[1]] == 1 or \
                       self.current_building['type'] == 'city' and player.city_borders[block_to_build[0]][block_to_build[1]] == 2:
                        
                        raylib.DrawTextureEx(tl[self.current_building['type']], (block_to_build[0] * world.block_size - self.pos[0],
                                                                             block_to_build[1] * world.block_size - self.pos[1]), 0, 1, [255, 255, 255, 145])
                    
                    if raylib.IsMouseButtonPressed(raylib.MOUSE_BUTTON_LEFT):
                    
                        if self.current_building['type'] != 'city' and player.city_borders[block_to_build[0]][block_to_build[1]] == 1 or \
                           self.current_building['type'] == 'city' and player.city_borders[block_to_build[0]][block_to_build[1]] == 2:
                            
                            client_socket.tasks.append({'task_id': client_socket.tasks_id_counter, 'building': self.current_building, 'x': block_to_build[0], 'y': block_to_build[1]})                                    
                            if not (block_to_build[0], block_to_build[1]) in player.buildings:
                                player.buildings.append((block_to_build[0], block_to_build[1]))
                            client_socket.tasks_id_counter += 1

                if raylib.IsMouseButtonPressed(raylib.MOUSE_BUTTON_RIGHT):
                    self.current_building = None
    
    def __draw_selection_rect(self, mouse_pos):
        for i in range(5):
            raylib.DrawRectangleLines(int(self.drag_start_pos[0] - i), int(self.drag_start_pos[1] + i),
                                                    int(mouse_pos[0] - self.drag_start_pos[0]), int(mouse_pos[1] - self.drag_start_pos[1]), raylib.YELLOW)
            
            