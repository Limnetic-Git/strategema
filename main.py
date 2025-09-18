import raylib
from window import Window
from map import World
from camera import Camera
from client_socket import ClientConnection
from textures_lib import TexturesLibrary
from units import UnitsList
from gui import ActionBar
from player import Player
from loaded_map import LoadedMap

WINDOW_WIDTH = 1600
WINDOW_HEIGHT = 1000

window = Window(WINDOW_WIDTH, WINDOW_HEIGHT) #создаёт окно X на Y пикселей (см. window.py)
client_socket = ClientConnection('89.110.90.193', 1234) 
world = World(seed=client_socket.world_seed) #создаёт мир (cм. map.py)
camera = Camera() #создаёт камеру которую можно двигать зажимая СКМ, а также выделять юнитов (см. camera.py)
units_list = UnitsList() 
tl = TexturesLibrary() #создаёт стеш с текстурами игры. обращаться к текстуре можно как tl['tree'] (см. texture_lib.py)
action_bar = ActionBar(tl) #создаёт скруглённое темное меню слева снизу, а будет отвечать за весь UI для строительства и изучений (см. gui.py)
player = Player(client_socket.id) #создаёт игрока, хранит информацию о его ресурсах и координатах столицы (см. player.py)
world.spawn_teams(4, player)
loaded_map = LoadedMap(world) #хранит прогруженный игроком мир с учетом тумана войны и прогрузки (см. loaded_map.py)
print(f'World seed: {world.seed}')

camera.focus_camera_to(window, world, player.capital_cords[0], player.capital_cords[1]) #фокусирует камеру на координатах столицы игрока (cм. camera.py)


while not raylib.WindowShouldClose():
    loaded_map.update(world) #отвечает за затемнение ласт-лоад зоны
    units_list.update(client_socket.units_dict)
    units_list.update_world_load(world, player, loaded_map)
    world.draw(window, tl, camera, loaded_map) #рисует весь мир
    units_list.draw_all(camera, tl, loaded_map) #рисует всех юнитов


    camera.drag_to_move(window, world) #позволяет камере перемещаться на СКМ
    camera.select(units_list, player, client_socket) #позволяет выделять юнитов
    action_bar.draw() #рисует панельку gui слева-снизу
    
    raylib.EndDrawing()
raylib.CloseWindow()