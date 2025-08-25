import raylib, random
from generate_map import MapGenerator
  
raylib.InitWindow(800, 800, b"Test aboba")
block_size = 4
FPS = 60
raylib.SetTargetFPS(FPS)


seed = random.randint(0, 999999)
world_map = MapGenerator(200, seed)

print(f"World seed: {seed}")

tick = 0
while not raylib.WindowShouldClose():  
    world_map.draw(          
    tick += 1
raylib.CloseWindow()
