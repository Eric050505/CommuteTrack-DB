# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'query_adjacent_stations.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_modify_L(object):
    def setupUi(self, modify_L):
        modify_L.setObjectName("modify_L")
        modify_L.resize(800, 601)
        self.id = QtWidgets.QLabel(modify_L)
        self.id.setGeometry(QtCore.QRect(40, 40, 150, 20))
        self.id.setObjectName("id")
        self.OK = QtWidgets.QPushButton(modify_L)
        self.OK.setGeometry(QtCore.QRect(640, 480, 150, 46))
        self.OK.setObjectName("OK")
        self.Exit = QtWidgets.QPushButton(modify_L)
        self.Exit.setGeometry(QtCore.QRect(640, 540, 150, 46))
        self.Exit.setObjectName("Exit")
        self.textBrowser = QtWidgets.QTextBrowser(modify_L)
        self.textBrowser.setGeometry(QtCore.QRect(40, 400, 500, 192))
        self.textBrowser.setObjectName("textBrowser")
        self.id_input = QtWidgets.QLineEdit(modify_L)
        self.id_input.setGeometry(QtCore.QRect(190, 40, 291, 20))
        self.id_input.setObjectName("id_input")
        self.station_input = QtWidgets.QLineEdit(modify_L)
        self.station_input.setGeometry(QtCore.QRect(190, 100, 291, 20))
        self.station_input.setText("")
        self.station_input.setObjectName("station_input")
        self.station = QtWidgets.QLabel(modify_L)
        self.station.setGeometry(QtCore.QRect(40, 100, 150, 20))
        self.station.setObjectName("station")
        self.n = QtWidgets.QLabel(modify_L)
        self.n.setGeometry(QtCore.QRect(40, 160, 150, 20))
        self.n.setObjectName("n")
        self.n_input = QtWidgets.QLineEdit(modify_L)
        self.n_input.setGeometry(QtCore.QRect(190, 160, 291, 20))
        self.n_input.setText("")
        self.n_input.setObjectName("n_input")

        self.retranslateUi(modify_L)
        QtCore.QMetaObject.connectSlotsByName(modify_L)

    def retranslateUi(self, modify_L):
        _translate = QtCore.QCoreApplication.translate
        modify_L.setWindowTitle(_translate("modify_L", "Form"))
        self.id.setText(_translate("modify_L", "line id:"))
        self.OK.setText(_translate("modify_L", "OK"))
        self.Exit.setText(_translate("modify_L", "Exit"))
        self.station.setText(_translate("modify_L", "station id:"))
        self.n.setText(_translate("modify_L", "input n:"))
