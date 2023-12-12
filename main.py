# This Pytahon file uses the following encoding: utf-8
#开发项目：AI人工语音播报提醒
#日期：2023.12.2
#作者：kkklu

#性能描述：
#定时播报需要播报的语音，提醒值班员。例如：请报平安、请三台并机、请恢复正常播出....
#读取xml文件，starttime endtime message等，闹钟判断时间并播出语音
#两个UI，一个UI运行执行程序，执行完了显示执行日志；另一个设置UI，设置starttime endtime message 按星期还是每天循环，参照计划任务,保存是写入xml文件

#改进：
#1.每个函数需考虑异常处理，成功后return true
#2.要不要考虑线程
#3.在哪个程序里放进清理xml文件中过期的语音提醒

#----------------------------------------

# This Python file uses the following encoding: utf-8
import sys
from PySide2.QtWidgets import QApplication,QWidget,QPlainTextEdit,QLabel,QLCDNumber,QVBoxLayout,QHBoxLayout,QGridLayout,QComboBox,QMessageBox,QPushButton
#from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel,QLCDNumber,QVBoxLayout,QMessageBox,QPushButton
import time,datetime
import threading
#import pandas as pd
from PySide2.QtCore import qDebug

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

#import pyttsx3



class MyWidget(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        #super().__init__()
        self.initUI()

        #不断刷新时间并显示
        time_display=threading.Thread(target=self.display,name="time_display")
        time_display.start()

        ReadXml=threading.Thread(target=self.ReadXml,name="read_xml")
        ReadXml.start()
        #if self.ReadXml():
        #    print("read xml success")

    #def readxml():

    #功能：初始化UI
    def initUI(self):
        self.resize(400,200)
        #self.windowTitle("zhbs time")
        self.setWindowTitle("zhbs Timer")

        #全局窗体
        self.globalWidget=QWidget(self)
        self.globalLayout=QVBoxLayout(self) #是不是应该是gridlayout？
        #分窗体
        self.h1_layout=QHBoxLayout()
        self.h2_layout=QVBoxLayout()
        self.g_layout=QGridLayout()

        #1号分窗体
        self.h1_label=QLabel()
        self.h1_label.setText("任务：")

        self.h1_combobox=QComboBox(self)
        #self.h1_combobox.resize(450,50)

        self.h1_button=QPushButton(self)
        self.h1_button.setText("测试")

        self.h1_layout.addWidget(self.h1_label)
        self.h1_layout.addStretch(0)
        self.h1_layout.addWidget(self.h1_combobox)
        self.h1_layout.addStretch(0)
        self.h1_layout.addWidget(self.h1_button)
     
        #2号分窗体
        self.h2_label=QLabel()
        self.h2_label.setText("日志：")
        self.h2_textedit=QPlainTextEdit()

        self.h2_layout.addWidget(self.h2_label)
        self.h2_layout.addWidget(self.h2_textedit)

    
        #3号分窗体
        self.LCD=QLCDNumber() #初始化LCD
        self.LCD.setDigitCount=8
        self.LCD.setDecMode=QLCDNumber.Dec
        self.LCD.setSegmentStyle=QLCDNumber.Flat
        self.LCD.display(time.strftime('%X',time.localtime())) 

        self.datelabel=QLabel()
        self.datelabel.setText(str( datetime.date.today()))
        #self.datelabel.move(100,0)

        self.box_layout=QVBoxLayout()
        self.box_layout.addWidget(self.LCD)
        self.box_layout.addWidget(self.datelabel)

        #self.box_layout.setAlignment(widget.width,widget.)
        #self.box_layout.setAlignment()
        #self.setLayout(self.box_layout) #设置窗体布局

        self.globalLayout.addLayout(self.h1_layout)
        #self.globalLayout.addLayout(self.h2_layout)
        self.globalLayout.addLayout(self.box_layout)


        self.show()
        return
    
    #函数名：display
    #功能：不断刷新时间并显示
    def display(self):
        while True:
            self.LCD.display(time.strftime('%X',time.localtime()))
            time.sleep(1)
        #return
    
    #----------------------------------------------------
    #函数名：读取xml文件
    #参考网址：https://zhuanlan.zhihu.com/p/582830847
    #功能：每隔一段时间读xml文件，并更新变量
    #1、方法1：需要做一个static的变量（list或字典）吗？然后不断地都xml，更新该变量
    #2、方法2 返回一个变量值
    #3、方法3：考虑用signal
    def ReadXml(self):
        while True:
            #init xml
            #read xml
            # 读取xml字符串
            
            #try:
            #    xml_data=open("config.xml").read()
            #except IOError:
            #    print("Error:找不到文件打开！")
            #else:
            #    root = ET.fromstring(xml_data)

                # 打开XML文件并解析 第二种打开xml方式
            try:
                tree = ET.parse('config.xml')
                #获取根元素
                root=tree.getroot()
                qDebug("打开config.xml成功")
            except IOError:
                print("打不开xml文件")
                return False
            data = list()
            for child in root:
                data1 = list()
                for son in child:
                    data1.append(son.text)
                    qDebug("DATA1:")
                    qDebug(data1)
                data.append(data1,end='\n')
                qDebug("DATA:")
                qDebug(data,end='\n')
            #for combobox_item in data:
            #    #整理好字符串并添加字符串：
            #
            #    self.h1_combobox.addItem(combobox_item)   

            #df = pd.DataFrame(data, columns=['start_date', 'end_date', 'time','message'])
            #print(df)
            time.sleep(3) #重新3秒读一次xml文件
            return True

    def initTime(self):
        mytime=datetime
        mytime=time.localtime
        
        return
if __name__ == "__main__":

    #print("This is my AI_VOICE")
    app = QApplication([])
    # ...this is my program
    widget=MyWidget() 
    #time_display=threading.Thread(target=widget.display,name="time_display")
    #time_display.start()
    #......
    sys.exit(app.exec_())
