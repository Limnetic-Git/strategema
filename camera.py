import raylib


class Camera:
    def __init__(self):
        self.pos = [0, 0]
        self.is_dragging = False
        self.drag_start_pos = [0, 0]
        self.focus_block = [0, 0]
        self.grid = True
        self.zoom = 1.0
        self.min_zoom = 0.3
        self.max_zoom = 3.0
        
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
                delta_x = (self.drag_start_pos[0] - mouse_pos[0]) / self.zoom
                delta_y = (self.drag_start_pos[1] - mouse_pos[1]) / self.zoom
                self.pos[0] += delta_x
                self.pos[1] += delta_y
                self.focus_block = [(self.pos[0] + window.width // (2 * self.zoom)) // world.block_size, 
                                  (self.pos[1] + window.height // (2 * self.zoom)) // world.block_size]
                self.drag_start_pos = mouse_pos
        
        wheel_move = raylib.GetMouseWheelMove()
        if wheel_move != 0:
            mouse_x, mouse_y = raylib.GetMouseX(), raylib.GetMouseY()
            world_x_before = self.pos[0] + mouse_x / self.zoom
            world_y_before = self.pos[1] + mouse_y / self.zoom
            
            old_zoom = self.zoom
            self.zoom += wheel_move * 0.3
            self.zoom = max(self.min_zoom, min(self.max_zoom, self.zoom))
            
            world_x_after = self.pos[0] + mouse_x / self.zoom
            world_y_after = self.pos[1] + mouse_y / self.zoom
            
            self.pos[0] += (world_x_before - world_x_after)
            self.pos[1] += (world_y_before - world_y_after)
   
    
    def focus_camera_to(self, window, world, block_x, block_y):
        if not hasattr(self, 'default_focus'): 
            self.default_focus = [(window.width // 2) // world.block_size, 
                                (window.height // 2) // world.block_size]
        self.pos = [world.block_size * (block_x - self.default_focus[0]), 
                   world.block_size * (block_y - self.default_focus[1])]
    
    def screen_to_world(self, screen_x, screen_y):
        return [
            self.pos[0] + screen_x / self.zoom,
            self.pos[1] + screen_y / self.zoom
        ]

    def world_to_screen(self, world_x, world_y):
        return [
            round((world_x - self.pos[0]) * self.zoom),
            round((world_y - self.pos[1]) * self.zoom)
        ]
    
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
                    
                    world_start = self.screen_to_world(self.drag_start_pos[0], self.drag_start_pos[1])
                    world_end = self.screen_to_world(mouse_pos[0], mouse_pos[1])
                    
                    world_start_x, world_start_y = world_start
                    world_end_x, world_end_y = world_end
                    
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
                world_pos = self.screen_to_world(mouse_pos[0], mouse_pos[1])
                block_to_build = [int(world_pos[0] // world.block_size), int(world_pos[1] // world.block_size)]
                
                if 0 <= block_to_build[0] < len(loaded_map.now_loaded) and 0 <= block_to_build[1] < len(loaded_map.now_loaded[0]):
                    if loaded_map.now_loaded[block_to_build[0]][block_to_build[1]] == 0:
                        if self.current_building['type'] != 'city' and player.city_borders[block_to_build[0]][block_to_build[1]] == 1 or \
                           self.current_building['type'] == 'city' and player.city_borders[block_to_build[0]][block_to_build[1]] == 2:
                            
                            screen_pos = self.world_to_screen(block_to_build[0] * world.block_size, 
                                                            block_to_build[1] * world.block_size)
                            
                            raylib.DrawTextureEx(tl[self.current_building['type']], 
                                               (screen_pos[0], screen_pos[1]), 
                                               0, self.zoom, [255, 255, 255, 145])
                        
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
        start_x = self.drag_start_pos[0]
        start_y = self.drag_start_pos[1]
        width = mouse_pos[0] - start_x
        height = mouse_pos[1] - start_y
        
        for i in range(5):
            raylib.DrawRectangleLines(int(start_x - i), int(start_y + i), int(width), int(height), raylib.YELLOW)