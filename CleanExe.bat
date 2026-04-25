@for %%i in (*.spec) do @del %%i

@rmdir /s /q dist
@rmdir /s /q build