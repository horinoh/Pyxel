# title: 
# author: 
# desc: 
# site: 
# license: MIT
# version: 1.0
 
import pyxel
from pyglm import glm

import LibPhysics.Scene
import LibPhysics.Shape
import LibPhysics.RigidBody
import LibPhysics.Collision

LIGHT_BLUE = 0x87CEEB

class App:
    def __init__(self):
        pyxel.init(width = 320, height = 240, title = "Physics", fps = 60)
        
        # パレットを初期状態
        pyxel.pal()
        # パレットの色を「グレースケール」に書き換える
        for i in range(len(pyxel.colors)):
            pyxel.colors[i] = i * 0x101010
        pyxel.colors[15] = LIGHT_BLUE

        # 描画領域を全画面
        pyxel.clip()

        # 射影変換行列
        povy = glm.radians(45.0)
        aspect = pyxel.width / pyxel.height
        zn = 0.01
        zf = 100.0 
        self.Projection = glm.perspective(povy, aspect, zn, zf)

        # ビュー
        self.CamXAngle = 0.0
        self.CamYAngle = 20.0
        self.CamRadius = 30.0
        self.CamTag = glm.vec3(0.0, 0.0, 0.0)
        self.CamUp = glm.vec3(0.0, 1.0, 0.0)
        self.View = None

        self.HalfWidth = pyxel.width // 2
        self.HalfHeight = pyxel.height // 2
    
        # シーン
        self.Scene = LibPhysics.Scene.Scene()
        floor = LibPhysics.Shape.ShapeBox(glm.vec3(20.0, 1.0, 20.0))
        # 床
        self.Scene.Shapes.append(floor)
        rb = LibPhysics.RigidBody.RigidBody(floor, 0.0)
        rb.Position = glm.vec3(0.0, -0.5, 0.0)
        self.Scene.RigidBodies.append(rb)
        # ボックス
        box = LibPhysics.Shape.ShapeBox()
        self.Scene.Shapes.append(box)
        ofs = 1.5; ny = 2; nx = 2; nz = 2
        for i in range(ny):
            for j in range(nx):
                for k in range(nz):
                    rb = LibPhysics.RigidBody.RigidBody(box, 1.0)
                    rb.Position = glm.vec3(ofs * j - ofs * (nx - 1) * 0.5, ofs * i + 5.0, ofs * k - ofs * (nz - 1) * 0.5)
                    #rb.Velocity_Angular = glm.vec3(0, 0, glm.radians(40))
                    self.Scene.RigidBodies.append(rb)

        self.ctrlBox = LibPhysics.RigidBody.RigidBody(box, 1.0)
        self.ctrlBox.Position = glm.vec3(0.0, 10.0, 0.0)
        self.Scene.RigidBodies.append(self.ctrlBox)

        # ライトの方向
        self.LightDirection = glm.normalize(glm.vec3(0.0, 1.0, 1.0))

        self.ScreenedTris = []
        self.ScreenedPts = []

        self.Pause = False

        # テスト
        LibPhysics.Collision.Test()

        # 更新、描画関数を指定して実行
        pyxel.run(self.update, self.draw)
    
    # 入力
    def inputControl(self):
        # ポーズ
        if pyxel.btnp(pyxel.GAMEPAD1_BUTTON_START) or pyxel.btnp(pyxel.KEY_SPACE):
            self.Pause = not self.Pause

        # カメラ
        if pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_UP, hold = 1, repeat = 1) or pyxel.btnp(pyxel.KEY_W, hold = 1, repeat = 1):
            self.CamYAngle += 1.0
        if pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN, hold = 1, repeat = 1) or pyxel.btnp(pyxel.KEY_S, hold = 1, repeat = 1):
            self.CamYAngle -= 1.0
        if pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT, hold = 1, repeat = 1) or pyxel.btnp(pyxel.KEY_D, hold = 1, repeat = 1):
            self.CamXAngle += 1.0
        if pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT, hold = 1, repeat = 1) or pyxel.btnp(pyxel.KEY_A, hold = 1, repeat = 1):
            self.CamXAngle -= 1.0
        self.CamYAngle = glm.clamp(self.CamYAngle, 0.0, 80.0)
        self.CamXAngle = self.CamXAngle % 360.0
        self.CamPos = glm.vec3(self.CamRadius * glm.sin(glm.radians(self.CamXAngle)), self.CamRadius * glm.sin(glm.radians(self.CamYAngle)), self.CamRadius * glm.cos(glm.radians(self.CamXAngle)))
        self.View = glm.lookAt(self.CamPos, self.CamTag, self.CamUp)        
        self.ViewProjection = self.Projection * self.View

        if pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A, hold = 1, repeat = 1) or pyxel.btnp(pyxel.KEY_DOWN, hold = 1, repeat = 1):
            self.ctrlBox.Position += glm.vec3(0.0, -1.0, 0.0) * 0.1
        if pyxel.btnp(pyxel.GAMEPAD1_BUTTON_B, hold = 1, repeat = 1) or pyxel.btnp(pyxel.KEY_UP, hold = 1, repeat = 1):
            self.ctrlBox.Position += glm.vec3(0.0, 1.0, 0.0) * 0.1
        if pyxel.btnp(pyxel.GAMEPAD1_BUTTON_X, hold = 1, repeat = 1) or pyxel.btnp(pyxel.KEY_LEFT, hold = 1, repeat = 1):
            self.ctrlBox.Rotation = glm.angleAxis(glm.radians(1.0), glm.vec3(1.0, 0.0, 0.0)) * self.ctrlBox.Rotation
        if pyxel.btnp(pyxel.GAMEPAD1_BUTTON_Y, hold = 1, repeat = 1) or pyxel.btnp(pyxel.KEY_RIGHT, hold = 1, repeat = 1):
            self.ctrlBox.Rotation = glm.angleAxis(glm.radians(-1.0), glm.vec3(1.0, 0.0, 0.0)) * self.ctrlBox.Rotation

    # メッシュ描画用の変換
    def drawMesh(self, vertices, indices, World):
        vpw = self.ViewProjection * World
        vw = self.View * World
        for i in range(0, len(indices), 3):
            v0 = glm.vec4(vertices[indices[i]], 1.0)
            v1 = glm.vec4(vertices[indices[i + 1]], 1.0)
            v2 = glm.vec4(vertices[indices[i + 2]], 1.0)

            # スクリーン座標に変換
            sc0 = vpw * v0
            sc1 = vpw * v1
            sc2 = vpw * v2

            # クリッピング
            if sc0.w <= 0 or sc1.w <= 0 or sc2.w <= 0:
                continue
            
            # 法線ベクトル
            N = glm.normalize(glm.cross(glm.vec3(v1) - glm.vec3(v0), glm.vec3(v2) - glm.vec3(v0)))

            # ライティング
            LN = glm.max(0.0, glm.dot(-self.LightDirection, glm.normalize(glm.mat3(World) * N)))

            # バックフェイスカリング
            N = glm.normalize(glm.mat3(vw) * N)
            if N.z > 0:
                continue

            sc0 /= sc0.w
            sc1 /= sc1.w
            sc2 /= sc2.w

            # ビューポート変換
            sc0.x = self.HalfWidth * sc0.x + self.HalfWidth
            sc0.y = -self.HalfHeight * sc0.y + self.HalfHeight
            sc1.x = self.HalfWidth * sc1.x + self.HalfWidth
            sc1.y = -self.HalfHeight * sc1.y + self.HalfHeight
            sc2.x = self.HalfWidth * sc2.x + self.HalfWidth
            sc2.y = -self.HalfHeight * sc2.y + self.HalfHeight

            # 明るさをw成分に格納
            sc0.w = LN
            self.ScreenedTris.append((sc0, sc1, sc2))

    def drawPoints(self, vertices):
        vp = self.ViewProjection
        for i in vertices:
            sv = vp * glm.vec4(i, 1.0)
            if sv.w <= 0:
                continue
            sv /= sv.w
            sv.x = self.HalfWidth * sv.x + self.HalfWidth
            sv.y = -self.HalfHeight * sv.y + self.HalfHeight
            self.ScreenedPts.append(sv)

    # 更新関数
    def update(self):
        self.inputControl()       

        # 物理シミュレーション
        if not self.Pause:
            self.Scene.Update(1.0 / 60.0)

        # 描画用の変換
        self.ScreenedTris.clear()
        self.ScreenedPts.clear()
        for i in range(len(self.Scene.RigidBodies)):
            rb = self.Scene.RigidBodies[i]

            w = glm.mat4(1.0)
            w = glm.translate(w, rb.Position)
            w = w * glm.mat4(rb.Rotation)
            
            self.drawMesh(rb.Shape.Vertices, rb.Shape.Indices, w)

        # z座標でソート（遠い順）
        self.ScreenedTris.sort(key = lambda tri: tri[0].z + tri[1].z + tri[2].z, reverse = True)
        self.ScreenedPts.sort(key = lambda pt: pt.z, reverse = True)

    # 描画関数
    def draw(self):
        # 画面クリア
        pyxel.cls(col = 15)

        # 描画
        for v0, v1, v2 in self.ScreenedTris:
            c = int(v0.w * 14) + 1
            pyxel.tri(v0.x, v0.y, v1.x, v1.y, v2.x, v2.y, c)
            #pyxel.line(v0.x, v0.y, v1.x, v1.y, c); pyxel.line(v1.x, v1.y, v2.x, v2.y, c); pyxel.line(v2.x, v2.y, v0.x, v0.y, c)

        for i in self.ScreenedPts:
            pyxel.pset(i.x, i.y, 0)
App()