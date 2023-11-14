# -*- coding: utf-8 -*-

import os
import json
import socket
import pymysql
import datetime
import requests
from selenium import webdriver
from PyQt5.QtGui import QFont
from bs4 import BeautifulSoup
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QWidget, QMessageBox


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

    # -------------------------------------------------------------
    # 函数名： initUI
    # 功能： UI初始化
    # -------------------------------------------------------------
    def initUI(self):
        self.setGeometry(300, 300, 400, 600)
        self.setWindowTitle(TITLE)
        self.setWindowIcon(QtGui.QIcon('jng.ico'))
        self.setToolTip(NAME)
        self.img_route = 'background.jpeg'
        self.info_dict = read_js()
        if os.path.exists(self.img_route):
            self.use_palette(img_route=self.img_route)

        self.helpButton = QtWidgets.QPushButton(self)
        self.helpButton.setGeometry(0, 0, 75, 25)
        self.helpButton.setText("Help")
        self.helpButton.setToolTip("app help")
        self.helpButton.clicked.connect(self.help_window)

        self.configButton = QtWidgets.QPushButton(self)
        self.configButton.setGeometry(72, 0, 75, 25)
        self.configButton.setText("Config")
        self.configButton.setToolTip("do the configuration")
        self.configButton.clicked.connect(self.config_window)

        self.exitButton = QtWidgets.QPushButton(self)
        self.exitButton.setGeometry(325, 0, 75, 25)
        self.exitButton.setText("Exit")
        self.exitButton.setToolTip("close app")
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

        self.searchButton = QtWidgets.QPushButton(self)
        self.searchButton.setGeometry(275, 80, 50, 25)
        self.searchButton.setText("Search")
        self.searchButton.setToolTip("Search item on JingDong")
        self.searchButton.clicked.connect(self.jd_search)

        self.goodInput = QtWidgets.QTextEdit(self)
        self.goodInput.setGeometry(115, 80, 150, 25)
        self.goodInput.setPlaceholderText('京东商品请先搜索')
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
        self.otherInput.setPlaceholderText('京东商品请填商品编号')
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

    # -------------------------------------------------------------
    # 函数名： use_palette
    # 功能： 使用背景
    # -------------------------------------------------------------
    def use_palette(self, img_route):
        window_pale = QtGui.QPalette()
        pix = QtGui.QPixmap(img_route)
        pix = pix.scaled(400, 600)
        window_pale.setBrush(QtGui.QPalette.Background, QtGui.QBrush(pix))
        self.setPalette(window_pale)

    # -------------------------------------------------------------
    # 函数名： help_window
    # 功能： 打开帮助窗口
    # -------------------------------------------------------------
    def help_window(self):
        self.window3 = Help()
        self.window3.show_info()
        self.window3.show()

    # -------------------------------------------------------------
    # 函数名： config_window
    # 功能： 打开配置窗口
    # -------------------------------------------------------------
    def config_window(self):
        self.window4 = Config()
        self.window4.show()

    # -------------------------------------------------------------
    # 函数名： check_result
    # 功能： 检查输入数据
    # -------------------------------------------------------------
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

    # -------------------------------------------------------------
    # 函数名： submit_result
    # 功能： 提交数据
    # -------------------------------------------------------------
    def submit_result(self):
        if CHECK_FLAG == 0:
            self.outBox.setText("请先检查后再提交")
            return
        reply = QMessageBox.question(self, 'Warning', 'Are you sure to submit', QMessageBox.Yes, QMessageBox.No)
        if reply == QMessageBox.No:
            return
        db = pymysql.connect(host="10.122.176.4", port=3306, user="root", password="123456", database="elepikachu")
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
        cursor.execute('select * from buyitem_itemlog order by id desc limit 1;')
        maxIdx2 = cursor.fetchone()
        idx2 = maxIdx2[0] + 1
        ip = socket.gethostbyname(socket.gethostname())
        cmd = f"insert into buyitem_itemlog value({idx2}, '{ip}', '{date}', 'insert', '{self.info_dict['姓名']}-{self.info_dict['商品名称']}-false via app');"
        try:
            cursor.execute(cmd)
            db.commit()
        except Exception as e:
            print(e)
        self.outBox.setText("submit success, data index is %d" % idx)

    # -------------------------------------------------------------
    # 函数名： closeEvent
    # 功能： 关闭时询问
    # -------------------------------------------------------------
    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Warning', 'Are you sure to quit', QMessageBox.Yes, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    # -------------------------------------------------------------
    # 函数名： get_info
    # 功能： 获取用户输入信息
    # -------------------------------------------------------------
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

    # -------------------------------------------------------------
    # 函数名： jd_search
    # 功能： 在京东搜索
    # -------------------------------------------------------------
    def jd_search(self):
        good = self.goodInput.toPlainText()
        if good == '':
            self.outBox.setText('empty good name')
            return
        res = self.jd_spider(good, 1)
        output = ''
        for item in res:
            output += str(item) + '\n'
        #value, ok = QtWidgets.QInputDialog.getInt(self, "qtmanage", "Search success, result is shown in outputbox\n\nplease input the index of good:", 1, 1, len(res), 1)
        value, ok = QtWidgets.QInputDialog.getInt(self, "qtmanage",
                                                  "%s\n\nplease input the index of good:" % (output),
                                                  1, 1, len(res), 1)
        if ok:
            self.goodInput.setText(res[value]['name'])
            self.brandInput.setText(res[value]['shop'])
            self.otherInput.setText('商品编号： ' + res[value]['number'])
            self.outBox.setText('ADD SUCCESS' + str(res[value]))

    # -------------------------------------------------------------
    # 函数名： get_page
    # 功能： 爬取页面
    # -------------------------------------------------------------
    def get_page(self, url):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
        }
        try:
            html = requests.request("GET", url, headers=headers, timeout=10)
            html.encoding = "utf-8"
            return html.text
        except:
            print('爬取失败')
            return "爬取失败"

    # -------------------------------------------------------------
    # 函数名： parse_page
    # 功能： 解析爬取页面
    # -------------------------------------------------------------
    def parse_page(self, item, page):
        url = "https://search.jd.com/Search?keyword=%s&page=%s" % (item, page)
        # url = "https://www.jd.com/"
        html = self.get_page(url)
        html = str(html)
        if html is not None:
            soup = BeautifulSoup(html, 'html.parser')
            li_all = soup.select('#J_goodsList ul .gl-item')
            res_list = []
            idx = 1
            for li in li_all:
                name = [i.get_text() for i in li.select('.p-name em')][0]
                price = [i.get_text() for i in li.select('.p-price i')][0]
                if li.select('.p-shop a'):
                    shop = [i.get_text() for i in li.select('.p-shop a')][0]
                elif li.select('.p-shopnum a'):
                    shop = [i.get_text() for i in li.select('.p-shopnum a')][0]
                else:
                    shop = "自营"
                number = li['data-sku']
                href = "item.jd.com/%s.html" % number
                if (len(name) != 0 and len(price) != 0 and len(shop) != 0 and len(number) != 0):
                    info = {'idx': idx, 'name': name, 'price': price, 'shop': shop, 'number': number, 'href': href}
                    res_list.append(info)
                    idx += 1
            return res_list
        else:
            print('error')
            return None

    # -------------------------------------------------------------
    # 函数名： jd_spider
    # 功能： 通过webdriver爬取页面（爬虫寄了）
    # -------------------------------------------------------------
    def jd_spider(self, item, page):
        opt = webdriver.ChromeOptions()
        opt.add_argument('headless')
        driver = webdriver.Chrome(options=opt)
        url = "https://search.jd.com/Search?keyword=%s&page=%s" % (item, page)
        driver.get(url)
        li = driver.find_elements_by_class_name('gl-item')  # 查找li标签
        res_list = []
        idx = 1
        for l in li:
            name = l.find_element_by_css_selector('.p-name').text
            priz = l.find_element_by_css_selector('.p-price').text
            shop = l.find_element_by_css_selector('.p-shop').text
            number = l.get_attribute('data-sku')
            href = "item.jd.com/%s.html" % number
            if (len(name) != 0 and len(priz) != 0 and len(shop) != 0 and len(number) != 0):
                info = {'idx': idx, 'name': name, 'price': priz, 'shop': shop, 'number': number, 'href': href}
                res_list.append(info)
                idx += 1
        return res_list


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
        self.outBox.setGeometry(50, 100, 300, 400)
        self.outBox.setStyleSheet("background:rgb(255,255,255,0.6)")
        self.show()

    # -------------------------------------------------------------
    # 函数名： show_info
    # 功能： 读取帮助信息
    # -------------------------------------------------------------
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
        self.successLabel.setVisible(False)

        self.show()

    # -------------------------------------------------------------
    # 函数名： config
    # 功能： 配置完成
    # -------------------------------------------------------------
    def config(self):
        text = self.outBox.toPlainText().strip()
        with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
            f.write(json.dumps(eval(text), ensure_ascii=False))
        self.successLabel.setVisible(True)

    # -------------------------------------------------------------
    # 函数名： reset_config
    # 功能： 重置配置
    # -------------------------------------------------------------
    def reset_config(self):
        self.outBox.setText(str(ORIGIN_CONFIG))
    with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
        f.write(json.dumps(ORIGIN_CONFIG, ensure_ascii=False))


# -------------------------------------------------------------
# 函数名： read_js
# 功能： 读取json数据
# -------------------------------------------------------------
def read_js(path=CONFIG_PATH):
    with open(path, encoding='utf-8') as load_f:
        return json.load(load_f)
