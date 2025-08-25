import raylib
import random
from window import Window
from map import World
from camera import Camera
from textures_lib import TexturesLibrary
from units import UnitsList, Scout
from gui import ActionBar

window = Window(1600, 1000)
world = World()
camera = Camera()
tl = TexturesLibrary()
units_list = UnitsList()
action_bar = ActionBar(tl)


units_list.add(Scout(4800, 4800))

camera.focus_camera_to(window, world, 100, 100)
while not raylib.WindowShouldClose():
    world.draw(window, tl, camera)
    units_list.draw_all(camera)
    camera.drag_to_move(window, world)
    camera.select(units_list)
    action_bar.draw()

    raylib.EndDrawing()
raylib.CloseWindow()
