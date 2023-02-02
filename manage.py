import os
import sys
import pymysql
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox
from PyQt5.QtGui import QFont


FONT_12 = QFont('Kaiti TC', 15)
VERSION = 'project manage system v1.0.0'
NAME = VERSION + ' --- by elepikachu'
TITLE = 'manage mode'


class Manage_UI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 600, 400)
        self.setWindowTitle(TITLE)
        self.setWindowIcon(QtGui.QIcon('jng.png'))
        self.setToolTip(NAME)
        self.img_route = 'background2.jpeg'
        if os.path.exists(self.img_route):
            self.use_palette(img_route=self.img_route)

        self.helpButton = QtWidgets.QPushButton(self)
        self.helpButton.setGeometry(0, 0, 100, 25)
        self.helpButton.setText("Help")
        self.helpButton.setToolTip("打开帮助文档")
        self.helpButton.clicked.connect(self.help_window)

        self.exitButton = QtWidgets.QPushButton(self)
        self.exitButton.setGeometry(500, 0, 100, 25)
        self.exitButton.setText("Exit")
        self.exitButton.setToolTip("关闭程序")
        self.exitButton.clicked.connect(self.close)

        self.titleLabel = QtWidgets.QLabel(self)
        self.titleLabel.setText(VERSION + ' ' + TITLE)
        self.titleLabel.setFont(FONT_12)
        self.titleLabel.setGeometry(75, 40, 450, 20)
        self.titleLabel.setStyleSheet("Color:green")

        self.dataTable = QtWidgets.QTableWidget(self)
        self.tableInit()
        self.dataTable.setStyleSheet("background:rgb(255,255,255,0.8)")
        self.dataTable.setGeometry(50, 80, 500, 200)

        self.outputBox = QtWidgets.QTextBrowser(self)
        self.outputBox.setStyleSheet("background:rgb(255,255,255,0.6)")
        self.outputBox.setGeometry(300, 300, 250, 75)

        self.addButton = QtWidgets.QPushButton(self)
        self.addButton.setGeometry(40, 320, 75, 20)
        self.addButton.setText("Add line")
        self.addButton.setToolTip("add line in the end")
        self.addButton.clicked.connect(self.close)

        self.updateButton = QtWidgets.QPushButton(self)
        self.updateButton.setGeometry(130, 320, 75, 20)
        self.updateButton.setText("update line")
        self.updateButton.setToolTip("update the line you selected")
        self.updateButton.clicked.connect(self.close)

        self.deleteButton = QtWidgets.QPushButton(self)
        self.deleteButton.setGeometry(220, 320, 75, 20)
        self.deleteButton.setText("delete line")
        self.deleteButton.setToolTip("delete the line you selected")
        self.deleteButton.clicked.connect(self.close)

        self.filterBox = QtWidgets.QComboBox(self)
        self.filterBox.setGeometry(40, 350, 75, 20)

        self.filterButton = QtWidgets.QPushButton(self)
        self.filterButton.setGeometry(130, 350, 75, 20)
        self.filterButton.setText("name filter")
        self.filterButton.setToolTip("filter data according to name")
        self.filterButton.clicked.connect(self.close)

        self.printButton = QtWidgets.QPushButton(self)
        self.printButton.setGeometry(220, 350, 75, 20)
        self.printButton.setText("print chart")
        self.printButton.setToolTip("print the chart")
        self.printButton.clicked.connect(self.close)


    def tableInit(self):
        db = pymysql.connect(host="localhost", port=3306, user="root", password="123456", database="elepikachu")
        cursor = db.cursor()
        cursor.execute("select * from buyitem_item")
        all = cursor.fetchall()
        row = len(all)
        vol = len(all[0])
        col_lst = [tup[0] for tup in cursor.description]
        self.dataTable.setColumnCount(vol)
        self.dataTable.setRowCount(row)
        self.dataTable.setHorizontalHeaderLabels(col_lst)
        self.dataTable.verticalHeader().setVisible(False)
        for i in range(row):
            for j in range(vol):
                tmp = all[i][j]
                data = QtWidgets.QTableWidgetItem(str(tmp))
                self.dataTable.setItem(i, j, data)


    def use_palette(self, img_route):
        window_pale = QtGui.QPalette()
        pix = QtGui.QPixmap(img_route)
        pix = pix.scaled(600, 400)
        window_pale.setBrush(QtGui.QPalette.Background, QtGui.QBrush(pix))
        self.setPalette(window_pale)

    def help_window(self):
        self.window3 = Help()
        self.window3.show_info()
        self.window3.show()

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Warning', 'Are you sure to quit', QMessageBox.Yes, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


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