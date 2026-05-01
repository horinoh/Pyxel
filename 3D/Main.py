# title: 
# author: 
# desc: 
# site: 
# license: MIT
# version: 1.0
 
import pyxel
from pyglm import glm

class App:
    def __init__(self):
        pyxel.init(width = 320, height = 240, title = "3D", fps = 60)
        
        # パレットを初期状態
        pyxel.pal()
        # パレットの色を「グレースケール」に書き換える
        for i in range(len(pyxel.colors)):
            pyxel.colors[i] = i * 0x101010

        # 描画領域を全画面
        pyxel.clip()

        # ビュー変換行列
        eye = glm.vec3(0.0, 1.0, 20.0)
        at = glm.vec3(0.0, 0.0, 0.0)
        up = glm.vec3(0.0, 1.0, 0.0)
        self.View = glm.lookAt(eye, at, up)

        # 射影変換行列
        povy = glm.radians(45.0)
        aspect = pyxel.width / pyxel.height
        zn = 0.01
        zf = 100.0 
        self.Projection = glm.perspective(povy, aspect, zn, zf)

        self.ViewProjection = self.Projection * self.View

        self.HalfWidth = pyxel.width // 2
        self.HalfHeight = pyxel.height // 2
        # ビューポート変換行列
        # self.Viewport = glm.mat4(
        #     [self.HalfWidth, 0.0, 0.0, 0.0],
        #     [0.0, -self.HalfHeight, 0.0, 0.0],
        #     [0.0, 0.0, 1.0, 0.0],
        #     [self.HalfWidth, self.HalfHeight, 0.0, 1.0]
        # )

        # 頂点データ
        self.Vertices = [
            glm.vec3(-1, -1, -1), glm.vec3(1, -1, -1), glm.vec3(1, 1, -1), glm.vec3(-1, 1, -1),
            glm.vec3(-1, -1, 1), glm.vec3(1, -1, 1), glm.vec3(1, 1, 1), glm.vec3(-1, 1, 1)
        ]
        # インデックスデータ
        self.Indices = [
            0,3,2, 0,2,1,  # front
            4,7,6, 4,6,5,  # back
            0,4,7, 0,7,3,  # left
            1,5,6, 1,6,2,  # right
            3,7,6, 3,6,2,  # top
            0,4,5, 0,5,1   # bottom
        ]

        self.World = [glm.mat4(1.0), glm.mat4(1.0)]

        self.Transformed = []
        self.Screened = []

        # 更新、描画関数を指定して実行
        pyxel.run(self.update, self.draw)
    
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
            
            n = glm.normalize(glm.cross(glm.vec3(v1) - glm.vec3(v0), glm.vec3(v2) - glm.vec3(v0)))
            N = glm.normalize(glm.mat3(World) * n)
            L = glm.normalize(glm.vec3(0.0, 1.0, 1.0))
            LN = glm.max(0.0, glm.dot(L, N))

            # バックフェイスカリング
            #N = glm.normalize(glm.mat3(vw) * n)
            #print(N.z)
            #if N.z < 0:
            #    print("cull")
            #    continue

            # ビューポート変換
            sc0 /= sc0.w
            sc1 /= sc1.w
            sc2 /= sc2.w
            #sc0 = self.Viewport * sc0
            #sc1 = self.Viewport * sc1
            #sc2 = self.Viewport * sc2
            sc0.x = self.HalfWidth * sc0.x + self.HalfWidth
            sc0.y = -self.HalfHeight * sc0.y + self.HalfHeight
            sc1.x = self.HalfWidth * sc1.x + self.HalfWidth
            sc1.y = -self.HalfHeight * sc1.y + self.HalfHeight
            sc2.x = self.HalfWidth * sc2.x + self.HalfWidth
            sc2.y = -self.HalfHeight * sc2.y + self.HalfHeight

            sc0[3] = LN
            sc1[3] = LN
            sc2[3] = LN
            self.Screened.append((sc0, sc1, sc2))

    # 更新関数
    def update(self):
        # ワールド変換行列の更新
        w = glm.mat4(1.0)
        w = glm.translate(w, glm.vec3(0.0, -15.0, 0.0))
        w = glm.scale(w, glm.vec3(10.0))
        self.World[0] = w

        w = glm.mat4(1.0)
        w = glm.translate(w, glm.vec3(0.0, 0.0, 0.0))
        w = glm.rotate(w, glm.radians(pyxel.frame_count % 360), glm.vec3(0.0, 1.0, 0.0))
        w = glm.rotate(w, glm.radians(pyxel.frame_count % 360), glm.vec3(0.0, 0.0, 1.0))
        w = glm.scale(w, glm.vec3(1.0))
        self.World[1] = w

        self.Screened.clear()
        for i in range(len(self.World)):
            self.drawMesh(self.Vertices, self.Indices, self.World[i])
        # z座標でソート（遠い順）
        self.Screened.sort(key = lambda tri: tri[0].z + tri[1].z + tri[2].z, reverse = True)

    # 描画関数
    def draw(self):
        # 画面クリア
        pyxel.cls(col = 7)

        for v0, v1, v2 in self.Screened:
            c = int(v0.w * 15)
            pyxel.tri(v0.x, v0.y, v1.x, v1.y, v2.x, v2.y, c)
            pyxel.line(v0.x, v0.y, v1.x, v1.y, c);pyxel.line(v1.x, v1.y, v2.x, v2.y, c);pyxel.line(v2.x, v2.y, v0.x, v0.y, c)

App()