from pyglm import glm

class Shape:
    def __init__(self):
        self.CenterOfMass = self.CalcCenterOfMass()
        self.InertiaTensor = self.CalcInertiaTensor() + self.GetParallelAxisTheoremTensor()
        self.InertiaTensor_Inverse = glm.inverse(self.InertiaTensor)
    def __del__(self):
        pass
    # モデル中心と重心がずれている場合の慣性テンソルの調整
    def GetParallelAxisTheoremTensor(self):
        r = -self.CenterOfMass
        r2 = glm.dot(r, r)
        xx = r.x * r.x
        xy = r.x * r.y
        xz = r.x * r.z 
        yy = r.y * r.y
        yz = r.y * r.z
        zz = r.z * r.z
        return glm.mat3(r2-xx, xy, xz,
                        xy, r2-yy, yz,
                        xz, yz, r2-zz)
    def CalcCenterOfMass(self):
        return glm.vec3(0.0)
    def CalcInertiaTensor(self):
        return glm.mat3(1.0)
    def GetSupportPoint(self, pos, rot, uDir, bias):
        return None
    def GetFastestRotatingPointSpeed(self, angVel, uDir):
        return 0.0

class ConvexBase(Shape):
    def __init__(self):
        # 派生で定義してない場合に限り Vertices, Indices を初期化
        if not hasattr(self, 'Vertices'):
            self.Vertices = []
        if not hasattr(self, 'Indices'):
            self.Indices = []
        # 基底の __init__() を呼び出す
        super().__init__()
    def __del__(self):
        super().__del__()

    def CalcExtent(self):
        xs = []
        ys = []
        zs = []
        for i in self.Vertices:
            xs.append(i.x)
            ys.append(i.y)
            zs.append(i.z)
        return glm.vec3(max(xs) - min(xs), max(ys) - min(ys), max(zs) - min(zs))

    def GetSupportPoint(self, pos, rot, uDir, bias):
        points = []
        for i in self.Vertices:
            points.append(rot * i + pos)
        return max(points, key = lambda rhs: glm.dot(uDir, rhs)) + uDir * bias
    
    def GetFastestRotatingPointSpeed(self, angVel, uDir):
        speeds = []
        for i in self.Vertices:
            speeds.append(glm.dot(uDir, glm.cross(angVel, i - self.CenterOfMass)))
        return max(speeds)

class ShapeBox(ConvexBase):
    def __init__(self, ext = glm.vec3(1.0)):
        x = ext.x * 0.5
        y = ext.y * 0.5
        z = ext.z * 0.5
        self.Vertices = [
            glm.vec3(x, y, z),
            glm.vec3(x, y, -z),
            glm.vec3(x, -y, z),
            glm.vec3(x, -y, -z),
            glm.vec3(-x, y, z),
            glm.vec3(-x, y, -z),
            glm.vec3(-x, -y, z),
            glm.vec3(-x, -y, -z),
        ]
        self.Indices = [
            0, 1, 2, 1, 3, 2,   # right
            4, 6, 5, 5, 6, 7,   # left
            0, 2, 4, 2, 6, 4,   # front
            1, 5, 3, 3, 5, 7,   # back
            0, 4, 1, 1, 4, 5,   # top
            2, 3, 6, 3, 7, 6,   # bottom
        ]
        # Vertices, Indicesを初期化してから、基底の __init__() を呼び出す
        super().__init__()
    def __del__(self):
        super().__del__()
    
    def CalcInertiaTensor(self):
        ext = self.CalcExtent()
        x2 = ext.x * ext.x
        y2 = ext.y * ext.y
        z2 = ext.z * ext.z
        return glm.mat3(y2 + z2, 0.0, 0.0,
                        0.0, x2 + z2, 0.0,
                        0.0, 0.0, x2 + y2) / 12.0

class ShapeConvex(ConvexBase):
    def __init__(self):
        super().__init__()
    def __del__(self):
        super().__del__()
    # def CalcCenterOfMass(self):
    #     return glm.vec3(0.0)
    # def CalcInertiaTensor(self):
    #     return glm.mat3(1.0)
    
