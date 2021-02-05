from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QAction, QMessageBox
from PyQt5.QtGui import QIntValidator
import sys
import sqlite3
from sqlite3 import Error

DATABASE_PATH = 'settings.sqlite'
window, app, database = None, None, None


# database object that will be used to communicate with the sqlite db
class SettingsDatabase:
    def __init__(self, path):
        self.path = path
        self.con, self.cur = self.connect(path)

    # establish connection with sqlite db
    def connect(self, path):
        try:
            con = sqlite3.connect(path)
            cur = con.cursor()
        except sqlite3.Error:
            print('Sql error occurred...')
            return

        return con, cur

    # returns connection object
    def get_con(self):
        return self.con

    # returns cursor object
    def get_cur(self):
        return self.cur

    # commits changes in sqlite database
    def commit(self):
        self.con.commit()

    # returns fetched results from custom request
    def request(self, request):
        try:
            res = self.con.execute(request).fetchall()
            return res
        except Exception as e:
            print('Request error:', e)
            return


# PyQT Settings window
class MainWindow(object):
    # constructs the settings window components
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(640, 269)

        self.intValidator = QIntValidator()
        quit = QAction("Quit", self)
        quit.triggered.connect(self.closeEvent)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.fps = QtWidgets.QSlider(self.centralwidget)
        self.fps.setGeometry(QtCore.QRect(70, 20, 551, 20))
        self.fps.setOrientation(QtCore.Qt.Horizontal)
        self.fps.setMinimum(30)
        self.fps.setMaximum(90)
        self.fps.setSingleStep(5)
        self.fps.valueChanged.connect(self.slider_value_changed)
        self.fps.setObjectName("fps")

        self.fps_label = QtWidgets.QLabel(self.centralwidget)
        self.fps_label.setGeometry(QtCore.QRect(10, 20, 61, 16))

        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)

        self.fps_label.setFont(font)
        self.fps_label.setObjectName("fps_label")

        self.resolution_header = QtWidgets.QLabel(self.centralwidget)
        self.resolution_header.setGeometry(QtCore.QRect(10, 50, 61, 16))

        font = QtGui.QFont()
        font.setItalic(False)
        font.setUnderline(False)

        self.resolution_header.setFont(font)
        self.resolution_header.setObjectName("resolution_header")

        self.width_label = QtWidgets.QLabel(self.centralwidget)
        self.width_label.setGeometry(QtCore.QRect(10, 80, 41, 16))

        font = QtGui.QFont()
        font.setBold(True)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(75)

        self.width_label.setFont(font)
        self.width_label.setObjectName("width_label")

        self.width = QtWidgets.QLineEdit(self.centralwidget)
        self.width.setGeometry(QtCore.QRect(60, 80, 141, 20))
        self.width.setValidator(self.intValidator)
        self.width.textChanged.connect(self.on_value_changed)
        self.width.setObjectName("width")

        self.height_label = QtWidgets.QLabel(self.centralwidget)
        self.height_label.setGeometry(QtCore.QRect(230, 80, 41, 16))

        font = QtGui.QFont()
        font.setBold(True)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(75)

        self.height_label.setFont(font)
        self.height_label.setObjectName("height_label")

        self.height = QtWidgets.QLineEdit(self.centralwidget)
        self.height.setGeometry(QtCore.QRect(280, 80, 141, 20))
        self.height.setValidator(self.intValidator)
        self.height.textChanged.connect(self.on_value_changed)
        self.height.setObjectName("height")

        self.text_header = QtWidgets.QLabel(self.centralwidget)
        self.text_header.setGeometry(QtCore.QRect(10, 110, 61, 16))

        font = QtGui.QFont()
        font.setItalic(False)
        font.setUnderline(False)

        self.text_header.setFont(font)
        self.text_header.setObjectName("text_header")

        self.text_label = QtWidgets.QLabel(self.centralwidget)
        self.text_label.setGeometry(QtCore.QRect(10, 140, 81, 16))

        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)

        self.text_label.setFont(font)
        self.text_label.setObjectName("text_label")

        self.text = QtWidgets.QSlider(self.centralwidget)
        self.text.setGeometry(QtCore.QRect(100, 140, 521, 20))
        self.text.setOrientation(QtCore.Qt.Horizontal)
        self.text.setMinimum(10)
        self.text.setMaximum(20)
        self.text.setSingleStep(1)
        self.text.valueChanged.connect(self.slider_value_changed)
        self.text.setObjectName("text")

        self.message_label = QtWidgets.QLabel(self.centralwidget)
        self.message_label.setGeometry(QtCore.QRect(10, 210, 621, 16))
        self.message_label.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.message_label.setAlignment(QtCore.Qt.AlignCenter)
        self.message_label.setObjectName("message_label")

        MainWindow.setCentralWidget(self.centralwidget)

        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 640, 21))
        self.menubar.setObjectName("menubar")

        MainWindow.setMenuBar(self.menubar)

        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")

        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    # updates window's text
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Settings"))
        self.fps_label.setText(_translate("MainWindow", "FPS: 30"))
        self.resolution_header.setText(_translate("MainWindow", "Resolution:"))
        self.width_label.setText(_translate("MainWindow", "Width:"))
        self.height_label.setText(_translate("MainWindow", "Height:"))
        self.text_header.setText(_translate("MainWindow", "Text:"))
        self.text_label.setText(_translate("MainWindow", "Text size: 15"))
        self.message_label.setText(_translate("MainWindow", ""))

    # updates fps and text_size labels when slider moves
    def slider_value_changed(self):
        if self.sender().objectName() == 'fps':
            self.fps_label.setText(f'FPS: {self.sender().value()}')
        else:
            self.text_label.setText(f'Text size: {self.sender().value()}')

        self.on_value_changed()

    # updates message line on every val change from settings window
    def on_value_changed(self):
        self.message_label.setText('Close the settings window and restart the game to commit changes!')

    # calling message box on close
    def closeEvent(self, event):
        close = QMessageBox()
        close.setWindowTitle('Settings')
        close.setText("Вы хотите сохранить изменения?")
        close.setStandardButtons(QMessageBox.Yes | QMessageBox.Cancel | QMessageBox.No)
        close = close.exec()

        if close == QMessageBox.Yes:
            self.commit_changes()
            event.accept()
        elif close == QMessageBox.Cancel:
            event.ignore()
        else:
            event.accept()

    # commits local preferences changes to database
    def commit_changes(self):
        database.request(f"UPDATE settings SET value = {self.fps.value()} WHERE name = 'fps'")
        database.request(f"UPDATE settings SET value = {self.text.value()} WHERE name = 'text_size'")
        database.request(f"UPDATE settings SET value = {self.height.text()} WHERE name = 'width'")
        database.request(f"UPDATE settings SET value = {self.width.text()} WHERE name = 'height'")

        database.commit()


# basically the settings window (above) 'wrapper'
class SettingsWindow(QMainWindow, MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)


# custom excepthook def to catch errors
def except_hook(a, b, c):
    sys.__excepthook__(a, b, c)


# setups pyqt window and return QApplication object
def setup_settings_ui():
    global window, app, database

    if not window:
        app = QApplication(sys.argv)
        window = SettingsWindow()
        sys.excepthook = lambda a, b, c: sys.__excepthook__(a, b, c)

    if not database:
        database = SettingsDatabase(DATABASE_PATH)

    print(get_resolution())

    return app


# updates displayed preferences and shows settings window
def show_window():
    global window

    window.show()

    window.fps_label.setText(f'FPS: {get_fps()}')
    window.width.setText(str(get_resolution()[0]))
    window.height.setText(str(get_resolution()[1]))
    window.text_label.setText(f'Text size: {get_text_size()}')

    window.fps.setValue(get_fps())
    window.text.setValue(get_text_size())
    window.message_label.setText('')


# returns preferred resolution from database
def get_resolution():
    global database

    if not database:
        database = SettingsDatabase(DATABASE_PATH)

    w, h = [int(i[0]) for i in database.request(
        "SELECT value FROM settings WHERE name in ('width', 'height')")]
    return w, h


# returns preferred fps from database
def get_fps():
    global database

    if not database:
        database = SettingsDatabase(DATABASE_PATH)

    fps = int(database.request("SELECT value FROM settings WHERE name = 'fps'")[0][0])
    return fps


# returns preferred text size from database
def get_text_size():
    global database

    if not database:
        database = SettingsDatabase(DATABASE_PATH)

    text_size = int(database.request("SELECT value FROM settings WHERE name = 'text_size'")[0][0])
    return text_size


if __name__ == "__main__":
    show_window()
