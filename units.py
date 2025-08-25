import raylib
import random
import math

class UnitsList:
    def __init__(self):
        self.units_list = []
        

    def draw_all(self, camera):
        for unit in self.units_list:
            unit.draw(camera)
    
    def add(self, unit):
        self.units_list.append(unit)
            
            
class Unit:
    def __init__(self, x, y, name, hp, damage_to_units, damage_to_buildings, fire_rate, speed, type_of_movement):
        self.x = x
        self.y = y
        self.name = name
        self.hp = hp
        self.damage_to_units = damage_to_units
        self.damage_to_buildings = damage_to_buildings
        self.fire_rate = fire_rate
        self.speed = speed
        self.type_of_movement = type_of_movement
        self.selected = False
        self.go_to_pos = [None, None]
    
    def update(self):
        if self.go_to_pos != [None, None] and self.go_to_pos != [self.x, self.y]:
            dx = self.go_to_pos[0] - self.x
            dy = self.go_to_pos[1] - self.y
            distance = math.hypot(dx, dy)
            
            if distance > 0:
                # Накопление дробного движения
                if not hasattr(self, '_move_accumulator_x'):
                    self._move_accumulator_x = 0.0
                    self._move_accumulator_y = 0.0
                
                # Добавляем дробное движение к аккумуляторам
                self._move_accumulator_x += (dx / distance) * self.speed
                self._move_accumulator_y += (dy / distance) * self.speed
                
                # Применяем целую часть движения
                move_x_int = int(self._move_accumulator_x)
                move_y_int = int(self._move_accumulator_y)
                
                if move_x_int != 0 or move_y_int != 0:
                    self.x += move_x_int
                    self.y += move_y_int
                    
                    # Сохраняем дробную часть
                    self._move_accumulator_x -= move_x_int
                    self._move_accumulator_y -= move_y_int
                
                # Проверяем достижение цели
                if abs(self.x - self.go_to_pos[0]) <= 1 and abs(self.y - self.go_to_pos[1]) <= 1:
                    self.x = self.go_to_pos[0]
                    self.y = self.go_to_pos[1]
        
class Scout(Unit):
    def __init__(self, x, y):
        super().__init__(x=x, y=y, name='Scout', hp=100, damage_to_units=10,
                                  damage_to_buildings=5, fire_rate=0.75, speed=1,
                                  type_of_movement='land')
    def draw(self, camera):
        raylib.DrawCircle(self.x - camera.pos[0], self.y - camera.pos[1], 10, raylib.RED)
        if self.selected:
            for i in range(2):
                raylib.DrawCircleLines(self.x - camera.pos[0], self.y - camera.pos[1], 10 - i, raylib.YELLOW)
        super().update()
        