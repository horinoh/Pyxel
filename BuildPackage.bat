REM @for %%i in (*.pyxapp) do @del %%i

@for /d %%i in (*) do @pyxel package %%i %%i/Main.py

REM 要 PyInstaller
@for /d %%i in (*.pyxapp) do @pyxel app2exe %%i
