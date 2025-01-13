# title: 
# author: 
# desc: 
# site: 
# license: MIT
# version: 1.0
 
import random
import pyxel

class App:
    def __init__(self):
        pyxel.init(width = 320, height = 240, title = "Draw", fps = 60)

        # パレットを初期状態
        pyxel.pal()
        
        # 描画領域を全画面
        pyxel.clip()

        # 更新、描画関数を指定して実行
        pyxel.run(self.update, self.draw)
        
    # 更新関数
    def update(self):    
        pass

    # 描画関数
    def draw(self):
        # 画面クリア
        pyxel.cls(col = 0)

        # 矩形
        for i in range(16):
            x = random.randint(0, pyxel.width) 
            y = random.randint(0, pyxel.height)
            pyxel.rect(x = x, y = y, w = 10, h = 10, col = i % 16)

        # 円
        for i in range(16):
            x = random.randint(0, pyxel.width) 
            y = random.randint(0, pyxel.height)
            pyxel.circ(x = x, y = y, r = 10, col = i % 16)

        # 楕円
        for i in range(16):
            x = random.randint(0, pyxel.width) 
            y = random.randint(0, pyxel.height)
            pyxel.elli(x = x, y = y, w = 20, h = 10, col = i % 16)
        
        # 三角形
        for i in range(16):
            x = random.randint(0, pyxel.width) 
            y = random.randint(0, pyxel.height)
            pyxel.tri(x1 = -10 + x, y1 = 10 + y, x2 = 10 + x, y2 = 10 + y, x3 = 0 + x, y3 = 0 + y, col = i % 16)
        
        # 線
        for i in range(16):
            x = random.randint(0, pyxel.width) 
            y = random.randint(0, pyxel.height)
            pyxel.line(x1 = -10 + x, y1 = 0 + y, x2 = 10 + x, y2 = 10 + y, col = i % 16)

App()