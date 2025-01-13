# title: 
# author: 
# desc: 
# site: 
# license: MIT
# version: 1.0

import pyxel

class App:
    # デジタルボタン用定義
    DOWN = 1 << 0
    RIGHT = 1 << 1
    LEFT = 1 << 2
    UP = 1 << 3
    A = 1 << 4
    B = 1 << 5
    X = 1 << 6
    Y = 1 << 7
    START = 1 << 8
    BACK = 1 << 9
    GUIDE = 1 << 10
    L1 = 1 << 11
    R1 = 1 << 12
    L3 = 1 << 13
    R3 = 1 << 14

    def __init__(self):
        pyxel.init(width = 320, height = 240, title = "GamePad", fps = 60)
        
        # 描画領域を全画面
        pyxel.clip()
        
         # デジタルボタン初期化
        self.DButtons = 0

        # 更新、描画関数を指定して実行
        pyxel.run(self.update, self.draw)
        
    # 更新関数
    def update(self):
        # デジタルボタン
        if pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN, hold = 1, repeat = 1):
            self.DButtons = self.DButtons | self.DOWN
        else:
            self.DButtons = self.DButtons & ~self.DOWN
        if pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT, hold = 1, repeat = 1):
            self.DButtons = self.DButtons | self.RIGHT
        else:
            self.DButtons = self.DButtons & ~self.RIGHT
        if pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT, hold = 1, repeat = 1):
            self.DButtons = self.DButtons | self.LEFT
        else:
            self.DButtons = self.DButtons & ~self.LEFT
        if pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_UP, hold = 1, repeat = 1):
            self.DButtons = self.DButtons | self.UP
        else:
            self.DButtons = self.DButtons & ~self.UP

        if pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A, hold = 1, repeat = 1):
            self.DButtons = self.DButtons | self.A
        else:
            self.DButtons = self.DButtons & ~self.A
        if pyxel.btnp(pyxel.GAMEPAD1_BUTTON_B, hold = 1, repeat = 1):
            self.DButtons = self.DButtons | self.B
        else:
            self.DButtons = self.DButtons & ~self.B
        if pyxel.btnp(pyxel.GAMEPAD1_BUTTON_X, hold = 1, repeat = 1):
            self.DButtons = self.DButtons | self.X
        else:
            self.DButtons = self.DButtons & ~self.X
        if pyxel.btnp(pyxel.GAMEPAD1_BUTTON_Y, hold = 1, repeat = 1):
            self.DButtons = self.DButtons | self.Y
        else:
            self.DButtons = self.DButtons & ~self.Y

        if pyxel.btnp(pyxel.GAMEPAD1_BUTTON_START, hold = 1, repeat = 1):
            self.DButtons = self.DButtons | self.START
        else:
            self.DButtons = self.DButtons & ~self.START
        if pyxel.btnp(pyxel.GAMEPAD1_BUTTON_BACK, hold = 1, repeat = 1):
            self.DButtons = self.DButtons | self.BACK
        else:
            self.DButtons = self.DButtons & ~self.BACK
        if pyxel.btnp(pyxel.GAMEPAD1_BUTTON_GUIDE, hold = 1, repeat = 1):
            self.DButtons = self.DButtons | self.GUIDE
        else:
            self.DButtons = self.DButtons & ~self.GUIDE

        if pyxel.btnp(pyxel.GAMEPAD1_BUTTON_LEFTSHOULDER, hold = 1, repeat = 1):
            self.DButtons = self.DButtons | self.L1
        else:
            self.DButtons = self.DButtons & ~self.L1
        if pyxel.btnp(pyxel.GAMEPAD1_BUTTON_RIGHTSHOULDER, hold = 1, repeat = 1):
            self.DButtons = self.DButtons | self.R1
        else:
            self.DButtons = self.DButtons & ~self.R1

        if pyxel.btnp(pyxel.GAMEPAD1_BUTTON_LEFTSTICK, hold = 1, repeat = 1):
            self.DButtons = self.DButtons | self.L3
        else:
            self.DButtons = self.DButtons & ~self.L3
        if pyxel.btnp(pyxel.GAMEPAD1_BUTTON_RIGHTSTICK, hold = 1, repeat = 1):
            self.DButtons = self.DButtons | self.R3
        else:
            self.DButtons = self.DButtons & ~self.R3

        # アナログスティック、トリガー (要 Xinput ゲームパッド)
        self.LS = pyxel.btnv(pyxel.GAMEPAD1_AXIS_LEFTX), pyxel.btnv(pyxel.GAMEPAD1_AXIS_LEFTY)
        self.RS = pyxel.btnv(pyxel.GAMEPAD1_AXIS_RIGHTX), pyxel.btnv(pyxel.GAMEPAD1_AXIS_RIGHTY)
        self.L2 = pyxel.btnv(pyxel.GAMEPAD1_AXIS_TRIGGERLEFT)
        self.R2 = pyxel.btnv(pyxel.GAMEPAD1_AXIS_TRIGGERRIGHT)

    # 描画関数
    def draw(self):
        # 画面クリア
        pyxel.cls(col = 0)

        # ボタン状態 (テキスト表示)
        pyxel.text(x = 10, y = 10 + pyxel.FONT_HEIGHT * 1, s = "LS:(%06d, %06d) LT:%05d" % (self.LS[0], self.LS[1], self.L2), col = 7, font = None)
        pyxel.text(x = 10, y = 10 + pyxel.FONT_HEIGHT * 2, s = "RS:(%06d, %06d) RT:%05d" % (self.RS[0], self.RS[1], self.R2), col = 7, font = None)
        pyxel.text(x = 10, y = 10 + pyxel.FONT_HEIGHT * 3, s = "BTN:%04x" % self.DButtons, col = 7, font = None)

        # ボタン状態 (グラフィック表示)
        # DPAD
        X = 20
        Y = 200
        pyxel.circb(x = X, y = Y + 10, r = 5, col = 7)
        pyxel.circb(x = X + 10, y = Y, r = 5, col = 7)
        pyxel.circb(x = X - 10, y = Y, r = 5, col = 7)
        pyxel.circb(x = X, y = Y - 10, r = 5, col = 7)
        if self.DButtons & self.DOWN:
            pyxel.circ(x = X, y = Y + 10, r = 5, col = 7)
        if self.DButtons & self.RIGHT:
            pyxel.circ(x = X + 10, y = Y, r = 5, col = 7)
        if self.DButtons & self.LEFT:
            pyxel.circ(x = X - 10, y = Y, r = 5, col = 7)
        if self.DButtons & self.UP:
            pyxel.circ(x = X, y = Y - 10, r = 5, col = 7)
    
        # A, B, X, Y
        X = 120
        pyxel.circb(x = X, y = Y + 10, r = 5, col = 7)
        pyxel.circb(x = X + 10, y = Y, r = 5, col = 7)
        pyxel.circb(x = X - 10, y = Y, r = 5, col = 7)
        pyxel.circb(x = X, y = Y - 10, r = 5, col = 7)
        if self.DButtons & self.A:
            pyxel.circ(x = X, y = Y + 10, r = 5, col = 7)
        if self.DButtons & self.B:
            pyxel.circ(x = X + 10, y = Y, r = 5, col = 7)
        if self.DButtons & self.X:
            pyxel.circ(x = X - 10, y = Y, r = 5, col = 7)
        if self.DButtons & self.Y:
            pyxel.circ(x = X, y = Y - 10, r = 5, col = 7)

        # STAET, BACK, GUIDE
        X = 70
        Y = 190
        pyxel.circb(x = X + 15, y = Y, r = 5, col = 7)
        if self.DButtons & self.START:
            pyxel.circ(x = X + 15, y = Y, r = 5, col = 7)
        pyxel.circb(x = X - 15, y = Y, r = 5, col = 7)
        if self.DButtons & self.BACK:
            pyxel.circ(x = X - 15, y = Y, r = 5, col = 7)
        pyxel.circb(x = X, y = Y, r = 5, col = 7)
        if self.DButtons & self.GUIDE:
            pyxel.circ(x = X, y = Y, r = 5, col = 7)

        # LS, RS, L3, R3
        X = 50
        Y = 220
        pyxel.circb(x = X + self.LS[0] * 8 / 32767, y = Y + self.LS[1] * 8 / 32767, r = 5, col = 7)
        if self.DButtons & self.L3:
            pyxel.circ(x = X + self.LS[0] * 8 / 32767, y = Y + self.LS[1] * 8 / 32767, r = 5, col = 7)
        X = 90
        pyxel.circb(x = X+ self.RS[0] * 8 / 32767, y = Y+ self.RS[1] * 8 / 32767, r = 5, col = 7)
        if self.DButtons & self.R3:
            pyxel.circ(x = X+ self.RS[0] * 8 / 32767, y = Y+ self.RS[1] * 8 / 32767, r = 5, col = 7)

        # L1, R1
        X = 20
        Y = 170
        pyxel.circb(x = X, y = Y, r = 5, col = 7)
        if self.DButtons & self.L1:
            pyxel.circ(x = X, y = Y, r = 5, col = 7)
        X = 120
        pyxel.circb(x = X, y = Y, r = 5, col = 7)
        if self.DButtons & self.R1:
            pyxel.circ(x = X, y = Y, r = 5, col = 7)

        # L2, R2
        X = 20
        Y = 150
        pyxel.rectb(x = X - 4, y = Y - 8, w = 8, h = 16, col = 7)
        pyxel.rect(x = X - 4, y = Y - 8, w = 8, h = self.L2 * 16 / 32767, col = 7)
        X = 120
        pyxel.rectb(x = X - 4, y = Y - 8, w = 8, h = 16, col = 7)
        pyxel.rect(x = X - 4, y = Y - 8, w = 8, h = self.R2 * 16 / 32767, col = 7)

App()