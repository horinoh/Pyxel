import math
import sys
import copy

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
    def __del__(self):
        super().__del__()

    def Swap(self):
        super().Swap()
        self.PointA, self.PointB = self.PointB, self.PointA
        
    def CalcLocal(self):
        self.PointA = self.RigidBodyA.ToLocalPos(self.PointA_World)
        self.PointB = self.RigidBodyB.ToLocalPos(self.PointB_World)

class SupportPoint:
    def __init__(self, a, b):
        self.Points = [a - b, a, b]
    def __del__(self):
        None
    def GetA(self):
        return self.Points[1]
    def GetB(self):
        return self.Points[2]
    def GetC(self):
        return self.Points[0]

# 小行列
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
# 小行列
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
    return glm.pow(-1.0, col + row) * glm.determinant(Minor4(m4, col, row))

def Barycentric(a, b, c):
    n = glm.cross(b - a, c - a)
    # 三角形 abc に射影した原点を p
    p = n * glm.dot(a, n) / glm.length2(n)
    
    # xy, yz, zx 3 面へ射影した面積
    areas = []
    for i in range(3):
        j = (i + 1) % 3
        k = (i + 2) % 3
        tmp = glm.vec2(a[j], a[k])
        ab = glm.vec2(b[j], b[k]) - tmp
        ac = glm.vec2(c[j], c[k]) - tmp
        area = glm.determinant(glm.mat2(ab, ac))
        areas.append(area)

    # 射影の絶対値が最大となる面
    index = np.argmax([glm.abs(i) for i in areas])

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

def SimplexSignedVolume(spts, dir):
    match len(spts):
        case 2:
            lmd = SignedVolume1(spts[0].GetC(), spts[1].GetC())
            dir = -(spts[0].GetC() * lmd[0] + spts[1].GetC() * lmd[1])
            return lmd
        case 3:
            lmd = SignedVolume2(spts[0].GetC(), spts[1].GetC(), spts[2].GetC())
            dir = -(spts[0].GetC() * lmd[0] + spts[1].GetC() * lmd[1] + spts[2].GetC() * lmd[2])
            return lmd
        case 4:
            lmd = SignedVolume3(spts[0].GetC(), spts[1].GetC(), spts[2].GetC(), spts[3].GetC())
            dir = -(spts[0].GetC() * lmd[0] + spts[1].GetC() * lmd[1] + spts[2].GetC() * lmd[2] + spts[3].GetC() * lmd[3])
            return lmd
    return None

def GetSupportPoint(rbA, rbB, uDir, bias):
    return SupportPoint(rbA.Shape.GetSupportPoint(rbA.Position, rbA.Rotation, uDir, bias), 
                        rbB.Shape.GetSupportPoint(rbB.Position, rbB.Rotation, -uDir, bias))

def GJK(rbA, rbB, bias, onAB):
    spts = []

    # (1, 1, 1) 方向 (正規化済) へのサポートポイント
    dir = glm.vec3(0.57735, 0.57735, 0.57735)
    spt = GetSupportPoint(rbA, rbB, dir, 0.0)
    spts.append(spt)

    # 原点に向かう方向 (逆向き) へ
    dir = -spt.GetC()
    closest = sys.float_info.max
    hasInt = False
    iLmd = []
    while hasInt == False:
        dir = glm.normalize(dir)
        spt = GetSupportPoint(rbA, rbB, dir, 0.0)

        # 既存の点の場合これ以上拡張できないので衝突無し
        for i in spts:
            if all(np.isclose(i.GetC(), spt.GetC())):
                break

        spts.append(spt)

        # シンプレクスが原点を含むなら衝突
        lmd = SimplexSignedVolume(spts, dir)
        lenSq = glm.length2(dir)
        if math.isclose(lenSq, 0.0, rel_tol = 0.0001):
            hasInt = True
            break

        # 最短を更新できなければ終了 (2三角形の対角線上に原点が位置するような場合、2三角形間でループになるのを回避)
        if lenSq >= closest:
            break
        closest = lenSq
        
        # enumerate() : インデックス付きへ ([0]:インデックス、[1]:値)
        # filter() : [1]:値 が非 0.0 のものだけ残す
        # list(map()) : サポートポイントインデックスと値のペア ([0]:サポートポイントインデックス、[1]:値)
        iLmd = list(map(lambda rhs: [rhs[0], rhs[1]], filter(lambda rhs: rhs[1] != 0.0, enumerate(lmd))))
        # 該当するインデックスのサポートポイントのみ取り出す
        spts = list(map(lambda rhs: spts[rhs[0]], iLmd))

        # 四面体でここまで来たら衝突    
        hasInt = 4 == len(spts)
    
    # 衝突点を求める
    if hasInt:
        EPA(rbA, rbB, spts, bias, onAB)
        print("Hit")
        return True

    # iLmd に値が入らずにループを抜けることがあり、以下の onAB 加算がされない TODO

    # 最近接点を求める
    onAB[0] = glm.vec3(0.0)
    onAB[1] = glm.vec3(0.0)
    for i in range(len(iLmd)):
        onAB[0] += spts[i].GetA() * iLmd[i][1]
        onAB[1] += spts[i].GetB() * iLmd[i][1]

    return False

def EPA(rbA, rbB, spts, bias, onAB):
    None

def ConservativeAdvance(rbA, rbB, deltaSec, ct):
    wRbA = copy.deepcopy(rbA)
    wRbB = copy.deepcopy(rbB)
    
    dt = deltaSec
    toi = 0.0
    itr = 0
    bias = 0.001
    onAB = [glm.vec3(), glm.vec3()]
    while dt > 0:
        if GJK(wRbA, wRbB, bias, onAB):
            ct.TimeOfImpact = toi
            ct.RigidBodyA = rbA
            ct.RigidBodyB = rbB
            ct.Normal_World = glm.normalize(onAB[1] - onAB[0])
            # 拡張分をキャンセル
            onAB[0] -= ct.Normal_World * bias
            onAB[1] += ct.Normal_World * bias
            ct.PointA_World = onAB[0]
            ct.PointB_World = onAB[1]
            ct.CalcLocal()
            return True
                
        # 移動せずに回転しているような場合、ループを抜け出さないことがあるのを回避
        itr += 1
        if itr > 10:
            break

        ab = onAB[1] - onAB[0]

        sepLen = glm.length(ab)
        if math.isclose(sepLen, 0.0):
            print(f"onA == onB {onAB[0]} {onAB[1]}")
            dir = glm.vec3(0.0)
        else:
            dir = ab / sepLen
        vell = glm.dot(wRbA.Velocity_Linear - wRbB.Velocity_Linear, dir)
        vela = wRbA.Shape.GetFastestRotatingPointSpeed(wRbA.Velocity_Angular, dir) - wRbB.Shape.GetFastestRotatingPointSpeed(wRbB.Velocity_Angular, dir)
        orthoSpeed = vell + vela
        if orthoSpeed <= 0.0:
            # 近づいていない
            break
        
        # 衝突するであろう時間
        timeToGo = sepLen / orthoSpeed
        if timeToGo > dt:
            # 今フレーム中には衝突しない
            break

        # 直前まで進める
        dt -= timeToGo
        toi += timeToGo
        wRbA.Update(timeToGo)
        wRbB.Update(timeToGo)
        
    return False

# テスト
def Test():
    orig = [glm.vec3(0), glm.vec3(1, 0, 0), glm.vec3(0, 1, 0), glm.vec3(0, 0, 1)]
    pts = []
    for i in orig:
        pts.append(i + glm.vec3(1))
    lmd = LibPhysics.Collision.SignedVolume3(pts[0], pts[1], pts[2], pts[3])
    assert all(np.isclose(lmd, glm.vec4(1, 0, 0, 0)))
    v = pts[0] * lmd[0] + pts[1] * lmd[1] + pts[2] * lmd[2] + pts[3] * lmd[3]
    assert all(np.isclose(v, glm.vec3(1)))

    pts.clear()
    for i in orig:
        pts.append(i + glm.vec3(-1))
    lmd = LibPhysics.Collision.SignedVolume3(pts[0], pts[1], pts[2], pts[3])
    assert all(np.isclose(lmd, glm.vec4(0, 0.333333, 0.333333, 0.333333)))
    v = pts[0] * lmd[0] + pts[1] * lmd[1] + pts[2] * lmd[2] + pts[3] * lmd[3]
    assert all(np.isclose(v, glm.vec3(-0.666667)))

    pts.clear()
    for i in orig:
        pts.append(i + glm.vec3(1, 1, -0.5))
    lmd = LibPhysics.Collision.SignedVolume3(pts[0], pts[1], pts[2], pts[3])
    assert all(np.isclose(lmd, glm.vec4(0.5, 0.0, 0.0, 0.5)))
    v = pts[0] * lmd[0] + pts[1] * lmd[1] + pts[2] * lmd[2] + pts[3] * lmd[3]
    assert all(np.isclose(v, glm.vec3(1, 1, 0)))

    pts.clear()
    pts = [ 
        glm.vec3(51.1996613, 26.1989613, 1.91339576), 
        glm.vec3(-51.0567360, -26.0565681, -0.436143428),
        glm.vec3(50.8978920, -24.1035538, -1.04042661),
        glm.vec3(-49.1021080, 25.8964462, -1.04042661)
    ]
    lmd = LibPhysics.Collision.SignedVolume3(pts[0], pts[1], pts[2], pts[3])
    assert all(np.isclose(lmd, glm.vec4(0.290401, 0.30223, 0.205651, 0.201718)))
    v = pts[0] * lmd[0] + pts[1] * lmd[1] + pts[2] * lmd[2] + pts[3] * lmd[3]
    assert all(np.isclose(v, glm.vec3(0), atol = 0.00001))