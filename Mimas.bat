@ECHO OFF
pyinstaller.exe --onefile --paths c:\Users\krzysztof.filipowicz\PycharmProjects\SBReader\venv\Lib\site-packages\ --icon=Mimas.ico main.py --name=Mimas --windowed
pause