from main_window import Ui_MainWindow
from browser import Ui_Browser
from PySide2 import QtCore, QtGui, QtWidgets
from config import config_utils
from config import config
import signal
import sys


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
  def __init__(self):
    super(MainWindow, self).__init__()
    self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
    self.setupUi(self)

    # Set the theme of the window
    # Propagates downward to every child widget
    if config.theme:
      stylesheet = open("themes/" + config.theme + ".qss", "r").read()
      self.setStyleSheet(stylesheet)

    # Set window size according to config
    if config.width and config.height:
      self.resize(config.width, config.height)

    # Move the window to the center of the screen
    rect = self.frameGeometry()
    centerPoint = QtWidgets.QDesktopWidget().availableGeometry().center()
    rect.moveCenter(centerPoint)
    self.move(rect.topLeft())

    # Create a browser instance
    browser = Browser()
    self.setCentralWidget(browser)

    # Show the window
    self.show()

  def keyPressEvent(self, e):
    if e.key() == QtCore.Qt.Key_Escape:
      sys.exit()


class Browser(QtWidgets.QWidget, Ui_Browser):
  def __init__(self):
    super(Browser, self).__init__()
    self.setupUi(self)


if __name__ == "__main__":
  app = QtWidgets.QApplication(sys.argv)
  config_utils.load()

  mainWindow = MainWindow()
  signal.signal(signal.SIGINT, signal.SIG_DFL)
  ret = app.exec_()
  sys.exit(ret)
