# title: 
# author: 
# desc: 
# site: 
# license: MIT
# version: 1.0

import pyxel
import random

class App:
    def __init__(self):
        pyxel.init(width = 320, height = 240, title = "Palette", fps = 60)
        
        # パレットを初期状態
        pyxel.pal()

        # デフォルトのパレットを退避
        self.Colors = pyxel.colors.to_list()

        # 描画領域を全画面
        pyxel.clip()
                
        # 更新、描画関数を指定して実行
        pyxel.run(self.update, self.draw)
        
    # 更新関数
    def update(self): 
        if pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A, hold = 30, repeat = 1) or pyxel.btnp(pyxel.KEY_A, hold = 30, repeat = 1):
            # 背景色 0 へ、パレットの中からランダムでセットする
            pyxel.pal(col1 = 0, col2 = random.randint(0, len(pyxel.colors) - 1))
        if pyxel.btnp(pyxel.GAMEPAD1_BUTTON_B) or pyxel.btnp(pyxel.KEY_B):
            # デフォルトのパレットを復元
            pyxel.colors.from_list(self.Colors)
            # 背景色 0 へパレット 0 をセット
            pyxel.pal(col1 = 0, col2 = 0)
        if pyxel.btnp(pyxel.GAMEPAD1_BUTTON_X) or pyxel.btnp(pyxel.KEY_X):
            # パレットの色を「ランダム」に書き換える
            for i in range(len(pyxel.colors)):
                pyxel.colors[i] = (random.randint(0x0, 0xff) << 16) | (random.randint(0x0, 0xff) << 8) | (random.randint(0x0, 0xff) << 0)
        if pyxel.btnp(pyxel.GAMEPAD1_BUTTON_Y) or pyxel.btnp(pyxel.KEY_Y):
            # パレットの色を「グレースケール」に書き換える
            for i in range(len(pyxel.colors)):
                pyxel.colors[i] = i * 0x101010

    # 描画関数
    def draw(self):
        # 画面クリア
        pyxel.cls(col = 0)

        # パレット
        i = 0
        for RGB in pyxel.colors:
            R = (RGB >> 16) & 0xff
            G = (RGB >>  8) & 0xff
            B = (RGB >>  0) & 0xff
            pyxel.text(x = 10, y = 10 + (i + 1) * pyxel.FONT_HEIGHT, s = "[%02d] 0x%06x (%03d, %03d, %03d)" % (i, RGB, R, G, B), col = i, font = None)
            i = i + 1
App()