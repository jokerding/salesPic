#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : UI_Mian.py
# @Author: joker
# @Date  : 2018/12/25
# @Desc  :
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import sys
from src.util.tools import Tools
import os
import webbrowser
from img.img import *


class UI_Mian(QMainWindow):

    def __init__(self):

        super().__init__()

        self.initUI()

    def initUI(self):

        # self.initMeauBar()
        self.initBackground()

        self.setBackgroundImage(info='test')

        self.addInfoWidgetView()

        self.cheackConfig()

        # self.test()

    def cheackConfig(self):
        res = Tools.redFiles()
        if not res:
            Tools.showAlert('首次应用请先设置相关参数，点击右键选择设置')

    def contextMenuEvent(self, event):
        cmenu = QMenu(self)

        setupAct = cmenu.addAction('资料设置')
        newAct = cmenu.addAction('新增战报')
        openAct = cmenu.addAction('导出图片')
        quitAct = cmenu.addAction('退出系统')
        action = cmenu.exec_(self.mapToGlobal(event.pos()))

        if action == quitAct:
            qApp.quit()
        elif action == setupAct:
            self.setupView()
        elif action == newAct:
            self.newSales()
        else:
            self.savaImage()

    def initMeauBar(self):
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('资料设置')
        newAct = QAction('新增战报', self)
        newAct.triggered.connect(self.newSales)

        impAct = QAction('导出图片',self)
        impAct.triggered.connect(self.savaImage)

        fileMenu.addAction(newAct)
        fileMenu.addAction(impAct)
        

    def initBackground(self):

        self.setGeometry(100,100, 711 / 2, 1134 / 2)

        self.setWindowTitle('战报生成器V1.0')

        self.setAutoFillBackground(True)
        self.setFixedSize(self.width(), self.height())


    def setBackgroundImage(self,info = None):
        if info:
            img = ':img/2.jpg'
        else:
            img = ':img/1.jpg'

        png = QPixmap(img)



        palette1 = QPalette()
        palette1.setBrush(self.backgroundRole(), QBrush(png))
        self.setPalette(palette1)

    def addInfoWidgetView(self,images=None,name=None,dept=None,price=None,product=None,fromType=None,totalPrice=None):
        # 员工图像
        self.userIconlable = QLabel(self)
        self.userIconlable.setGeometry(55,200,125,155)
        images = ':img/3.jpg'
        pix =QPixmap(images).scaled(self.userIconlable.width(),self.userIconlable.height())
        self.userIconlable.setAlignment(Qt.AlignCenter)
        self.userIconlable.setPixmap(pix)

        # 员工姓名
        self.userNameLable = QLabel(self)
        self.userNameLable.setText('xxx')
        self.userNameLable.setGeometry(190,250,130,50)
        self.userNameLable.setAlignment(Qt.AlignCenter)
        self.userNameLable.setStyleSheet("font:30pt '黑体';color:red;")
        self.userNameLable.setWordWrap(True)

        # 员工部门
        self.depLable = QLabel(self)
        self.depLable.setText('xxxxx')
        self.depLable.setGeometry(190,300, 130, 50)
        self.depLable.setAlignment(Qt.AlignCenter)
        self.depLable.setStyleSheet("font:17pt '黑体';color:black;")
        self.depLable.setWordWrap(True)

        label1 = QLabel(self)
        label1.setGeometry(55,380,50,20)
        label1.setStyleSheet("font:15pt '黑体';color:black;")
        label1.setText('战果:')

        self.priceLabel = QLabel(self)
        self.priceLabel.setText('xxxxx')
        self.priceLabel.setStyleSheet("font:15pt '黑体';color:black;")
        self.priceLabel.setGeometry(115,380,150,20)
        self.priceLabel.setWordWrap(True)

        label2 = QLabel(self)
        label2.setGeometry(55, 430, 50, 20)
        label2.setStyleSheet("font:15pt '黑体';color:black;")
        label2.setText('产品:')

        self.productLabel = QLabel(self)
        self.productLabel.setText('xxxxx')
        self.productLabel.setStyleSheet("font:15pt '黑体';color:black;")
        self.productLabel.setGeometry(115,430,200,20)
        self.productLabel.setWordWrap(True)

       # label3 = QLabel(self)
        #label3.setGeometry(55, 440, 95, 20)
        # label3.setStyleSheet("font:15pt '黑体';color:black;")
       # label3.setText('回款渠道:')

        # self.fromLabel = QLabel(self)
        # self.fromLabel.setText('xxxxx')
        # self.fromLabel.setStyleSheet("font:15pt '黑体';color:black;")
        # self.fromLabel.setGeometry(150, 440, 200, 20)
        # self.fromLabel.setWordWrap(True)

        self.totalPrice = QLabel(self)
        self.totalPrice.setText('战绩:xxxxx')
        self.totalPrice.setStyleSheet("font:30pt '黑体';color:red;")
        self.totalPrice.setAlignment(Qt.AlignCenter)
        self.totalPrice.setGeometry(55,470,230,40)
        self.totalPrice.setWordWrap(True)


    def setupView(self):
        setup = setupView()
        setup.exec_()
        if setup.close():
            print(setup.configDic)


    def newSales(self):
        print('newSales.......')
        self.input = inputView(callback= self.updateUI)
        if self.input.exec_():
            pass



    def updateUI(self,info=None):
        print(info)

        if info['name']:
            self.userNameLable.setText(info['name'])
        else:
            Tools.showAlert('请先输入员工姓名')
            return

        try:
            if info['image']:
                self.userIconlable.setPixmap(
                    QPixmap(info['image']).scaled(self.userIconlable.width(), self.userIconlable.height()))
        except KeyError as e:
            Tools.showAlert('没有找到此员工图片')
            return

        self.depLable.setText(info['dept'])

        if info['price']:
            self.priceLabel.setText(info['price'])
        else:
            Tools.showAlert('请输入回款金额')
            return

        if info['product']:
            self.productLabel.setText(info['product'])
        else:
            Tools.showAlert('请选择产品')
            return

        if info['totalPrice']:
            self.totalPrice.setText('战绩:' + info['totalPrice'])
        else:
            Tools.showAlert('请输入提成金额')
        # self.fromLabel.setText(input.info['fromType'])

        self.input.close()

    def savaImage(self):
        print('savaImages........')

        rect = self.rect()

        image = self.grab(rect)

        imgPath = os.path.join(os.path.abspath('.'), 'temp.jpg')

        try:
            with open(imgPath, 'wb+'):
                image.save(imgPath)
                self.show_image(imgPath)
        except FileExistsError:
            print('......')



        # image.save('C:\\Users\\user\\Downloads\\temp.jpg')
        #
        # self.show_image('C:\\Users\\user\\Downloads\\temp.jpg')

    def show_image(self,file_path):
        """
        跨平台显示图片文件
        :param file_path: 图片文件路径
        """
        if sys.version_info >= (3, 3):
            from shlex import quote
        else:
            from pipes import quote

        if sys.platform == "darwin":
            command = "open -a /Applications/Preview.app %s&" % quote(file_path)
            os.system(command)
        else:
            webbrowser.open(file_path)

    def test(self):
        images = Tools.resource_path('images/费胜.jpg')
        self.addInfoWidgetView(images=images,
                               name='费胜',
                               dept='内贸开发三部',
                               price='5000万',
                               product='半导体激光血氧治疗仪',
                               fromType='自营品牌',
                               totalPrice='2000元')


class inputView(QDialog):
    def __init__(self,callback=None):
        super().__init__()
        self.dept = None
        self.product = None
        self.fromType = None
        self.callback = callback
        self.configDic = Tools.redFiles()
        self.info = dict()
        self.initUI()


    def initUI(self):

        self.setWindowTitle('新增战报')

        v_layout = QVBoxLayout()

        self.setLayout(v_layout)

        layout = QGridLayout()

        label1 = QLabel('战将:')
        self.nameText = QLineEdit()
        self.nameText.setPlaceholderText('请输入员工姓名')
        self.nameText.editingFinished.connect(self.endEdit)
        layout.addWidget(label1,0,0)
        layout.addWidget(self.nameText,0,1)

        label2 = QLabel('部门:')
        # self.deptList = QComboBox()
        # self.deptList.addItem('请选择部门')

        self.deptText = QLineEdit()
        self.deptText.setPlaceholderText('请输入员工部门')
        layout.addWidget(label2, 1, 0)
        layout.addWidget(self.deptText, 1, 1)

        label4 = QLabel('产品:')

        self.productList = QComboBox()
        self.productList.addItem('请选择回款产品')
        for product in self.configDic['productList']:
            self.productList.addItem(product)
        self.productList.currentIndexChanged.connect(self.productChoose)

        # layout.addWidget(self.productList)
        # self.productText = QLineEdit()
        # self.productText.setPlaceholderText('请输入产品名称')
        layout.addWidget(label4, 2, 0)
        layout.addWidget(self.productList, 2, 1)

        # label5 = QLabel('回款渠道:')
        # self.fromList = QComboBox()
        # self.fromList.addItem('请选择回款渠道')
        # self.fromText = QLineEdit()
        # self.fromText.setPlaceholderText('请输入回款渠道')
        # layout.addWidget(label5, 3, 0)
        # layout.addWidget(self.fromList, 3, 1)

        label3 = QLabel('战果:')
        self.salesText = QLineEdit()
        self.salesText.setPlaceholderText('请输入回款额')
        layout.addWidget(label3, 4, 0)
        layout.addWidget(self.salesText, 4, 1)

        label6 = QLabel('战绩:')
        self.moneyText = QLineEdit()
        self.moneyText.setPlaceholderText('请输入提成金额')
        layout.addWidget(label6, 5, 0)
        layout.addWidget(self.moneyText, 5, 1)

        v_layout.addLayout(layout)

        self.confirmBtn = QPushButton('确认提交')

        self.confirmBtn.setStyleSheet("background-color:orange;color:white")

        self.confirmBtn.clicked.connect(self.confirmBtnClick)

        v_layout.addWidget(self.confirmBtn)


    def endEdit(self):
        if self.nameText.text():
            self.configDic = Tools.redFiles()
            for img in Tools.getDirAllFiles(self.configDic['usericondir']):
                if img.find(self.nameText.text()) >=0:
                    print(img)
                    self.info['image'] = img
            if self.configDic:
                self.dept = self.configDic['userInfo'][self.nameText.text()]
                self.deptText.setText(self.dept)
                print(self.dept)

    def productChoose(self):

        self.product = self.productList.currentText()
        print(self.product)

    def confirmBtnClick(self):
        # print('..........')
        self.info['name'] = self.nameText.text()
        self.info['dept'] = self.dept
        self.info['price'] = self.salesText.text()
        self.info['product'] = self.product
        # self.info['fromType'] = self.fromType
        self.info['totalPrice'] = self.moneyText.text()

        self.callback(info = self.info)






class setupView(QDialog):
    def __init__(self):
        super().__init__()
        self.configDic = dict()
        self.initUI()
    
    def initUI(self):

        self.setWindowTitle('资料设置')
        v_layout = QVBoxLayout()

        self.setLayout(v_layout)

        layout = QGridLayout()

        self.configUserIconDirBtn = QPushButton('设置员工图像存放目录')
        self.configUserIconDirBtn.clicked.connect(self.configUserIconDir)
        layout.addWidget(self.configUserIconDirBtn)
        self.configUserIconDirEdit = QLineEdit()
        layout.addWidget(self.configUserIconDirEdit)
        self.configUserListBtn = QPushButton('批量导入员工资料')
        self.configUserListBtn.clicked.connect(self.configUserListInfo)
        layout.addWidget(self.configUserListBtn)
        closeBtn = QPushButton('确认保存')
        closeBtn.clicked.connect(self.closeView)
        layout.addWidget(closeBtn)
        v_layout.addLayout(layout)

        self.configDic = Tools.redFiles()
        if self.configDic:
            self.configUserIconDirEdit.setText(self.configDic['usericondir'])

    def closeEvent(self,event):
        self.close()

    def configUserIconDir(self):
        self.configDic = Tools.redFiles()
        if not self.configDic:
            self.configDic = dict()
        dir = Tools.open(sender=1)
        self.configDic['usericondir'] = dir
        self.configUserIconDirEdit.setText(dir)
        Tools.writeFiles(self.configDic)

    def configUserListInfo(self):
        file = Tools.open(sender=2)

        self.configDic = Tools.redFiles()

        u_list =  Tools.readExcelFiel(filepath=file,sheetIndex=1)

        userDic = {}

        for info in u_list:

            userDic[info[1]] = info[3]


        self.configDic['userInfo'] = userDic

        print()

        p_list = Tools.readExcelFiel(filepath=file,sheetIndex=2)

        p_temp_list =[]

        for p_info in p_list:
            p_temp_list.append(p_info[1])

        self.configDic["productList"] = p_temp_list

        Tools.writeFiles(self.configDic)





    def closeView(self):
        self.close()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindows = UI_Mian()
    mainWindows.show()

    sys.exit(app.exec_())