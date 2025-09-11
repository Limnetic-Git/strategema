import raylib
import random
from window import Window
from map import World
from camera import Camera
from textures_lib import TexturesLibrary
from units import UnitsList, Scout
from gui import ActionBar
from player import Player
from loaded_map import LoadedMap
import time


window = Window(1600, 1000) #создаёт окно X на Y пикселей (см. window.py)
world = World() #создаёт мир по дефолту на рандомном сиде и с размером 256 на 256 (cм. map.py)
camera = Camera() #создаёт камеру которую можно двигать зажимая СКМ, а также выделять юнитов (см. camera.py)
tl = TexturesLibrary() #создаёт стеш с текстурами игры. обращаться к текстуре можно как tl['tree'] (см. texture_lib.py)
units_list = UnitsList() #создаёт стеш с информацией о всех юнитах, с возможностью отрисовывать их и добавлять новых (см. units.py)
action_bar = ActionBar(tl) #создаёт скруглённое темное меню слева снизу, а будет отвечать за весь UI для строительства и изучений (см. gui.py)
player = Player(0) #создаёт игрока, хранит информацию о его ресурсах и координатах столицы (см. player.py)
loaded_map = LoadedMap(world) #хранит прогруженный игроком мир с учетом тумана войны и прогрузки (см. loaded_map.py)

world.spawn_teams(4, player, units_list) #спавнит в мире 4 команды игроков в виде зданий с залежей железа справа, а также одним скаутом (см. map.py)


camera.focus_camera_to(window, world, player.capital_cords[0], player.capital_cords[1]) #фокусирует камеру на координатах столицы игрока (cм. camera.py)


while not raylib.WindowShouldClose():
    loaded_map.update(world) #отвечает за затемнение ласт-лоад зоны
    units_list.update_all(world, loaded_map, player)
    world.draw(window, tl, camera, loaded_map) #рисует весь мир
    units_list.draw_all(camera, world, loaded_map, player) #рисует всех юнитов

    camera.drag_to_move(window, world) #позволяет камере перемещаться на СКМ
    camera.select(units_list, player) #позволяет выделять юнитов
    action_bar.draw() #рисует панельку gui слева-снизу
    
    raylib.EndDrawing()
raylib.CloseWindow()
