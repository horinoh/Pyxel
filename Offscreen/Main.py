# title: 
# author: 
# desc: 
# site: 
# license: MIT
# version: 1.0
 
import pyxel

class App:
    def __init__(self):
        pyxel.init(width = 320, height = 240, title = "Offscreen", fps = 60)
        
        # パレットを初期状態
        pyxel.pal()
        
        # 描画領域を全画面
        pyxel.clip()
        
        # バックバッファの準備
        self.Backbuffer = pyxel.Image(pyxel.width, pyxel.height)
        
        self.IsRaster = True

        # 更新、描画関数を指定して実行
        pyxel.run(self.update, self.draw)
        
    # 更新関数
    def update(self):
        if pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A) or pyxel.btnp(pyxel.KEY_A):
            self.IsRaster = False if self.IsRaster else True

    # 描画関数
    def draw(self):
        # バックバッファクリア
        self.Backbuffer.cls(col = 0)

        # バックバッファへ描画
        for i in range(0, self.Backbuffer.height // pyxel.FONT_HEIGHT):
            self.Backbuffer.text(x = self.Backbuffer.width // 2, y = i * pyxel.FONT_HEIGHT, s = "Hello World", col = 7, font = None)

        if self.IsRaster:
            # バックバッファを画面へ転送 (ラスタースクロール)
            for i in range(0, self.Backbuffer.height):
                c = pyxel.cos(deg = (pyxel.frame_count + i) % 360)
                pyxel.blt(x = c * 50, y = i, img = self.Backbuffer, u = 0, v = i, w = self.Backbuffer.width, h = 1)
        else:
            # バックバッファを画面へ転送
           pyxel.blt(x = 0, y = 0, img = self.Backbuffer, u = 0, v = 0, w = self.Backbuffer.width, h = self.Backbuffer.height)

App()