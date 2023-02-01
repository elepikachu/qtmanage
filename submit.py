# -*- coding: utf-8 -*-

import datetime
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
CHECK_FLAG = 0


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
        self.titleLabel.setText(TITLE + ' - please input')
        self.titleLabel.setFont(FONT_12)
        self.titleLabel.setGeometry(75, 40, 300, 20)
        self.titleLabel.setStyleSheet("Color:green")

        self.infoLabel = QtWidgets.QLabel(self)
        self.infoLabel.setText("Remember to click check before submit your data :)")
        self.infoLabel.setGeometry(50, 510, 300, 20)
        self.infoLabel.setStyleSheet("Color:blue")

        self.goodName = QtWidgets.QLabel(self)
        self.goodName.setText('商品名称')
        self.goodName.setGeometry(40, 80, 60, 25)

        self.goodInput = QtWidgets.QTextEdit(self)
        self.goodInput.setGeometry(115, 80, 200, 25)
        self.goodInput.setStyleSheet("background:rgb(255,255,255,0.6)")

        self.brandName = QtWidgets.QLabel(self)
        self.brandName.setText('品牌型号')
        self.brandName.setGeometry(40, 110, 60, 25)

        self.brandInput = QtWidgets.QTextEdit(self)
        self.brandInput.setGeometry(115, 110, 200, 25)
        self.brandInput.setStyleSheet("background:rgb(255,255,255,0.6)")

        self.NumName = QtWidgets.QLabel(self)
        self.NumName.setText('数量单位')
        self.NumName.setGeometry(40, 140, 60, 25)

        self.NumInput = QtWidgets.QTextEdit(self)
        self.NumInput.setGeometry(115, 140, 45, 25)
        self.NumInput.setPlaceholderText('1')
        self.NumInput.setStyleSheet("background:rgb(255,255,255,0.6)")

        self.UnitInput = QtWidgets.QComboBox(self)
        self.UnitInput.addItems(['个', '只', '套', '组', '盒'])
        self.UnitInput.setEditable(True)
        self.UnitInput.setGeometry(160, 140, 45, 25)

        self.ClassName = QtWidgets.QLabel(self)
        self.ClassName.setText('物资分类')
        self.ClassName.setGeometry(215, 140, 60, 25)

        self.ClassInput = QtWidgets.QComboBox(self)
        self.ClassInput.addItems(['办公用品', '设备耗材', '办公家具', '五金杂品', '劳动防护', '化学试剂', '实验耗材及小型设备'])
        self.ClassInput.setGeometry(270, 140, 70, 25)

        self.infoName = QtWidgets.QLabel(self)
        self.infoName.setText('采购说明')
        self.infoName.setGeometry(40, 170, 60, 25)

        self.infoInput = QtWidgets.QTextEdit(self)
        self.infoInput.setGeometry(115, 170, 200, 25)
        self.infoInput.setStyleSheet("background:rgb(255,255,255,0.6)")

        self.otherName = QtWidgets.QLabel(self)
        self.otherName.setText('备注')
        self.otherName.setGeometry(40, 200, 60, 25)

        self.otherInput = QtWidgets.QTextEdit(self)
        self.otherInput.setGeometry(115, 200, 200, 25)
        self.otherInput.setPlaceholderText('京东请填商品编号')
        self.otherInput.setStyleSheet("background:rgb(255,255,255,0.6)")

        self.checkButton = QtWidgets.QPushButton(self)
        self.checkButton.setGeometry(120, 555, 75, 25)
        self.checkButton.setText("Check")
        self.checkButton.setToolTip("check the info before submit")
        self.checkButton.clicked.connect(self.check_result)

        self.submitButton = QtWidgets.QPushButton(self)
        self.submitButton.setGeometry(220, 555, 75, 25)
        self.submitButton.setText("Submit")
        self.submitButton.setToolTip("submit info to the database")
        self.submitButton.clicked.connect(self.submit_result)

        self.outBox = QtWidgets.QTextBrowser(self)
        self.outBox.setGeometry(50, 250, 300, 250)
        self.outBox.setStyleSheet("background:rgb(255,255,255,0.6)")
        self.show()

    def use_palette(self, img_route):
        window_pale = QtGui.QPalette()
        pix = QtGui.QPixmap(img_route)
        pix = pix.scaled(400, 600)
        window_pale.setBrush(QtGui.QPalette.Background, QtGui.QBrush(pix))
        self.setPalette(window_pale)

    def help_window(self):
        self.window3 = Help()
        self.window3.show_info()
        self.window3.show()

    def config_window(self):
        self.window4 = Config()
        self.window4.show()

    def check_result(self):
        global CHECK_FLAG
        if self.get_info() == False:
            return
        self.text = '请检查您的信息，确认无误后点击提交\n'\
               f'姓名： {self.info_dict["姓名"]}\n' \
               f'单位全称： {self.info_dict["单位全称"]}\n' \
               f'联系电话： {self.info_dict["联系电话"]}\n' \
               f'课题编号： {self.info_dict["课题编号"]}\n' \
               f'商品名称： {self.info_dict["商品名称"]}\n' \
               f'品牌型号： {self.info_dict["品牌型号"]}\n' \
               f'数量单位： {self.info_dict["数量"]} {self.info_dict["单位"]}\n' \
               f'分类： {self.info_dict["分类"]}\n' \
               f'采购说明： {self.info_dict["采购说明"]}\n' \
               f'备注： {self.info_dict["备注"]}\n'
        self.outBox.setText(self.text)
        CHECK_FLAG = 1

    def submit_result(self):
        if CHECK_FLAG == 0:
            self.outBox.setText("请先检查后再提交")
            return
        reply = QMessageBox.question(self, 'Warning', 'Are you sure to submit', QMessageBox.Yes, QMessageBox.No)
        if reply == QMessageBox.No:
            return
        db = pymysql.connect(host="localhost", port=3306, user="root", password="123456", database="elepikachu")
        cursor = db.cursor()
        cursor.execute('select * from buyitem_item order by id desc limit 1;')
        maxIdx = cursor.fetchone()
        print(maxIdx)
        idx = maxIdx[0]+1
        date = datetime.datetime.today()
        cmd = f"insert into buyitem_item value({idx}, '{self.info_dict['商品名称']}', '{self.info_dict['品牌型号']}', '{self.info_dict['单位']}', '{self.info_dict['数量']}', '{self.info_dict['姓名']}', '{self.info_dict['联系电话']}', '{self.info_dict['课题编号']}', '{self.info_dict['采购说明']}', '{self.info_dict['备注']}', '{self.info_dict['单位全称']}', '{date}', 0, '{self.info_dict['分类']}');"
        print(cmd)
        try:
            cursor.execute(cmd)
            db.commit()
        except Exception as e:
            print(e)
        self.outBox.setText("submit success, data index is %d" % idx)

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Warning', 'Are you sure to quit', QMessageBox.Yes, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def get_info(self):
        self.info_dict['商品名称'] = self.goodInput.toPlainText()
        self.info_dict['品牌型号'] = self.brandInput.toPlainText()
        self.info_dict['数量'] = self.NumInput.toPlainText()
        self.info_dict['单位'] = self.UnitInput.currentText()
        self.info_dict['分类'] = self.ClassInput.currentText()
        self.info_dict['采购说明'] = self.infoInput.toPlainText()
        self.info_dict['备注'] = self.otherInput.toPlainText()
        if self.info_dict['商品名称'] == '':
            self.outBox.setText("商品名为空")
            return False
        if self.info_dict['数量'] == '':
            self.outBox.setText("数量为空")
            return False
        return True



class Help(QWidget):
    def __init__(self):
        super().__init__()

        self.setGeometry(300, 300, 400, 600)
        self.setWindowTitle("Help")
        self.setWindowIcon(QtGui.QIcon('jng.png'))

        self.titleLabel = QtWidgets.QLabel(self)
        self.titleLabel.setText(TITLE + ' - Help')
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


class Config(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(300, 300, 400, 600)
        self.setWindowTitle("Config")
        self.setWindowIcon(QtGui.QIcon('jng.png'))
        self.info_dict = read_js()

        self.titleLabel = QtWidgets.QLabel(self)
        self.titleLabel.setText(TITLE + ' - Config')
        self.titleLabel.setFont(FONT_12)
        self.titleLabel.setGeometry(75, 50, 300, 20)
        self.titleLabel.setStyleSheet("Color:green")

        self.outBox = QtWidgets.QTextEdit(self)
        self.outBox.setGeometry(50, 100, 300, 300)
        self.outBox.setStyleSheet("background:rgb(255,255,255,0.6)")
        self.outBox.setText(str(self.info_dict))

        self.checkButton = QtWidgets.QPushButton(self)
        self.checkButton.setGeometry(75, 500, 75, 25)
        self.checkButton.setText("Config")
        self.checkButton.setToolTip("配置")
        self.checkButton.clicked.connect(self.config)

        self.submitButton = QtWidgets.QPushButton(self)
        self.submitButton.setGeometry(240, 500, 75, 25)
        self.submitButton.setText("Reset")
        self.submitButton.setToolTip("重置配置")
        self.submitButton.clicked.connect(self.reset_config)

        self.successLabel = QtWidgets.QLabel(self)
        self.successLabel.setGeometry(150, 450, 100, 25)
        self.successLabel.setText("config success")

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
