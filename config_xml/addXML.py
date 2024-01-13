# This Python file uses the following encoding: utf-8
# This Pytahon file uses the following encoding: utf-8
# 开发项目：AI人工语音播报提醒-保存xml文件
# 日期：2023.12.30
# 作者：kkklu
# email:2039871@qq.com

# 性能描述：
# 改进：
import sys
from PySide2.QtWidgets import QApplication, QWidget,QMessageBox,QDialog,QPushButton
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import QFile,QIODevice,qDebug,QDate
import add_Xml_ui
from add_Xml_ui import Ui_Dialog
from xml.etree.ElementTree import Element,ElementTree
import xml.dom.minidom as minidom

import datetime

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

class addXML(QDialog,add_Xml_ui.Ui_Dialog):  #有空对比QWidget 和self.super.__init__()语句，会不会有大的差异，dialog没有super.init
    def __init__(self):
        #self.super.__init__() #用super.__init__()会报错，必须用self
        #QWidget.__init__(self)
        QDialog.__init__(self)
        self.initUI()
        #self.save_buttonBox.clicked.connect(self.savexml)
        self.save_buttonBox.clicked.connect(self.savexml)
            
        pass  # call __init__(self) of the custom base class here
    
    #load ui :https://cloud.tencent.com/developer/article/2334289
    def initUI(self):
        self.setupUi(self)
        #region 第二种load ui文件的方法，打开UI文件，并load
        """"
        loader=QUiLoader()
        ui_file=QFile("add_Xml.ui")
        if not ui_file.open(QIODevice.ReadOnly):
            loadui_messagebox = QMessageBox()
            loadui_messagebox.warning(self, "错误", "无法打开UI文件")
            sys.exit(-1)
        self.window= loader.load(ui_file)
        ui_file.close()
        """
        #endregion
    
    def savexml(self):
        
        #以下这些语句是不是在ui.py的文件写会好一点，然后得到的starttime等结果的合法性在这里进行判断
        #start_date=QDate.getDate()
        #datetime.date(self.start_date.date())
        #end_date=datetime.date()
        #alarm_time=datetime.time()

        alarm_str=self.alarm_str_lineEdit.text()
        start_date=self.start_date.date()
        end_date=self.end_date.date()
        alarm_time=self.alarm_time.time()

        qDebug("提醒语音："+alarm_str)
        qDebug("start_date:"+start_date.__str__())
        qDebug("end_date:"+end_date.__str__())
        qDebug("time:"+alarm_time.__str__())

        if alarm_str is not None:
            pass
        else:
            QMessageBox.about(self.aboutButton,'错误','提醒语音不能为空！')
        
        # region 打开XML文件
        data=list()
        try:
            tree = ET.parse('config.xml')
            # 获取根元素
            root = tree.getroot()
            qDebug("打开config.xml成功")
            #self.h1_combobox.clear() #更新前清除以前的数据
            data.clear()
            #data1.clear()
        except IOError:
            qDebug("打开config.xml失败")
            qDebug(ET.ParseError().__str__)
            QMessageBox.about(self.aboutButton,'错误','打开config.xml失败')
            #return False
        # endregion
        
        # region 追加xml文件的一个元素
        #N0.1 func 这是一种写法？
        #https://zhuanlan.zhihu.com/p/146507161
        
        newItem=ET.SubElement(root,'item')
        ET.SubElement(newItem,'start_date').text='2024-01-01' #self.alarm_str_lineEdit.text
        ET.SubElement(newItem,'end_date').text='2024-01-01'
        ET.SubElement(newItem,'alarm_time').text='12:00:00'
        ET.SubElement(newItem,'message').text=alarm_str

        rough_str = ET.tostring(root, 'utf-8')
        # 格式化
        reparsed = minidom.parseString(rough_str)
        new_str = reparsed.toprettyxml(indent='\t')
        f = open('config.xml', 'w', encoding='utf-8')
        # 保存
        f.write(new_str)
        f.close()
        
        pass
        pass
        #tree.write('config.xml',encoding='utf-8',xml_declaration=True)
        
        #N0.2 func 这是另一种写法
        #https://blog.csdn.net/gbz3300255/article/details/108358253
        #待解决问题：tree.write不能换行，所有新数据都写在一行上
        #https://blog.csdn.net/hu694028833/article/details/81089959
        #https://blog.csdn.net/u012692537/article/details/101395192
        #https://blog.csdn.net/weixin_42997255/article/details/100090114
        """
        
        newItem_element=Element('item')
        new_start_date=Element('start_date')
        new_start_date.text='2023-12-31'
        newItem_element.append(new_start_date)

        new_end_date=Element('end_date')
        new_end_date.text='2023-12-31'
        newItem_element.append(new_end_date)

        new_alarm_time=Element('alarm_time')
        new_alarm_time.text='12:00:00'
        newItem_element.append(new_alarm_time)

        new_message=Element('message')
        new_message.text=alarm_str#'2023-12-31'
        newItem_element.append(new_message)

        root.append(newItem_element)
        tree.write('config.xml',encoding='utf-8',xml_declaration=True)
        """
        # endregion

        pass
        #self.alarm_str_lineEdit

        return

if __name__ == "__main__":
    app = QApplication([])
    configxml_window = addXML()
    #configxml_window.window.show()
    configxml_window.show()
    sys.exit(app.exec_())
