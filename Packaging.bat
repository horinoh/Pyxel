REM @for %%i in (*.pyxapp) do @del %%i

@for /d %%i in (*) do @pyxel package %%i %%i/Main.py
