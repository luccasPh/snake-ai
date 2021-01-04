import sys
from PyQt5 import QtWidgets

from src.config import Window

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec_())