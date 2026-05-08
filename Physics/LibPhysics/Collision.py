from pyglm import glm
import numpy as np

import LibPhysics.RigidBody

class ContactBase:
    def __init__(self):
        self.TimeOfImpact = 0.0
        self.RigidBodyA = None
        self.RigidBodyB = None
        self.PointA_World = glm.vec3(0.0)
        self.PointB_World = glm.vec3(0.0)
        self.Normal_World = glm.vec3(0.0)
    def __del__(self):
        None

    def Swap(self):
        self.RigidBodyA, self.RigidBodyB = self.RigidBodyB, self.RigidBodyA
        self.PointA_World, self.PointB_World = self.PointB_World, self.PointA_World
        self.Normal_World = -self.Normal_World

class Contact(ContactBase):
    def __init__(self):
        super().__init__()
        self.PointA = glm.vec3(0.0)
        self.PointB = glm.vec3(0.0)
    def __del__(self):
        super().__del__()

    def Swap(self):
        super().Swap()
        self.PointA, self.PointB = self.PointB, self.PointA
        
    def CalcLocal(self):
        self.PointA = self.RigidBodyA.ToLocalPos(self.PointA_World)
        self.PointB = self.RigidBodyB.ToLocalPos(self.PointB_World)

def Minor3(m3, col, row):
    m2 = glm.mat2()
    r = 0
    for j in range(3):
        if row == j:
            continue
        c = 0
        for i in range(3):
            if col == i:
                continue
            m2[c][r] = m3[i][j]
            c += 1
        r += 1
    return m2
def Minor4(m4, col, row):
    m3 = glm.mat3()
    r = 0
    for j in range(4):
        if row == j:
            continue
        c = 0
        for i in range(4):
            if col == i:
                continue
            m3[c][r] = m4[i][j]
            c += 1
        r += 1
    return m3

#def Cofactor3(m3, col, row):
#    return glm.pow(-1.0, col + row) * glm.determinant(Minor3(m3, col, row))
def Cofactor4(m4, col, row):
    return glm.pow(-1.0, col + row) *  glm.determinant(Minor4(m4, col, row))

def Barycentric(a, b, c):
    n = glm.cross(b - a, c - a)
    # 三角形 abc に射影した原点を p
    p = n * glm.dot(a, n) / glm.length2(n)
    
    # xy, yz, zx 3 面へ射影した面積
    areas = []
    areasAbs = []
    for i in range(3):
        j = (i + 1) % 3
        k = (i + 2) % 3
        tmp = glm.vec2(a[j], a[k])
        ab = glm.vec2(b[j], b[k]) - tmp
        ac = glm.vec2(c[j], c[k]) - tmp
        area = glm.determinant(glm.mat2(ab, ac))
        areas.append(area)
        areasAbs.append(glm.abs(area))

    # 射影が最大となる面
    index = np.argmax(areasAbs)

    # p、abc を選択した面に射影 (Z が選択された場合は XY 平面といった具合になる)
    x = (index + 1) % 3
    y = (index + 2) % 3

    prjABC = [glm.vec2(a[x], a[y]), glm.vec2(b[x], b[y]), glm.vec2(c[x], c[y])]
    prjP = glm.vec2(p[x], p[y])

    # 射影後の p, abc からなるサブ三角形それぞれの面積
    subAreas = []
    for i in range(3):
        j = (i + 1) % 3
        k = (i + 2) % 3
        subAreas.append(glm.determinant(glm.mat2(prjABC[j] - prjP, prjABC[k] - prjP)))
    
    # p が abc 内部にあればパラメータを返す
    if all(glm.sign(i) == glm.sign(areas[index]) for i in subAreas):
        return glm.vec3(subAreas[0], subAreas[1], subAreas[2]) / areas[index]
    
    return None

def SignedVolume1(a, b):
    ab = b - a
    # 線分 ab に射影した原点を p
    p = a + ab * glm.dot(ab, -a) / glm.length2(ab)

    # ab をxyz各軸へ射影した線分
    segs = []
    for i in ab:
        segs.append(glm.abs(i))
    
    # 射影が最大となる軸
    index = np.argmax(segs)

    # p. a. b を軸へ射影
    prjA = a[index]
    prjB = b[index]
    prjP = p[index]

    # p が ab の内部にあれば重心パラメータを返す
    if (prjP > prjA and prjP < prjB) or (prjP > prjB and prjP < prjA):
        return glm.vec2(prjB - prjP, prjP - prjA) / ab[index]

    # 外部確定 p が a 側か b 側か
    if (prjA <= prjB and prjP <= prjA) or (prjA >= prjB and prjP >= prjA):
        return glm.vec2(1.0, 0.0)
    
    return glm.vec2(0.0, 1.0)

def SignedVolume2(a, b, c):
    # 三角形 abc に原点を射影し内部にあれば重心パラメータを返すs
    lmd = Barycentric(a, b, c)
    if lmd is not None:
        return lmd
    
    # 3 辺に対して重心パラメータと距離を求めるs
    edges = [a, b, c]
    lmds = []
    lens = []
    for i in range(3):
        j = (i + 1) % 3
        k = (i + 2) % 3
        # 1-シンプレクスに帰着
        lmd = SignedVolume1(edges[j], edges[k])
        lmds.append(lmd)
        lens.append(glm.length2(edges[j] * lmd[0] + edges[k] * lmd[1]))

    # 距離が最小となるインデックス
    index = np.argmin(lens)

    lmd = glm.vec3(0.0)
    #lmd[index] = 0.0
    lmd[(index + 1) % 3] = lmds[index][0]
    lmd[(index + 2) % 3] = lmds[index][1]

    return lmd

def SignedVolume3(a, b, c, d):
    m = glm.transpose(glm.mat4(glm.vec4(a, 1.0), glm.vec4(b, 1.0), glm.vec4(c, 1.0), glm.vec4(d, 1.0)))
    cof = glm.vec4(Cofactor4(m, 3, 0), Cofactor4(m, 3, 1), Cofactor4(m, 3, 2), Cofactor4(m, 3, 3))
    det = sum(cof)
    if all(glm.sign(det) == glm.sign(i) for i in cof):
        return cof / det
    
    faces = [a, b, c, d]
    lmds = []
    lens = []
    for i in range(4):
        j = (i + 1) % 4
        k = (i + 2) % 4
        # 2-シンプレクスに帰着
        lmd = SignedVolume2(faces[i], faces[j], faces[k])
        lmds.append(lmd)
        lens.append(glm.length2(faces[i] * lmd[0] + faces[j] * lmd[1] + faces[k] * lmd[2]))

    index = np.argmin(lens)

    lmd = glm.vec4(0.0)
    lmd[index] = lmds[index][0]
    lmd[(index + 1) % 4] = lmds[index][1]
    lmd[(index + 2) % 4] = lmds[index][2]
    #lmd[(index + 3) % 4] = 0.0

    return lmd

# テスト
def SignedVolumeTest():
    orig = [glm.vec3(0), glm.vec3(1, 0, 0), glm.vec3(0, 1, 0), glm.vec3(0, 0, 1)]
    pts = []
    for i in orig:
        pts.append(i + glm.vec3(1))
    lmd = LibPhysics.Collision.SignedVolume3(pts[0], pts[1], pts[2], pts[3])
    print(lmd) # 1, 0, 0, 0
    v = pts[0] * lmd[0] + pts[1] * lmd[1] + pts[2] * lmd[2] + pts[3] * lmd[3]
    print(v) # 1, 1 ,1

    pts.clear()
    for i in orig:
        pts.append(i + glm.vec3(-1))
    lmd = LibPhysics.Collision.SignedVolume3(pts[0], pts[1], pts[2], pts[3])
    print(lmd) # 0, 0.33, 0.33, 0.33
    v = pts[0] * lmd[0] + pts[1] * lmd[1] + pts[2] * lmd[2] + pts[3] * lmd[3]
    print(v) # -0.6687, -0.6687, -0.6687

    pts.clear()
    for i in orig:
        pts.append(i + glm.vec3(1, 1, -0.5))
    lmd = LibPhysics.Collision.SignedVolume3(pts[0], pts[1], pts[2], pts[3])
    print(lmd) # 0.5, 0, 0, 0.5
    v = pts[0] * lmd[0] + pts[1] * lmd[1] + pts[2] * lmd[2] + pts[3] * lmd[3]
    print(v) # 1, 1, 0

    pts.clear()
    pts = [ 
        glm.vec3(51.1996613, 26.1989613, 1.91339576), 
        glm.vec3(-51.0567360, -26.0565681, -0.436143428),
        glm.vec3(50.8978920, -24.1035538, -1.04042661),
        glm.vec3(-49.1021080, 25.8964462, -1.04042661)
    ]
    lmd = LibPhysics.Collision.SignedVolume3(pts[0], pts[1], pts[2], pts[3])
    print(lmd) # 0.29, 0.302, 0.206, 0.202
    v = pts[0] * lmd[0] + pts[1] * lmd[1] + pts[2] * lmd[2] + pts[3] * lmd[3]
    print(v) # 0, 0, 0