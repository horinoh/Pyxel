# title: 
# author: 
# desc: 
# site: 
# license: MIT
# version: 1.0
 
import pyxel
from pyglm import glm

LIGHT_BLUE = 0x87CEEB

class App:
    def __init__(self):
        pyxel.init(width = 320, height = 240, title = "3D", fps = 60)
        
        pyxel.images[0].load(x = 0, y = 0, filename = "../Assets/noguchi_128x128.png")

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
        # ビューポート変換行列
        # self.Viewport = glm.mat4(
        #      [self.HalfWidth, 0.0, 0.0, 0.0],
        #      [0.0, -self.HalfHeight, 0.0, 0.0],
        #      [0.0, 0.0, 1.0, 0.0],
        #      [self.HalfWidth, self.HalfHeight, 0.0, 1.0]
        # )

        # 平面
        self.FloorVertices = [
            glm.vec3(-0.5, 0.0, -0.5),
            glm.vec3(0.5, 0.0, -0.5),
            glm.vec3(0.5, 0.0, 0.5),
            glm.vec3(-0.5, 0.0, 0.5),
        ]
        self.FloorIndices = [
            0, 1, 2,
            0, 2, 3,
        ]
        w = glm.mat4(1.0)
        w = glm.translate(w, glm.vec3(0.0, 0.0, 0.0))
        w = glm.scale(w, glm.vec3(20.0))
        self.FloorWorld = w

        # 立方体
        self.BoxVertices = [
            glm.vec3(0.5),
            glm.vec3(0.5, 0.5, -0.5),
            glm.vec3(0.5, -0.5, 0.5),
            glm.vec3(0.5, -0.5, -0.5),
            glm.vec3(-0.5, 0.5, 0.5),
            glm.vec3(-0.5, 0.5, -0.5),
            glm.vec3(-0.5, -0.5, 0.5),
            glm.vec3(-0.5),
        ]
        self.BoxIndices = [
            0, 1, 2, 1, 3, 2,   # right
            4, 6, 5, 5, 6, 7,   # left
            0, 2, 4, 2, 6, 4,   # front
            1, 5, 3, 3, 5, 7,   # back
            0, 4, 1, 1, 4, 5,   # top
            2, 3, 6, 3, 7, 6,   # bottom
        ]
        # トランスフォーム
        self.World = [ glm.mat4(1.0) for _ in range(5) ]

        # ライトの方向
        self.LightDirection = glm.normalize(glm.vec3(0.0, 1.0, 1.0))

        self.Transformed = []
        self.Screened = []

        # 更新、描画関数を指定して実行
        pyxel.run(self.update, self.draw)
    
    def cameraControl(self):
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
            #sc0 = self.Viewport * sc0
            #sc1 = self.Viewport * sc1
            #sc2 = self.Viewport * sc2
            sc0.x = self.HalfWidth * sc0.x + self.HalfWidth
            sc0.y = -self.HalfHeight * sc0.y + self.HalfHeight
            sc1.x = self.HalfWidth * sc1.x + self.HalfWidth
            sc1.y = -self.HalfHeight * sc1.y + self.HalfHeight
            sc2.x = self.HalfWidth * sc2.x + self.HalfWidth
            sc2.y = -self.HalfHeight * sc2.y + self.HalfHeight

            # 明るさをw成分に格納
            sc0.w = LN
            #sc1.w = LN
            #sc2.w = LN
            self.Screened.append((sc0, sc1, sc2))

    # 更新関数
    def update(self):
        self.cameraControl()
        
        # ワールド変換行列の更新
        for i in range(len(self.World)):
            w = glm.mat4(1.0)
            w = glm.translate(w, glm.vec3((i - (len(self.World) - 1) * 0.5) * 8.0, 5.0, 0.0))
            w = glm.rotate(w, glm.radians(pyxel.frame_count % 360), glm.vec3(1.0, 0.0, 0.0))
            w = glm.rotate(w, glm.radians(pyxel.frame_count % 360), glm.vec3(0.0, 1.0, 0.0))
            w = glm.rotate(w, glm.radians(pyxel.frame_count % 360), glm.vec3(0.0, 0.0, 1.0))
            w = glm.scale(w, glm.vec3(4.0))
            self.World[i] = w

        self.Screened.clear()
        self.drawMesh(self.FloorVertices, self.FloorIndices, self.FloorWorld)  
        for i in range(len(self.World)):
            self.drawMesh(self.BoxVertices, self.BoxIndices, self.World[i])
       
        # z座標でソート（遠い順）
        self.Screened.sort(key = lambda tri: tri[0].z + tri[1].z + tri[2].z, reverse = True)
        #self.Screened.sort(key = lambda tri: max(tri[0].z, tri[1].z, tri[2].z), reverse = True)

    # 描画関数
    def draw(self):
        # 画面クリア
        pyxel.cls(col = 15)

        for v0, v1, v2 in self.Screened:
            c = int(v0.w * 14) + 1
            pyxel.tri(v0.x, v0.y, v1.x, v1.y, v2.x, v2.y, c)
            #pyxel.line(v0.x, v0.y, v1.x, v1.y, c); pyxel.line(v1.x, v1.y, v2.x, v2.y, c); pyxel.line(v2.x, v2.y, v0.x, v0.y, c)
            #pyxel.text(x = v0.x, y = v0.y, s = "{:.5f}".format(v0.z), col = 14); pyxel.text(x = v1.x, y = v1.y, s = "{:.5f}".format(v1.z), col = 14); pyxel.text(x = v2.x, y = v2.y, s = "{:.5f}".format(v2.z), col = 14)
        
            scl0 = (1 - v0.z) * 1000 * 3
            scl1 = (1 - v1.z) * 1000 * 3
            scl2 = (1 - v2.z) * 1000 * 3
            pyxel.blt(x = v0.x - 2 * scl0, y = v0.y - 2 * scl0, img = 0, u = 0, v = 0, w = 8, h = 8, colkey = 0,  rotate = 0, scale = scl0)
            pyxel.blt(x = v1.x - 2 * scl1, y = v1.y - 2 * scl1, img = 0, u = 0, v = 8, w = 8, h = 8, colkey = 0,  rotate = 0, scale = scl1)
            pyxel.blt(x = v2.x - 2 * scl2, y = v2.y - 2 * scl2, img = 0, u = 0, v = 16, w = 8, h = 8, colkey = 0,  rotate = 0, scale = scl2)
App()