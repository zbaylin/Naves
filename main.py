from main_window import Ui_MainWindow
from browser import Ui_Browser
from PySide2 import QtCore, QtGui, QtWidgets
from config import config_utils
from config import config
import importlib
import signal
import sys


dataProviders = []


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


class Browser(QtWidgets.QWidget, Ui_Browser):
  def __init__(self):
    super(Browser, self).__init__()
    self.setupUi(self)
    self.items = []
    for provider in dataProviders:
      self.items.extend(provider.run(""))
    for item in self.items:
      listItem = QtWidgets.QListWidgetItem(self.list)
      listItem.setData(QtCore.Qt.UserRole, item)
      listItem.setText(item.title)

    # Connect the search bar to the search function
    self.searchBar.textChanged[str].connect(self.search)
    self.list.itemSelectionChanged.connect(self.showItem)

  def keyPressEvent(self, e):
    if e.key() == QtCore.Qt.Key_Down:
      self.list.setCurrentRow(self.list.currentRow() + 1)
    elif e.key() == QtCore.Qt.Key_Up:
      self.list.setCurrentRow(self.list.currentRow() - 1)
    elif e.key() == QtCore.Qt.Key_Escape:
      sys.exit()

  def search(self):
    term = self.searchBar.text()
    self.items = []
    self.list.clear()
    for provider in dataProviders:
      self.items.extend(provider.run(term))

    for item in self.items:
      listItem = QtWidgets.QListWidgetItem(self.list)
      listItem.setData(QtCore.Qt.UserRole, item)
      listItem.setText(item.title)
  
  def showItem(self):
    item = self.list.currentItem()
    datum = item.data(QtCore.Qt.UserRole)
    self.itemLabel.setText(datum.title)
    self.itemInformation.setText(datum.description)


if __name__ == "__main__":
  app = QtWidgets.QApplication(sys.argv)
  config_utils.load()

  # Import all the specified data providers
  for provider in config.providers:
    dataProviders.append(importlib.import_module("providers." + provider).main())

  mainWindow = MainWindow()
  signal.signal(signal.SIGINT, signal.SIG_DFL)
  ret = app.exec_()
  sys.exit(ret)
