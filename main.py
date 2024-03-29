﻿# This Pytahon file uses the following encoding: utf-8
# 开发项目：AI人工语音播报提醒
# 日期：2023.12.2
# 作者：kkklu
# email:2039871@qq.com

# 性能描述：
# 定时播报需要播报的语音，提醒值班员。例如：请报平安、请三台并机、请恢复正常播出....
# 读取xml文件，starttime endtime message等，闹钟判断时间并播出语音
# 两个UI，一个UI运行执行程序，执行完了显示执行日志；另一个设置UI，设置starttime endtime message 按星期还是每天循环，参照计划任务,保存是写入xml文件

# 改进：
# 1.每个函数需考虑异常处理，成功后return true
# 2.要不要考虑线程
# 3.在哪个程序里放进清理xml文件中过期的语音提醒
# 4。auto-py-to-exe

# ----------------------------------------

# This Python file uses the following encoding: utf-8
import sys
from PySide2.QtWidgets import QApplication, QWidget, QPlainTextEdit, QLabel, QLCDNumber, QVBoxLayout, QHBoxLayout, QGridLayout, QComboBox, QMessageBox, QPushButton,QStatusBar
# from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel,QLCDNumber,QVBoxLayout,QMessageBox,QPushButton
import time
import datetime
import threading
# import pandas as pd
from PySide2.QtCore import qDebug, Slot
from PySide2.QtGui import QIcon,QCloseEvent
import os
import logging


from AIVoice import Artificial_voice_playback_1

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

import pyttsx3
import AIVoice

class MyWidget(QWidget):
    def __init__(self):
        #QWidget.__init__(self)
        super().__init__()

        self.data = list()
        self.initUI()
        self.initlog()

        # 不断刷新时间并显示 #mainthread结束，子线程也立马结束，那么需设置deamon=True
        time_display = threading.Thread(
            target=self.display, name="time_display",daemon=True)
        time_display.start()
        

        ReadXml = threading.Thread(target=self.ReadXml, name="read_xml", args=(
            self.data,),daemon=True)  # [self.data])#(self.data,)) #thread 传递 list参数的两种方法
        ReadXml.start()
        

        self.h1_button.clicked.connect(self.test_button_clicked)
        # if self.ReadXml():
        #    print("read xml success")

    # def readxml():

    # 功能：初始化UI

    def initUI(self):
        self.setVisible(True) 
        #self.setFixedWidth()
        self.resize(520, 300)
        
        self.setWindowTitle("珠海电台播控语音提醒")
        #self.setWindowIconText("珠海zhbs")
        self.setWindowIcon(QIcon("timer.png")) #这个不起作用，待解决

        # 全局窗体
        self.globalWidget = QWidget(self)
        self.globalLayout = QVBoxLayout(self)  # 是不是应该是gridlayout？
        # 分窗体
        self.h1_layout = QHBoxLayout()
        self.h2_layout = QVBoxLayout()
        self.h3_layout=QHBoxLayout()
        self.g_layout = QGridLayout()

        # 1号分窗体
        self.h1_label = QLabel()
        #self.h1_label.resize(40,30)
        self.h1_label.setText("任务：")

        self.h1_combobox = QComboBox(self)
        qDebug("ComboBox width:"+self.h1_combobox.width().__str__())
        qDebug("ComboBox height:"+self.h1_combobox.height().__str__())
        #self.h1_combobox.resize(200,30) #这个语句不起作用，why？
        self.h1_combobox.setFixedSize(370,20)

        

        self.h1_button = QPushButton(self)
        #self.h1_button.resize(40,30)
        self.h1_button.setText("测试")
        
        #self.h1_layout.addStretch(2)
        self.h1_layout.addWidget(self.h1_label)
        self.h1_layout.addStretch(2)
        self.h1_layout.addWidget(self.h1_combobox)
        self.h1_layout.addStretch(2)
        self.h1_layout.addWidget(self.h1_button)
        #self.h1_layout.addStretch(2)

        # 2号分窗体
        self.h2_label = QLabel()
        self.h2_label.setText("日志：")
        self.h2_textedit = QPlainTextEdit()

        self.h2_layout.addWidget(self.h2_label)
        self.h2_layout.addWidget(self.h2_textedit)

        # 3号分窗体
        #
        #self.LCD = QLCDNumber()  # 初始化LCD
        #self.LCD.setDigitCount = 8
        #self.LCD.setDecMode = QLCDNumber.Dec
        #self.LCD.setSegmentStyle = QLCDNumber.Flat
        ## (datetime.datetime.today().strftime("%H:%M:%S"))#(time.strftime('%H:%M:%S',time.localtime()))
        #self.LCD.display(time.strftime('%X', time.localtime()))

        #self.datelabel = QLabel()
        #self.datelabel.setText(str(datetime.date.today()))
        ## self.datelabel.move(100,0)

        #self.box_layout = QVBoxLayout()
        #self.box_layout.addWidget(self.LCD)
        #self.box_layout.addWidget(self.datelabel)
        #...
        #4号窗体
        self.h3_statusbar= QStatusBar()
        #self.h3_statusbar.showMessage("成功") #.setWindowIconText("成功")
        self.h3_layout.addWidget(self.h3_statusbar)

        # self.box_layout.setAlignment(widget.width,widget.)
        # self.box_layout.setAlignment()
        # self.setLayout(self.box_layout) #设置窗体布局

        self.globalLayout.addLayout(self.h1_layout)
        self.globalLayout.addLayout(self.h2_layout)
        #self.globalLayout.addLayout(self.box_layout)
        self.globalLayout.addLayout(self.h3_layout)

        self.show()
        return

    def initlog(self):
        #默认的warning级别，只输出warning以上的
        #使用basicConfig()来指定日志级别和相关信息

        logging.basicConfig(level=logging.DEBUG #设置日志输出格式
                    ,filename="history.log" #log日志输出的文件位置和文件名
                    ,filemode="w" #文件的写入格式，w为重新写入文件，默认是追加
                    ,format="%(asctime)s - %(name)s - %(levelname)-9s - %(filename)-8s : %(lineno)s line - %(message)s" #日志输出的格式
                    # -8表示占位符，让输出左对齐，输出长度都为8位
                    ,datefmt="%Y-%m-%d %H:%M:%S" #时间输出的格式
                    )

        logging.debug("This is  DEBUG !!")
        logging.info("This is  INFO !!")
        logging.warning("This is  WARNING !!")
        logging.error("This is  ERROR !!")
        logging.critical("This is  CRITICAL !!")
        return

#在实际项目中，捕获异常的时候，如果使用logging.error(e)，只提示指定的logging信息，不会出现
#为什么会错的信息，所以要使用logging.exception(e)去记录。

    # 函数名：display
    # 功能：不断刷新时间并显示
    def display(self):
        while True:
            # (datetime.datetime.today().strftime("%H:%M:%S"))
            try:
                #self.LCD.display(time.strftime('%X', time.localtime()))
                self.h3_statusbar.showMessage(datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S"))
                #logging.debug()
            except IOError:
                pass
                logging.error(IOError)
                break
            #qDebug("显示当前时间：")
            #qDebug(time.strftime('%X', time.localtime()))
            #qDebug(datetime.datetime.today().ctime())
            #qDebug(datetime.datetime.today().strftime("%Y/%m/%d/%H/%M/%S"))

            ##在这里加上时间比较函数，函数名改为 readxml and compare time  还是重新做一个合并函数，把thread改为合并函数，合并函数包括readxml 和 compare time，这样程序架构更加清晰
            ## if compare_time == True: AI发声
            p=AIVoice.compare_time(self.data)  #闹钟时间
            if p>=0:
                logging.debug("当前时间处于闹钟时间")
                qDebug(datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")+"成功播放："+self.data[p][3].__str__())
                Artificial_voice_playback_1(self.data[p][3].__str__())
                self.h2_textedit.appendPlainText(datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")+"成功播放："+self.data[p][3].__str__())
                #p=-1
                #break
                #添加日志信息
                logging.debug(datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")+"成功播放："+self.data[p][3].__str__())
        
            time.sleep(1)
        # return
    # region date strtime格式
    '''
%y 两位数的年份表示（00-99）
%Y 四位数的年份表示（000-9999）
%m 月份（01-12）
%d 月内中的一天（0-31）
%H 24小时制小时数（0-23）
%I 12小时制小时数（01-12）
%M 分钟数（00=59）
%S 秒（00-59）
%a 本地简化星期名称
%A 本地完整星期名称
%b 本地简化的月份名称
%B 本地完整的月份名称
%c 本地相应的日期表示和时间表示
%j 年内的一天（001-366）
%p 本地A.M.或P.M.的等价符
%U 一年中的星期数（00-53）星期天为星期的开始
%w 星期（0-6），星期天为星期的开始
%W 一年中的星期数（00-53）星期一为星期的开始
%x 本地相应的日期表示
%X 本地相应的时间表示
%Z 当前时区的名称
%% %号本身
    '''
    # endregion
    # ----------------------------------------------------
    # 函数名：读取xml文件
    # 参考网址：https://zhuanlan.zhihu.com/p/582830847
    # 功能：每隔一段时间读xml文件，并更新变量
    # 1、方法1：需要做一个static的变量（list或字典）吗？然后不断地都xml，更新该变量
    # 2、方法2 返回一个变量值
    # 3、方法3：考虑用signal

    def ReadXml(self, data):
        
        while True:
            # region 另一种read xml方法
            # init xml
            # read xml
            # 读取xml字符串

            # try:
            #    xml_data=open("config.xml").read()
            # except IOError:
            #    print("Error:找不到文件打开！")
            # else:
            #    root = ET.fromstring(xml_data)

            # 打开XML文件并解析 第二种打开xml方式
            # endregion
            try:
                tree = ET.parse('config.xml')
                # 获取根元素
                root = tree.getroot()
                #qDebug("打开config.xml成功")
                
                self.h1_combobox.clear() #更新前清除以前的数据
                data.clear()
                logging.debug('打开config.xml成功')
                #data1.clear()
            except IOError:
                qDebug("打开config.xml失败")
                qDebug(ET.ParseError().__str__)
                #QMessageBox.about(self.aboutButton,'About PySide','PySide6')
                logging.error(IOError)
                break
                #return False
           # data = list()


           
            for child in root:
                #qDebug("child: "+child[0].text+" "+child[1].text +
                #       " "+child[2].text+" "+child[3].text)
                #
                self.h1_combobox.addItem(
                    child[0].text+" "+child[1].text+" "+child[2].text+" "+child[3].text)  # combobox additem
                data1 = list()
                data1.clear()
                for son in child:
                    data1.append(son.text)
                    qDebug("DATA1:"+son.text)
                data.append(data1)
            """
            # region 调试输出,需要调试时才打开
            qDebug("======================")
            # for data_temp in data:
            qDebug(data.__str__())
            qDebug("======================")
            # endregion
            """
            # region combobox additem
            # for combobox_item in data:
            #    #整理好字符串并添加字符串：
            #
            #    self.h1_combobox.addItem(combobox_item)
            # endregion




            time.sleep(30)  # 重新3秒读一次xml文件
            #return True
    # region unused
    """"
    def initTime(self):
        mytime = datetime
        mytime = time.localtime

        return
    """
    # endregion
 
    # 加 button click事件
    # @Slot
    def test_button_clicked(self):
        qDebug("button has clicked")
        # is not -1:#self.h1_combobox.currentText is not None:
        if self.h1_combobox.currentIndex() != -1:
            qDebug(self.h1_combobox.currentText())
            qDebug("index: "+self.h1_combobox.currentIndex().__str__())
            # 用 静态的data 截取时间和提醒文字，还是通着combobox得currentText来提取？好像用data好一点？
            qDebug(self.data[self.h1_combobox.currentIndex()].__str__())
            qDebug(self.data[self.h1_combobox.currentIndex()][3].__str__())
            # region 调试，需要时才打开
            # 拷贝人工语音程序过来
            #此语句导致显示卡顿，采用thread会解决
            #Artificial_voice_playback_1(
            #    self.data[self.h1_combobox.currentIndex()][3].__str__())
            # endregion
            threading.Thread(target=Artificial_voice_playback_1,name='Artificial_voice_play',args=(self.data[self.h1_combobox.currentIndex()][3].__str__(),)).start()
        else:
            # self.dlg=customDialog
            h1_messagebox = QMessageBox()
            h1_messagebox.warning(self, "错误", "combobox不能为空")
        return
    def closeEvent(self, event: QCloseEvent) -> None:
        #sys.exit(app.exec_())
        
        return super().closeEvent(event)
    


if __name__ == "__main__":

    # print("This is my AI_VOICE")
    app = QApplication([])
    # ...this is my program
    widget = MyWidget()
    #widget.show() #在self.init有self.show(),在这里可加可不加
    # time_display=threading.Thread(target=widget.display,name="time_display")
    # time_display.start()
    # ......
    sys.exit(app.exec_())
