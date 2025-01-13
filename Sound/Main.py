# title: 
# author: 
# desc: 
# site: 
# license: MIT
# version: 1.0
 
import pyxel

class App:
    def __init__(self):
        pyxel.init(width = 320, height = 240, title = "Sound", fps = 60)
        
        # パレットを初期状態
        pyxel.pal()
        
        # 描画領域を全画面
        pyxel.clip()
        
        # サウンド定義
        pyxel.sounds[0].set(
            # c0:ド, d0:レ, e0:ミ, f0:ファ, g0:ソ a0:ラ b0:シ, c1:ド, ...
            notes = "c0d0e0f0g0a0b0c1", 
            # t:三角波, s:矩形波, p:パルス波, n:ノイズ
            tones = "t", 
            # ボリューム [0, 7]
            volumes = "6", 
            # n:無し, s:スライド, v:ビブラート, f:フェードアウト
            effects = "n", 
            # 速度 (大きい程 遅い)
            speed = 30)
        pyxel.sounds[1].set(notes = "c1b0a0g0f0e0d0c0", tones = "s", volumes = "6", effects = "n", speed = 30)
        pyxel.sounds[2].set(notes = "c0d0e0f0g0a0b0c1", tones = "p", volumes = "6", effects = "n", speed = 30)
        pyxel.sounds[3].set(notes = "c1b0a0g0f0e0d0c0", tones = "n", volumes = "6", effects = "n", speed = 30)

        # ミュージック定義 (各チャンネルでサウンド 0, 1, 2, 3)
        pyxel.musics[0].set([0], [1], [2], [3])

        # 更新、描画関数を指定して実行
        pyxel.run(self.update, self.draw)
        
    # 更新関数
    def update(self):
        if pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A) or pyxel.btnp(pyxel.KEY_A):
            # playm() ミュージックを鳴らす
            pyxel.playm(msc = 0, loop = False)
        if pyxel.btnp(pyxel.GAMEPAD1_BUTTON_B) or pyxel.btnp(pyxel.KEY_B):
            pyxel.stop()
        if pyxel.btnp(pyxel.GAMEPAD1_BUTTON_X) or pyxel.btnp(pyxel.KEY_X):
            # play() サウンドを鳴らす
            pyxel.play(ch = 0, snd = [0], loop = False)
        if pyxel.btnp(pyxel.GAMEPAD1_BUTTON_Y) or pyxel.btnp(pyxel.KEY_Y):
            pyxel.play(ch = 1, snd = [1], loop = False)
        if pyxel.btnp(pyxel.GAMEPAD1_BUTTON_LEFTSHOULDER) or pyxel.btnp(pyxel.KEY_L):
            pyxel.play(ch = 2, snd = [2], loop = False)
        if pyxel.btnp(pyxel.GAMEPAD1_BUTTON_RIGHTSHOULDER) or pyxel.btnp(pyxel.KEY_R):
            pyxel.play(ch = 3, snd = [3], loop = False)
    # 描画関数
    def draw(self):
        # 画面クリア
        pyxel.cls(col = 0)

App()