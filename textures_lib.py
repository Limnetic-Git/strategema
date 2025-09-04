import raylib

class TexturesLibrary:
    def __init__(self):
        self.textures_library = {}
        self.textures_library['tree'] = raylib.LoadTexture(b"textures/tree.png")
        self.textures_library['metal_cluster'] = raylib.LoadTexture(b"textures/metal_cluster.png")
        self.textures_library['water_metal_cluster'] = raylib.LoadTexture(b"textures/water_metal_cluster.png")
        self.textures_library['city'] = raylib.LoadTexture(b"textures/city.png")
        self.textures_library['factory'] = raylib.LoadTexture(b"textures/factory.png")
        self.textures_library['fog'] = raylib.LoadTexture(b"textures/fog.png")
        
    def __getitem__(self, key):
        return self.textures_library[key]
    