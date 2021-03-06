# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'WorkFlow_Editor_UI.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1124, 861)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName("tabWidget")
        self.verticalLayout.addWidget(self.tabWidget)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_add_workflow = QtWidgets.QLabel(self.centralwidget)
        self.label_add_workflow.setObjectName("label_add_workflow")
        self.horizontalLayout.addWidget(self.label_add_workflow)
        self.pushButton_add_workflow = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_add_workflow.setObjectName("pushButton_add_workflow")
        self.horizontalLayout.addWidget(self.pushButton_add_workflow)
        self.pushButton_remove_workflow = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_remove_workflow.setObjectName("pushButton_remove_workflow")
        self.horizontalLayout.addWidget(self.pushButton_remove_workflow)
        self.label_add_work = QtWidgets.QLabel(self.centralwidget)
        self.label_add_work.setObjectName("label_add_work")
        self.horizontalLayout.addWidget(self.label_add_work)
        self.comboBox_add_work = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_add_work.setObjectName("comboBox_add_work")
        self.horizontalLayout.addWidget(self.comboBox_add_work)
        self.pushButton_remove_work = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_remove_work.setObjectName("pushButton_remove_work")
        self.horizontalLayout.addWidget(self.pushButton_remove_work)
        self.horizontalLayout_2.addLayout(self.horizontalLayout)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.pushButton_position_measurement = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_position_measurement.setObjectName("pushButton_position_measurement")
        self.gridLayout.addWidget(self.pushButton_position_measurement, 0, 0, 1, 1)
        self.label_position_measurement = QtWidgets.QLabel(self.centralwidget)
        self.label_position_measurement.setText("")
        self.label_position_measurement.setObjectName("label_position_measurement")
        self.gridLayout.addWidget(self.label_position_measurement, 0, 1, 1, 1)
        self.pushButton_rgb_measurement = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_rgb_measurement.setObjectName("pushButton_rgb_measurement")
        self.gridLayout.addWidget(self.pushButton_rgb_measurement, 1, 0, 1, 1)
        self.label_rgb_measurement = QtWidgets.QLabel(self.centralwidget)
        self.label_rgb_measurement.setText("")
        self.label_rgb_measurement.setObjectName("label_rgb_measurement")
        self.gridLayout.addWidget(self.label_rgb_measurement, 1, 1, 1, 1)
        self.gridLayout.setColumnStretch(0, 1)
        self.gridLayout.setColumnStretch(1, 2)
        self.horizontalLayout_2.addLayout(self.gridLayout)
        self.horizontalLayout_2.setStretch(0, 5)
        self.horizontalLayout_2.setStretch(1, 3)
        self.horizontalLayout_2.setStretch(2, 2)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1124, 26))
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.action_open_workflow = QtWidgets.QAction(MainWindow)
        self.action_open_workflow.setObjectName("action_open_workflow")
        self.action_save_workflow = QtWidgets.QAction(MainWindow)
        self.action_save_workflow.setObjectName("action_save_workflow")
        self.menu.addAction(self.action_open_workflow)
        self.menu.addAction(self.action_save_workflow)
        self.menubar.addAction(self.menu.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(-1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Workflow Editor"))
        self.label_add_workflow.setText(_translate("MainWindow", "新增WorkFlow"))
        self.pushButton_add_workflow.setText(_translate("MainWindow", "+"))
        self.pushButton_remove_workflow.setText(_translate("MainWindow", "-"))
        self.label_add_work.setText(_translate("MainWindow", "新增Work"))
        self.pushButton_remove_work.setText(_translate("MainWindow", "-"))
        self.pushButton_position_measurement.setText(_translate("MainWindow", "坐标测量"))
        self.pushButton_rgb_measurement.setText(_translate("MainWindow", "RGB测量"))
        self.menu.setTitle(_translate("MainWindow", "文件"))
        self.action_open_workflow.setText(_translate("MainWindow", "打开WorkFlow"))
        self.action_save_workflow.setText(_translate("MainWindow", "保存WorkFlow"))
