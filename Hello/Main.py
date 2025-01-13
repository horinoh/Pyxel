# title: 
# author: 
# desc: 
# site: 
# license: MIT
# version: 1.0
 
import pyxel

class App:
    def __init__(self):
        pyxel.init(width = 320, height = 240, title = "Hello", fps = 60)
        
        # パレットを初期状態
        pyxel.pal()
        
        # 描画領域を全画面
        pyxel.clip()
        
        # フォントを使用する場合
        self.Font = None
        #self.Font = umplus10 = pyxel.Font("umplus_j10r.bdf")
        #self.Font = umplus10 = pyxel.Font("umplus_j12r.bdf")

        # 更新、描画関数を指定して実行
        pyxel.run(self.update, self.draw)
        
    # 更新関数
    def update(self):
        pass

    # 描画関数
    def draw(self):
        # 画面クリア
        pyxel.cls(col = 0)

        # Hello World
        pyxel.text(x = 10, y = 10, s = "Hello World", col = pyxel.frame_count % 16, font = self.Font)

App()