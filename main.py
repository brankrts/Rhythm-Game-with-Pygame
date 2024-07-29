from game_settings import GameSettings
from PyQt5.QtWidgets import QApplication
import sys


app = QApplication(sys.argv)

def open_lobby():

    global lobby
    lobby = GameSettings()
    lobby.show()

if __name__ == '__main__':
    open_lobby()  
    sys.exit(app.exec_())
