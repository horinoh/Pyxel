@REM BuildPackage.bat 後 (.pyxappがある状態で) に実行すること

@REM 要 PyInstaller
@for %%i in (*.pyxapp) do @pyxel app2exe %%i


