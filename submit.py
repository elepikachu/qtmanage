import os
import json
import pymysql
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox
from PyQt5.QtGui import QFont


FONT_12 = QFont('Kaiti TC', 15)
VERSION = 'project manage system v1.0.0'
NAME = VERSION + ' --- by elepikachu'
TITLE = 'submit mode'
CONFIG_PATH = 'config.json'
ORIGIN_CONFIG = '{' \
                '"姓名": "张三",' \
                '"联系电话": "0000",' \
                 '"课题编号": "",' \
                '"单位全称": "新能源研究中心" ' \
                '}'


class Submit_UI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 400, 600)
        self.setWindowTitle(TITLE)
        self.setWindowIcon(QtGui.QIcon('jng.png'))
        self.setToolTip(NAME)
        self.img_route = 'background.jpeg'
        self.info_dict = read_js()
        if os.path.exists(self.img_route):
            self.use_palette(img_route=self.img_route)

        self.InputWin = QtWidgets.QTextEdit(self)
        self.InputWin.setGeometry(75, 100, 270, 30)
        self.InputWin.setPlaceholderText("输入要做的LC题目，一次一道")
        self.InputWin.setStyleSheet("background:rgb(255,255,255,0.6)")


        self.helpButton = QtWidgets.QPushButton(self)
        self.helpButton.setGeometry(0, 0, 75, 25)
        self.helpButton.setText("Help")
        self.helpButton.setToolTip("打开帮助文档")
        self.helpButton.clicked.connect(self.help_window)

        self.configButton = QtWidgets.QPushButton(self)
        self.configButton.setGeometry(72, 0, 75, 25)
        self.configButton.setText("Config")
        self.configButton.setToolTip("打开配置窗口")
        self.configButton.clicked.connect(self.config_window)

        self.exitButton = QtWidgets.QPushButton(self)
        self.exitButton.setGeometry(325, 0, 75, 25)
        self.exitButton.setText("Exit")
        self.exitButton.setToolTip("关闭程序")
        self.exitButton.clicked.connect(self.close)

        self.titleLabel = QtWidgets.QLabel(self)
        self.titleLabel.setText(TITLE)
        self.titleLabel.setFont(FONT_12)
        self.titleLabel.setGeometry(75, 40, 300, 20)
        self.titleLabel.setStyleSheet("Color:green")

        self.infoLabel = QtWidgets.QLabel(self)
        self.infoLabel.setText("----请输入要提交的信息----")
        self.infoLabel.setFont(FONT_12)
        self.infoLabel.setGeometry(150, 510, 150, 20)
        self.infoLabel.setStyleSheet("Color:green")

        self.submitButton = QtWidgets.QPushButton(self)
        self.submitButton.setGeometry(220, 555, 75, 25)
        self.submitButton.setText("Submit")
        self.submitButton.setToolTip("=。=")
        self.submitButton.clicked.connect(self.help_window)

        self.outBox = QtWidgets.QTextBrowser(self)
        self.outBox.setGeometry(50, 200, 300, 300)
        self.outBox.setStyleSheet("background:rgb(255,255,255,0.6)")
        self.show()

    def use_palette(self, img_route):
        window_pale = QtGui.QPalette()
        pix = QtGui.QPixmap(img_route)
        pix = pix.scaled(400, 600)
        window_pale.setBrush(QtGui.QPalette.Background, QtGui.QBrush(pix))
        self.setPalette(window_pale)

    def help_window(self):
        windows = Help()
        windows.show_info()

    def config_window(self):
        windows = Config()


class Help(QWidget):
    def __init__(self):
        super().__init__()

        self.setGeometry(300, 300, 400, 600)
        self.setWindowTitle("Help")
        self.setWindowIcon(QtGui.QIcon('jng.png'))

        self.outBox = QtWidgets.QTextBrowser(self)
        self.outBox.setGeometry(50, 100, 300, 300)
        self.outBox.setStyleSheet("background:rgb(255,255,255,0.6)")
        self.show()

    def show_info(self):
        with open(r'Help.txt', 'r', encoding='utf-8') as f:
            text = f.read()
        self.outBox.setText(text)


class Config(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(300, 300, 400, 600)
        self.setWindowTitle("配置文档")
        self.setWindowIcon(QtGui.QIcon('jng.png'))
        self.info_dict = read_js()

        self.outBox = QtWidgets.QTextEdit(self)
        self.outBox.setGeometry(50, 100, 300, 300)
        self.outBox.setStyleSheet("background:rgb(255,255,255,0.6)")
        self.outBox.setText(str(self.info_dict))

        self.checkButton = QtWidgets.QPushButton(self)
        self.checkButton.setGeometry(100, 500, 75, 25)
        self.checkButton.setText("Config")
        self.checkButton.setToolTip("配置")
        self.checkButton.clicked.connect(self.config)

        self.submitButton = QtWidgets.QPushButton(self)
        self.submitButton.setGeometry(250, 500, 75, 25)
        self.submitButton.setText("Reset")
        self.submitButton.setToolTip("重置配置")
        self.submitButton.clicked.connect(self.reset_config)

        self.show()

    def config(self):
        text = self.outBox.toPlainText().strip()
        with open(CONFIG_PATH, 'w') as f:
            f.write(json.dumps(eval(text), ensure_ascii=False))

    def reset_config(self):
        self.outBox.setText(str(ORIGIN_CONFIG))
        with open(CONFIG_PATH, 'w') as f:
            f.write(json.dumps(ORIGIN_CONFIG, ensure_ascii=False))


def read_js(path=CONFIG_PATH):
    with open(path) as load_f:
        return json.load(load_f)