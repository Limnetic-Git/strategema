import raylib
import random
import math

class UnitsList:
    def __init__(self):
        self.units_list = []
        

    def draw_all(self, camera, world):
        for unit in self.units_list:
            unit.draw(camera, world)
    
    def add(self, unit):
        self.units_list.append(unit)
            
            
class Unit:
    def __init__(self, x, y, team, name, hp, damage_to_units, damage_to_buildings, fire_rate, speed, type_of_movement):
        self.x = x
        self.y = y
        self.team = team
        self.name = name
        self.hp = hp
        self.damage_to_units = damage_to_units
        self.damage_to_buildings = damage_to_buildings
        self.fire_rate = fire_rate
        self.speed = speed
        self.type_of_movement = type_of_movement
        self.selected = False
        self.go_to_pos = [None, None]
    
    def update(self, world):
        if self.go_to_pos != [None, None] and self.go_to_pos != [self.x, self.y]:
            dx = self.go_to_pos[0] - self.x
            dy = self.go_to_pos[1] - self.y
            distance = math.hypot(dx, dy)
            
            if distance > 0:
                if not hasattr(self, '_move_accumulator_x'):
                    self._move_accumulator_x, self._move_accumulator_y = 0.0, 0.0
                self._move_accumulator_x += (dx / distance) * self.speed
                self._move_accumulator_y += (dy / distance) * self.speed
                move_x_int, move_y_int = int(self._move_accumulator_x), int(self._move_accumulator_y)
                if move_x_int != 0 or move_y_int != 0:
                    self.x += move_x_int; self.y += move_y_int
                    self._move_accumulator_x -= move_x_int; self._move_accumulator_y -= move_y_int
                    
                if abs(self.x - self.go_to_pos[0]) <= 1 and abs(self.y - self.go_to_pos[1]) <= 1:
                    self.x, self.y = self.go_to_pos
            bx, by = self.x // 48, self.y // 48
            for i in [-1, 1]:
                for k in [-1, 1]:
                    for j in range(5):
                        for u in range(5):
                            world.fog[bx + (j*i)][by + (u*k)] = 0

        
class Scout(Unit):
    def __init__(self, x, y, team):
        super().__init__(x=x, y=y, team=team, name='Scout', hp=100, damage_to_units=10,
                                  damage_to_buildings=5, fire_rate=0.75, speed=1,
                                  type_of_movement='land')
    def draw(self, camera, world):
        color = [raylib.RED, raylib.BLUE, raylib.PURPLE, raylib.YELLOW]
        raylib.DrawCircle(self.x - camera.pos[0], self.y - camera.pos[1], 10, color[self.team])
        if self.selected:
            for i in range(2):
                if self.team != 3:
                    raylib.DrawCircleLines(self.x - camera.pos[0], self.y - camera.pos[1], 10 - i, raylib.YELLOW)
                else:
                    raylib.DrawCircleLines(self.x - camera.pos[0], self.y - camera.pos[1], 10 - i, raylib.BLACK)
        super().update(world)
        