from pyglm import glm

class Shape:
    def __init__(self):
        pass
    def __del__(self):
        pass

class ConvexBase(Shape):
    def __init__(self):
        super().__init__()
        self.Vertices = []
        self.Indices = []
    def __del__(self):
        super().__del__()

class ShapeBox(ConvexBase):
    def __init__(self):
        super().__init__()
        self.Vertices = [
            glm.vec3(0.5),
            glm.vec3(0.5, 0.5, -0.5),
            glm.vec3(0.5, -0.5, 0.5),
            glm.vec3(0.5, -0.5, -0.5),
            glm.vec3(-0.5, 0.5, 0.5),
            glm.vec3(-0.5, 0.5, -0.5),
            glm.vec3(-0.5, -0.5, 0.5),
            glm.vec3(-0.5),
        ]
        self.Indices = [
            0, 1, 2, 1, 3, 2,   # right
            4, 6, 5, 5, 6, 7,   # left
            0, 2, 4, 2, 6, 4,   # front
            1, 5, 3, 3, 5, 7,   # back
            0, 4, 1, 1, 4, 5,   # top
            2, 3, 6, 3, 7, 6,   # bottom
        ]
    def __del__(self):
        super().__del__()