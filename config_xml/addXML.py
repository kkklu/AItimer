# This Python file uses the following encoding: utf-8
import sys
from PySide2.QtWidgets import QApplication, QWidget,QMessageBox,QDialog,QPushButton
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import QFile,QIODevice
import add_Xml_ui

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
    
    def savexml():
        return

if __name__ == "__main__":
    app = QApplication([])
    configxml_window = addXML()
    #configxml_window.window.show()
    configxml_window.show()
    sys.exit(app.exec_())
