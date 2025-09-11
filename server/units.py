import random
import math

class UnitsList:
    def __init__(self):
        self.units_list = []
        self.units_id_counter = 0
    
    def pack_units_list(self):
        pack = []
        for unit in self.units_list:
            dict_ = unit.converse_to_dict().copy()
            del dict_['damage_to_units']
            del dict_['damage_to_buildings']
            del dict_['fire_rate']
            del dict_['speed']
            del dict_['type_of_movement']
            del dict_['go_to_pos']
            pack.append(dict_)
        return pack
    
    def update_all(self, world):
        for unit in self.units_list:
            unit.update(world)
                   
    def add(self, unit):
        self.units_id_counter += 1
        self.units_list.append(unit)
        
            
            
class Unit:
    def __init__(self, id, x, y, team, name, hp, damage_to_units, damage_to_buildings, fire_rate, speed, type_of_movement):
        self.id = id
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
        self.go_to_pos = [None, None]
        
    def converse_to_dict(self):
        return self.__dict__
    
    def update(self, world):
        if self.go_to_pos != [None, None] and self.go_to_pos != [self.x, self.y]:
            dx = self.go_to_pos[0] - self.x
            dy = self.go_to_pos[1] - self.y
            distance = math.hypot(dx, dy)
            
            if distance > 2:
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

                        
class Scout(Unit):
    def __init__(self, x, y, team, units_list):
        super().__init__(id=units_list.units_id_counter, x=x, y=y, team=team, name='Scout', hp=100, damage_to_units=10,
                                  damage_to_buildings=5, fire_rate=0.75, speed=5,
                                  type_of_movement='land')