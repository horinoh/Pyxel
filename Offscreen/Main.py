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
        
        # 更新、描画関数を指定して実行
        pyxel.run(self.update, self.draw)
        
    # 更新関数
    def update(self):
        pass

    # 描画関数
    def draw(self):
        # バックバッファクリア
        self.Backbuffer.cls(col = 1)

        # バックバッファへ描画
        self.Backbuffer.text(x = 10, y = 10, s = "Hello World", col = 7, font = None)

        # バックバッファを画面へ転送
        pyxel.blt(0, 0, self.Backbuffer, 0, 0, self.Backbuffer.width, self.Backbuffer.height)

App()