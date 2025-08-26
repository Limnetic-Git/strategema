import raylib
import random
from window import Window
from map import World
from camera import Camera
from textures_lib import TexturesLibrary
from units import UnitsList, Scout
from gui import ActionBar
from player import Player

window = Window(1600, 1000)
world = World()
camera = Camera()
tl = TexturesLibrary()
units_list = UnitsList()
action_bar = ActionBar(tl)
player = Player(0)
for i in range(4):
    bx, by = world.spawn_team(i)
    if i == player.team: player.capital_cords = [bx, by]
    units_list.add(Scout(bx*48, by*48, i))

camera.focus_camera_to(window, world, player.capital_cords[0], player.capital_cords[1])


units_list.add(Scout(4800, 4800, 0))

while not raylib.WindowShouldClose():
    world.draw(window, tl, camera)
    units_list.draw_all(camera, world)
    camera.drag_to_move(window, world)
    camera.select(units_list)
    action_bar.draw()

    raylib.EndDrawing()
raylib.CloseWindow()
