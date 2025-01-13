# title: 
# author: 
# desc: 
# site: 
# license: MIT
# version: 1.0

import pyxel

class App:
    def __init__(self):
        pyxel.init(width = 320, height = 240, title = "Mouse", fps = 60)
        
        # マウスカーソルの表示
        pyxel.mouse(True)

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

        # マウス情報
        pyxel.text(x = pyxel.mouse_x, y = pyxel.mouse_y, s = "  (X = %d, Y = %d, Wheel = %d)" % (pyxel.mouse_x, pyxel.mouse_y, pyxel.mouse_wheel), col = 7, font = None)

App()