# This Python file uses the following encoding: utf-8
import sys
from PySide2.QtWidgets import QApplication, QWidget,QMessageBox,QDialog,QPushButton
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import QFile,QIODevice,qDebug
import add_Xml_ui

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
        self.save_buttonBox.clicked.connect(self.savexml)
            
        pass  # call __init__(self) of the custom base class here
    
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
        pass
        #self.alarm_str_lineEdit

        return

if __name__ == "__main__":
    app = QApplication([])
    configxml_window = addXML()
    #configxml_window.window.show()
    configxml_window.show()
    sys.exit(app.exec_())
