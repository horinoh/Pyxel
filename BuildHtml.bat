@REM BuildPackage.bat 後 (.pyxappがある状態で) に実行すること

@for %%i in (*.pyxapp) do @pyxel app2html %%i