# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'add_Xml.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(239, 289)
        self.save_buttonBox = QDialogButtonBox(Dialog)
        self.save_buttonBox.setObjectName(u"save_buttonBox")
        self.save_buttonBox.setGeometry(QRect(20, 240, 171, 21))
        self.save_buttonBox.setOrientation(Qt.Horizontal)
        self.save_buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Save)
        self.alarm_str_lineEdit = QLineEdit(Dialog)
        self.alarm_str_lineEdit.setObjectName(u"alarm_str_lineEdit")
        self.alarm_str_lineEdit.setGeometry(QRect(40, 200, 161, 21))
        self.label_4 = QLabel(Dialog)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(40, 170, 61, 16))
        self.widget = QWidget(Dialog)
        self.widget.setObjectName(u"widget")
        self.widget.setGeometry(QRect(40, 30, 161, 131))
        self.gridLayout = QGridLayout(self.widget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.start_date = QDateEdit(self.widget)
        self.start_date.setObjectName(u"start_date")

        self.verticalLayout_2.addWidget(self.start_date)

        self.end_date = QDateEdit(self.widget)
        self.end_date.setObjectName(u"end_date")

        self.verticalLayout_2.addWidget(self.end_date)

        self.alarm_time = QTimeEdit(self.widget)
        self.alarm_time.setObjectName(u"alarm_time")

        self.verticalLayout_2.addWidget(self.alarm_time)


        self.gridLayout.addLayout(self.verticalLayout_2, 0, 1, 1, 1)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(self.widget)
        self.label.setObjectName(u"label")

        self.verticalLayout.addWidget(self.label)

        self.label_2 = QLabel(self.widget)
        self.label_2.setObjectName(u"label_2")

        self.verticalLayout.addWidget(self.label_2)

        self.label_3 = QLabel(self.widget)
        self.label_3.setObjectName(u"label_3")

        self.verticalLayout.addWidget(self.label_3)


        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)


        self.retranslateUi(Dialog)
        self.save_buttonBox.accepted.connect(Dialog.accept)
        self.save_buttonBox.rejected.connect(Dialog.reject)
        #self.save_buttonBox.clicked.connect(self.savexml)
        #这个自动生成的代码不要去编辑也不要去修改
        #https://blog.csdn.net/u012561176/article/details/135022040

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi
    #def savexml():
        #这是加入保存xml的程序


    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"\u73e0\u6d77\u7535\u53f0AI\u667a\u80fd\u8bed\u97f3\u63d0\u9192", None))
        self.label_4.setText(QCoreApplication.translate("Dialog", u"\u63d0\u9192\u8bed\u97f3\uff1a", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"\u5f00\u59cb\u65e5\u671f\uff1a", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"\u7ed3\u675f\u65e5\u671f\uff1a", None))
        self.label_3.setText(QCoreApplication.translate("Dialog", u"\u63d0\u9192\u65f6\u95f4\uff1a", None))
    # retranslateUi

