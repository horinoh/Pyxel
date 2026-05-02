# title: 
# author: 
# desc: 
# site: 
# license: MIT
# version: 1.0

import pyxel

class App:
    UP = 0; DOWN = 1; LEFT = 2; RIGHT = 3

    # 移動速度、向き
    SpSpeed = 2
    SpDir = DOWN

    # キャラ毎の UV
    SpUVs = (
        (  0,  0 ), # キャラ 0
        (  0,  8 ), # キャラ 1
        (  0, 16 ), # ...
        ( 64,  8 ),
        ( 64, 16 ),
    )
    # 方向毎の U (UV の U)
    SpDirU = (16, 0, 32, 32)

    def __init__(self):
        pyxel.init(width = 320, height = 240, title = "Sprite", fps = 60)
        
        # 画像読み込み (images[0, 2])
        pyxel.images[0].load(x = 0, y = 0, filename = "../noguchi_128x128.png")

        # パレットを初期状態
        pyxel.pal()
        
        # 描画領域を全画面
        pyxel.clip()
        
        # キャラの位置
        self.SpXY = pyxel.width / 2, pyxel.height / 2
        
        # 更新、描画関数を指定して実行
        pyxel.run(self.update, self.draw)
        
    # 更新関数
    def update(self):    
        X, Y = self.SpXY
        if pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_UP, hold = 1, repeat = 1) or pyxel.btnp(pyxel.KEY_W, hold = 1, repeat = 1):
            Y = Y - self.SpSpeed
            self.SpDir = self.UP
        if pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN, hold = 1, repeat = 1) or pyxel.btnp(pyxel.KEY_S, hold = 1, repeat = 1):
            Y = Y + self.SpSpeed
            self.SpDir = self.DOWN
        if pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT, hold = 1, repeat = 1) or pyxel.btnp(pyxel.KEY_A, hold = 1, repeat = 1):
            X = X - self.SpSpeed
            self.SpDir = self.LEFT
        if pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT, hold = 1, repeat = 1) or pyxel.btnp(pyxel.KEY_D, hold = 1, repeat = 1):
            X = X + self.SpSpeed
            self.SpDir = self.RIGHT
        self.SpXY = min(max(X, 0), pyxel.width), min(max(Y, 0), pyxel.height)
        # アイドルアニメーションパターンの U (UV の U)
        self.SpAnimU = 0 if (pyxel.frame_count % 60) < 30 else 8

    # 描画関数
    def draw(self):
        # 画面クリア
        pyxel.cls(col = 0)

        # スプライト
        Scale = 4.0
        # 左右方向で幅の符号を反転する
        W = 8 if self.SpDir == self.RIGHT else -8
        # 各キャラ毎の UV
        i = 0
        for UV in self.SpUVs:
            # 方向、アニメーションの U オフセット
            UOfs = self.SpDirU[self.SpDir] + self.SpAnimU
            # 矩形領域の転送
            pyxel.blt(x = self.SpXY[0], y = self.SpXY[1] +  i * 8 * Scale, img = 0, u = UV[0] + UOfs, v = UV[1], w = W, h = 8, colkey = 0,  rotate = 0, scale = Scale)
            i = i + 1

App()