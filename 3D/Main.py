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
        
        # 描画領域を全画面
        pyxel.clip()

        # ビュー変換行列
        eye = glm.vec3(0.0, 0.0, 10.0)
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

        self.World = glm.mat4(1.0)

        # ビューポート変換行列
        # w2 = pyxel.width // 2
        # h2 = pyxel.height // 2
        # self.Viewport = glm.mat4(
        #     [w2, 0.0, 0.0, 0.0],
        #     [0.0, -h2, 0.0, 0.0],
        #     [0.0, 0.0, 1.0, 0.0],
        #     [w2, h2, 0.0, 1.0]
        # )

        # 頂点データ
        self.Vertices = [
            glm.vec3(-1, 0, 0), glm.vec3(1, 0, 0), glm.vec3(0, 1, 0),
            glm.vec3(-1, 0, 0), glm.vec3(1, 0, 0), glm.vec3(0, 0.5, 0),
            glm.vec3(-1, 0, 0), glm.vec3(1, 0, 0), glm.vec3(0, 0.25, 0),
            glm.vec3(-1, 0, 0), glm.vec3(1, 0, 0), glm.vec3(0, 0.125, 0),
        ]
        # インデックスデータ
        self.Indices = [
            0, 1, 2, 
            3, 4, 5,
            6, 7, 8,
            9, 10, 11,
        ]

        self.Transformed = []

        # 更新、描画関数を指定して実行
        pyxel.run(self.update, self.draw)
        
    # 更新関数
    def update(self):
        vpw = self.ViewProjection * self.World

        self.Transformed.clear()
        for i in range(0, len(self.Indices), 3):
            v0 = glm.vec4(self.Vertices[self.Indices[i]], 1.0)
            v1 = glm.vec4(self.Vertices[self.Indices[i + 1]], 1.0)
            v2 = glm.vec4(self.Vertices[self.Indices[i + 2]], 1.0)
            v0 = vpw * v0
            v1 = vpw * v1
            v2 = vpw * v2
            # クリッピング
            if v0[3] <= 0 or v1[3] <= 0 or v2[3] <= 0:
                continue
             # バックフェイスカリング
            if glm.cross(glm.vec3(v1) - glm.vec3(v0), glm.vec3(v2) - glm.vec3(v0)).z <= 0:
                continue
            # スクリーン座標に変換
            v0 /= v0[3]
            v1 /= v1[3]
            v2 /= v2[3]
            #v0 = self.Viewport * v0
            #v1 = self.Viewport * v1
            #v2 = self.Viewport * v2
            w2 = pyxel.width // 2
            h2 = pyxel.height // 2
            v0[0] = w2 * v0[0] + w2
            v0[1] = -h2 * v0[1] + h2
            v1[0] = w2 * v1[0] + w2
            v1[1] = -h2 * v1[1] + h2
            v2[0] = w2 * v2[0] + w2
            v2[1] = -h2 * v2[1] + h2
            self.Transformed.append((v0, v1, v2))

        # z座標でソート（遠い順）
        self.Transformed.sort(key = lambda tri: tri[0][2] + tri[1][2] + tri[2][2], reverse = True)

        # ワールド変換行列の更新
        self.World = glm.mat4(1.0)
        self.World = glm.translate(self.World, glm.vec3(0.0, 0.0, 0.0))
        self.World = glm.rotate(self.World, glm.radians(pyxel.frame_count % 360), glm.vec3(0.0, 1.0, 0.0))
        self.World = glm.scale(self.World, glm.vec3(1.0))

    # 描画関数
    def draw(self):
        # 画面クリア
        pyxel.cls(col = 0)

        c = 7
        for v0, v1, v2 in self.Transformed:
            pyxel.tri(v0[0], v0[1], v1[0], v1[1], v2[0], v2[1], c)
            # pyxel.line(v0[0], v0[1], v1[0], v1[1], c)
            # pyxel.line(v1[0], v1[1], v2[0], v2[1], c)
            # pyxel.line(v2[0], v2[1], v0[0], v0[1], c)
            c += 1
            c %= 16

App()