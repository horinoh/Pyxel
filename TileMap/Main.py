# title: 
# author: 
# desc: 
# site: 
# license: MIT
# version: 1.0
 
import pyxel

class App:
    TileSize = 8
    Tiles = (16, 16)
    
    def __init__(self):
        pyxel.init(width = 320, height = 240, title = "TileMap", fps = 60)
        
        # パレットを初期状態
        pyxel.pal()
        
        # 描画領域を全画面
        pyxel.clip()

        # イメージ 0 (画像読み込み)
        pyxel.images[0].load(x = 0, y = 0, filename = "noguchi_128x128.png")
        # イメージ 1 
        # 0:黒、4:茶, 8:赤, f:肌
        pyxel.images[1].set(x=0, y=0, data = [
            "0000088888000000",
            "0000888888888000",
            "0000444ff4f00000",
            "0004f4fff4fff000",
            "0004f44fff4fff00",
            "00044ffff4444000",
            "00000fffffff0000",
            "0000448444000000",
            "0004448448444000",
            "0044448888444400",
            "00ff48f88f84ff00",
            "00fff888888fff00",
            "00ff88888888ff00",
            "0000888008880000",
            "0004440000444000",
            "0044440000444400",
        ])

        # タイルマップ 0 (イメージ 0 使用)
        pyxel.tilemaps[0].imgsrc = 0
        # 上位 2 桁が X、下位 2 桁が Y を表している、ここでは 16 x 16 タイル (= 128 x 128)
        pyxel.tilemaps[0].set(x = 0, y = 0, data = [ 
            # Tile(X, Y) = (0, 0)=0000, (1, 0)=0100, ... (f, 0)=0f00 
            "0000 0100 0200 0300 0400 0500 0600 0700 0800 0900 0a00 0b00 0c00 0d00 0e00 0f00", 
            "0001 0101 0201 0301 0401 0501 0601 0701 0801 0901 0a01 0b01 0c01 0d01 0e01 0f01", 
            "0002 0102 0202 0302 0402 0502 0602 0702 0802 0902 0a02 0b02 0c02 0d02 0e02 0f02", 
            "0003 0103 0203 0303 0403 0503 0603 0703 0803 0903 0a03 0b03 0c03 0d03 0e03 0f03", 
            "0004 0104 0204 0304 0404 0504 0604 0704 0804 0904 0a04 0b04 0c04 0d04 0e04 0f04", 
            "0005 0105 0205 0305 0405 0505 0605 0705 0805 0905 0a05 0b05 0c05 0d05 0e05 0f05", 
            "0006 0106 0206 0306 0406 0506 0606 0706 0806 0906 0a06 0b06 0c06 0d06 0e06 0f06", 
            "0007 0107 0207 0307 0407 0507 0607 0707 0807 0907 0a07 0b07 0c07 0d07 0e07 0f07", 
            "0008 0108 0208 0308 0408 0508 0608 0708 0808 0908 0a08 0b08 0c08 0d08 0e08 0f08", 
            "0009 0109 0209 0309 0409 0509 0609 0709 0809 0909 0a09 0b09 0c09 0d09 0e09 0f09", 
            "000a 010a 020a 030a 040a 050a 060a 070a 080a 090a 0a0a 0b0a 0c0a 0d0a 0e0a 0f0a", 
            "000b 010b 020b 030b 040b 050b 060b 070b 080b 090b 0a0b 0b0b 0c0b 0d0b 0e0b 0f0b", 
            "000c 010c 020c 030c 040c 050c 060c 070c 080c 090c 0a0c 0b0c 0c0c 0d0c 0e0c 0f0c", 
            "000d 010d 020d 030d 040d 050d 060d 070d 080d 090d 0a0d 0b0d 0c0d 0d0d 0e0d 0f0d", 
            "000e 010e 020e 030e 040e 050e 060e 070e 080e 090e 0a0e 0b0e 0c0e 0d0e 0e0e 0f0e", 
            "000f 010f 020f 030f 040f 050f 060f 070f 080f 090f 0a0f 0b0f 0c0f 0d0f 0e0f 0f0f", 
        ])

        # タイルマップ 1 (イメージ 0 使用)
        pyxel.tilemaps[1].imgsrc = 0
        # タイルデータをプログラムで生成
        data = []
        for y in range(0, self.Tiles[1]):
            line = ""
            for x in range(0, self.Tiles[0]):
                # そのまま (タイルマップ 0 と同じ)
                #line = line + f"{x:02x}{y:02x} "
                # XY を転置したもの
                line = line + f"{y:02x}{x:02x} "
            data.append(line)
        pyxel.tilemaps[1].set(x = 0, y = 0, data = data)

        # タイルマップ 2 (イメージ 1 使用)
        pyxel.tilemaps[2].imgsrc = 1
        data1 = []
        for y in range(0, self.Tiles[1]):
            line = ""
            for x in range(0, self.Tiles[0]):
                # 2x2 タイル (= 16x16) の繰り返し
                line = line + f"{(x & 1):02x}{(y & 1):02x} "
            data1.append(line)
        pyxel.tilemaps[2].set(x = 0, y = 0, data = data1)

        # 更新、描画関数を指定して実行
        pyxel.run(self.update, self.draw)
        
    # 更新関数
    def update(self):
        pass

    # 描画関数
    def draw(self):
        # 画面クリア
        pyxel.cls(col = 0)
       
        # タイルマップ描画
        w = self.TileSize * self.Tiles[0]
        h = self.TileSize * self.Tiles[1]
        x = pyxel.width // 2 - w // 2
        y = pyxel.height // 2 - h // 2

        # タイルマップ 2 
        pyxel.bltm(x = x, y = y, tm = 2, u = 0, v = 0, w = w, h = h, colkey = 0, rotate = pyxel.frame_count % 360, scale = 2)
        # タイルマップ 1 (右)
        pyxel.bltm(x = x + w // 2 + 8, y = y, tm = 1, u = 0, v = 0, w = w, h = h, colkey = 0, rotate = 0, scale = 1)
         # タイルマップ 0 (左)
        pyxel.bltm(x = x - w // 2 - 8, y = y, tm = 0, u = 0, v = 0, w = w, h = h, colkey = 0, rotate = 0, scale = 1)
       
App()