import os
import sys
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox
from PyQt5.QtGui import QFont
from submit import Submit_UI


FONT_12 = QFont('Kaiti TC', 15)
VERSION = 'project manage system v1.0.0'
NAME = VERSION + ' --- by elepikachu'


class Lucky(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 400, 150)
        self.setWindowTitle(VERSION)
        self.setWindowIcon(QtGui.QIcon('jng.png'))
        self.setToolTip(NAME)
        self.img_route = 'background2.jpeg'
        if os.path.exists(self.img_route):
            self.use_palette(img_route=self.img_route)


        self.titleLabel = QtWidgets.QLabel(self)
        self.titleLabel.setText(VERSION)
        self.titleLabel.setFont(FONT_12)
        self.titleLabel.setGeometry(50, 40, 300, 20)
        self.titleLabel.setStyleSheet("Color:green")


        self.submitButton = QtWidgets.QPushButton(self)
        self.submitButton.setGeometry(75, 100, 100, 20)
        self.submitButton.setText("Submit mode")
        self.submitButton.setToolTip("Submit data")
        self.submitButton.clicked.connect(self.submit_mode)


        self.manageButton = QtWidgets.QPushButton(self)
        self.manageButton.setGeometry(225, 100, 100, 20)
        self.manageButton.setText("Manage mode")
        self.manageButton.setToolTip("Manage data")
        self.manageButton.clicked.connect(self.manage_mode)

        self.helpButton = QtWidgets.QPushButton(self)
        self.helpButton.setGeometry(0, 0, 75, 25)
        self.helpButton.setText("Help")
        self.helpButton.setToolTip("打开帮助文档")
        self.helpButton.clicked.connect(self.help_window)

        self.exitButton = QtWidgets.QPushButton(self)
        self.exitButton.setGeometry(325, 0, 75, 25)
        self.exitButton.setText("Exit")
        self.exitButton.setToolTip("关闭程序")
        self.exitButton.clicked.connect(self.close)

        self.show()

    def submit_mode(self):
        self.windows = Submit_UI()
        self.windows.show()

    def manage_mode(self):
        pass

    def help_window(self):
        self.window2 = Help()
        self.window2.show_info()
        self.window2.show()

    def use_palette(self, img_route):
        window_pale = QtGui.QPalette()
        pix = QtGui.QPixmap(img_route)
        pix = pix.scaled(400, 150)
        window_pale.setBrush(QtGui.QPalette.Background, QtGui.QBrush(pix))
        self.setPalette(window_pale)


class Help(QWidget):
    def __init__(self):
        super().__init__()

        self.setGeometry(300, 300, 400, 600)
        self.setWindowTitle("Help")
        self.setWindowIcon(QtGui.QIcon('jng.png'))

        self.titleLabel = QtWidgets.QLabel(self)
        self.titleLabel.setText(VERSION + ' - Help')
        self.titleLabel.setFont(FONT_12)
        self.titleLabel.setGeometry(75, 50, 300, 20)
        self.titleLabel.setStyleSheet("Color:green")

        self.outBox = QtWidgets.QTextBrowser(self)
        self.outBox.setGeometry(50, 100, 300, 300)
        self.outBox.setStyleSheet("background:rgb(255,255,255,0.6)")
        self.show()

    def show_info(self):
        with open(r'Help.txt', 'r', encoding='utf-8') as f:
            text = f.read()
        self.outBox.setText(text)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Lucky()
    sys.exit(app.exec_())
