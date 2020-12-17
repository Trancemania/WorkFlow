import sys
import os
import re
sys.path.append(os.path.dirname(os.path.abspath('__file__')))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath('__file__'))))
from WorkFlow_Editor_UI import Ui_MainWindow
from WorkFlow import WorkFlow
from PyQt5 import QtCore, QtGui, QtWidgets
import threading
import time
import csv

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtWidgets.QApplication.UnicodeUTF8


    def _translate(context, text, disambig):
        return QtWidgets.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtWidgets.QApplication.translate(context, text, disambig)


class WorkFlowEditor(Ui_MainWindow, QtCore.QObject):
    show_di_status_signal = QtCore.pyqtSignal(int, int)

    def __init__(self, MainWindow):
        super(WorkFlowEditor, self).__init__()
        self.setupUi(MainWindow)
        self.MainWindow = MainWindow
        self.wf = WorkFlow()
        self.position_measurement_flag = False  # 位置测量标志
        self.rgb_measurement_flag = False  # rgb测量标志
        # 添加workflow类别
        for flow_name in ['所有Work', '点击', '输入', '特殊键', '软件控制']:
            self.comboBox_add_work.addItem(flow_name)
        self.all_events()  # 绑定事件

    def all_events(self):
        # 绑定事件
        self.pushButton_position_measurement.clicked.connect(self.thread_get_position)
        self.pushButton_rgb_measurement.clicked.connect(self.thread_get_rgb)
        self.pushButton_add_workflow.clicked.connect(self.add_workflow)
        self.pushButton_remove_workflow.clicked.connect(self.remove_workflow)
        self.comboBox_add_work.currentTextChanged.connect(self.add_work)
        self.pushButton_remove_work.clicked.connect(self.remove_work)
        self.action_save_workflow.triggered.connect(self.save_workflow)
        self.action_open_workflow.triggered.connect(self.open_workflow)

    def save_workflow(self):
        """保存workflow"""
        if not os.path.exists('./Workflow_Files'):
            os.mkdir('./Workflow_Files')
        for i in range(self.tabWidget.count()):
            with open('./Workflow_Files/%s.csv'%self.tabWidget.tabText(i), 'w+') as f:
                csv_writer = csv.writer(f)
                for row in range(20):
                    row_data = []
                    for col in range(20):
                        wdt = eval('self.table_%s' % i).cellWidget(row,col)
                        if not wdt:
                            row_data.append('')
                        if str(type(wdt)) in ["<class 'PyQt5.QtWidgets.QPushButton'>",
                                              "<class 'PyQt5.QtWidgets.QLabel'>",
                                              "<class 'PyQt5.QtWidgets.QLineEdit'>"]:
                            wdt_class = re.findall(r"<class '(.*)'>", str(type(wdt)), re.S)[0]
                            row_data.append(wdt_class + '_' + str(wdt.text()))
                        if str(type(wdt)) in ["<class 'PyQt5.QtWidgets.QComboBox'>"]:
                            wdt_class = re.findall(r"<class '(.*)'>", str(type(wdt)), re.S)[0]
                            row_data.append(wdt_class + '_' + str(wdt.currentText()))
                        if str(type(wdt)) in ["<class 'PyQt5.QtWidgets.QSpinBox'>"]:
                            wdt_class = re.findall(r"<class '(.*)'>", str(type(wdt)), re.S)[0]
                            row_data.append(wdt_class + '_' + str(wdt.value()))
                    csv_writer.writerow(row_data)

    def open_workflow(self):
        """打开workflow"""
        #打开文件对话框选择workflow文件
        files,file_type = QtWidgets.QFileDialog.getOpenFileNames(self.MainWindow,"打开Workflow文件",'./Workflow_Files',"Csv Files (*.csv)")
        for workflow_path in files:
            #创建workflow
            tab_name = os.path.split(workflow_path)[-1].split('.')[0]
            workflow_tab = self.add_workflow_tab(tab_name)
            #添加work
            with open(workflow_path,'r') as f:
                all_lines = f.readlines()
                for row in range(20):
                    row_data = all_lines[row].split(',')
                    try:
                        work = row_data[0].split('_',1)[1].split('_',1)[1]
                        self.add_work(work)

                        for col in range(20):
                            wdt = workflow_tab.cellWidget(row, col)
                            wdt_content = row_data[col]
                            if wdt_content != '':
                                try:
                                    wdt_class, wdt_text = wdt_content.split('_', 1)
                                except:
                                    continue
                                if wdt_class in ["PyQt5.QtWidgets.QPushButton",
                                                 "PyQt5.QtWidgets.QLabel",
                                                 "PyQt5.QtWidgets.QLineEdit"]:
                                    wdt.setText(wdt_text)
                                if wdt_class in ["PyQt5.QtWidgets.QComboBox"]:
                                    exist_flag = False
                                    for i in range(wdt.count()):
                                        if wdt_text == wdt.itemText(i):
                                            exist_flag = True
                                            break
                                    if not exist_flag:
                                        wdt.addItem(wdt_text)
                                    wdt.setCurrentText(wdt_text)
                                if wdt_class in ["PyQt5.QtWidgets.QSpinBox"]:
                                    wdt.setValue(int(wdt_text))
                    except:
                        pass

    def add_workflow_tab(self,text):
        # 新建tab
        tab_count = self.tabWidget.count()
        exec('self.tab_%s = QtWidgets.QWidget()' % (tab_count))
        # 新建table
        exec('self.table_%s = QtWidgets.QTableWidget(self.tab_%s)' % (tab_count, tab_count))
        eval('self.table_%s' % tab_count).setShowGrid(False)  # 隐藏表格线
        eval('self.table_%s' % tab_count).setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)  # 禁止编辑
        # table.setGeometry(QtCore.QRect(130, 70, 256, 192))
        # eval('table_%s'%tab_count).setObjectName("tableWidget")
        eval('self.table_%s' % tab_count).setColumnCount(20)
        eval('self.table_%s' % tab_count).setRowCount(20)
        for i in range(20):  # 设置列宽
            eval('self.table_%s' % tab_count).setColumnWidth(i, 100)
        # eval('self.table_%s'%tab_count).horizontalHeader().setVisible(False)
        exec('self.table_%s_row = 0' % tab_count)  # 初始化已有行数
        # table.verticalHeader().setVisible(False)
        horizontal_layout = QtWidgets.QHBoxLayout(eval('self.tab_%s' % (tab_count)))
        horizontal_layout.addWidget(eval('self.table_%s' % tab_count))
        self.tabWidget.addTab(eval('self.tab_%s' % (tab_count)), str(text))
        self.tabWidget.setCurrentIndex(tab_count)
        return eval('self.table_%s' % (tab_count))

    def add_workflow(self):
        """添加工作流"""
        # 获取工作流名称
        text, okPressed = QtWidgets.QInputDialog.getText(self.MainWindow, "新增工作流", "请输入工作流名称",
                                                         QtWidgets.QLineEdit.Normal, "")
        if okPressed and text != '':
            # 新建tab
            self.add_workflow_tab(text)

    def remove_workflow(self):
        """删除工作流"""
        index = self.tabWidget.currentIndex()
        if index == -1:
            QtWidgets.QMessageBox.information(self.MainWindow, '提示', '当前无可删除的Workflow！')
            return
        reply = QtWidgets.QMessageBox.question(self.MainWindow, '删除工作流',
                                               '是否删除工作流"%s"' % (self.tabWidget.tabText(index)),
                                               QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            self.tabWidget.removeTab(index)

    def add_work(self, work):
        """添加工作步骤"""
        if work == '所有Work':
            return
        # 获取当前工作流tab
        index = self.tabWidget.currentIndex()
        if index == -1:
            QtWidgets.QMessageBox.information(self.MainWindow, '提示', '请先新增Workflow后，再新增Work！')
            self.comboBox_add_work.setCurrentIndex(0)  # 将当前combox切回第一个
            return
        # 创建执行按钮
        pushbutton_1 = QtWidgets.QPushButton()
        pushbutton_1.setText("Work_%s" % str(work))
        pushbutton_1.setStyleSheet("background-color: rgb(255, 255, 0);")
        eval('self.table_%s' % str(index)).setCellWidget(eval('self.table_%s_row' % index), 0, pushbutton_1)

        if str(work) == '点击':
            # 创建lable
            label_1 = QtWidgets.QLabel()
            label_1.setText("在窗口")
            eval('self.table_%s' % str(index)).setCellWidget(eval('self.table_%s_row' % index), 2, label_1)
            # print(eval('self.table_%s' % str(index)).cellWidget(eval('self.table_%s_row'%index),0))  #获取单元格控件
            # 创建下拉控件,显示所有打开的窗口
            combox_1 = QtWidgets.QComboBox()
            all_process = self.wf.get_all_process()
            for p in all_process:
                combox_1.addItem(p)
            eval('self.table_%s' % str(index)).setCellWidget(eval('self.table_%s_row' % index), 3, combox_1)
            # 创建下拉控件，显示所有的鼠标功能
            combox_2 = QtWidgets.QComboBox()
            combox_2.addItem('左键单击')
            combox_2.addItem("左键双击")
            combox_2.addItem("右键单击")
            eval('self.table_%s' % str(index)).setCellWidget(eval('self.table_%s_row' % index), 4, combox_2)
            # 创建lable
            label_2 = QtWidgets.QLabel()
            label_2.setText("坐标")
            eval('self.table_%s' % str(index)).setCellWidget(eval('self.table_%s_row' % index), 5, label_2)
            # 创建spinbox显示x坐标
            spinBox_1 = QtWidgets.QSpinBox()
            spinBox_1.setMaximum(1920)
            spinBox_1.setObjectName("spinBox")
            eval('self.table_%s' % str(index)).setCellWidget(eval('self.table_%s_row' % index), 6, spinBox_1)
            # 创建spinbox显示y坐标
            spinBox_2 = QtWidgets.QSpinBox()
            spinBox_2.setMaximum(1080)
            spinBox_2.setObjectName("spinBox")
            eval('self.table_%s' % str(index)).setCellWidget(eval('self.table_%s_row' % index), 7, spinBox_2)
            # 绑定按钮点击事件
            def button_event():
                app_name = str(combox_1.currentText())
                mouse_info = str(combox_2.currentText())
                if mouse_info == '左键单击':
                    button = 'left'
                    click_times = 1
                if mouse_info == '左键双击':
                    button = 'left'
                    click_times = 2
                if mouse_info == '右键单击':
                    button = 'right'
                    click_times = 1
                position = (spinBox_1.value(),spinBox_2.value())
                self.wf.click_event(app_name, button, position, click_times)
            row = eval('self.table_%s_row' % index)
            pushbutton_1.clicked.connect(button_event)
        if str(work) == '输入':
            # 创建lable
            label_1 = QtWidgets.QLabel()
            label_1.setText("在窗口")
            eval('self.table_%s' % str(index)).setCellWidget(eval('self.table_%s_row' % index), 2, label_1)
            # 创建下拉控件,显示所有打开的窗口
            combox_1 = QtWidgets.QComboBox()
            all_process = self.wf.get_all_process()
            for p in all_process:
                combox_1.addItem(p)
            eval('self.table_%s' % str(index)).setCellWidget(eval('self.table_%s_row' % index), 3, combox_1)
            # 创建lable
            label_2 = QtWidgets.QLabel()
            label_2.setText("坐标")
            eval('self.table_%s' % str(index)).setCellWidget(eval('self.table_%s_row' % index), 4, label_2)
            # 创建spinbox显示x坐标
            spinBox_1 = QtWidgets.QSpinBox()
            spinBox_1.setMaximum(1920)
            spinBox_1.setObjectName("spinBox")
            eval('self.table_%s' % str(index)).setCellWidget(eval('self.table_%s_row' % index), 5, spinBox_1)
            # 创建spinbox显示y坐标
            spinBox_2 = QtWidgets.QSpinBox()
            spinBox_2.setMaximum(1080)
            spinBox_2.setObjectName("spinBox")
            eval('self.table_%s' % str(index)).setCellWidget(eval('self.table_%s_row' % index), 6, spinBox_2)
            # 创建lable
            label_3 = QtWidgets.QLabel()
            label_3.setText("输入")
            eval('self.table_%s' % str(index)).setCellWidget(eval('self.table_%s_row' % index), 7, label_3)
            # 创建linededit,输入内容
            line_edit_1 = QtWidgets.QLineEdit()
            eval('self.table_%s' % str(index)).setCellWidget(eval('self.table_%s_row' % index), 8, line_edit_1)
            # 绑定按钮点击事件
            def button_event():
                app_name = str(combox_1.currentText())
                position = (spinBox_1.value(),spinBox_2.value())
                text = str(line_edit_1.text())
                self.wf.input_event(app_name,position,text)
            row = eval('self.table_%s_row' % index)
            pushbutton_1.clicked.connect(button_event)
        if str(work) == '特殊键':
            # 创建lable
            label_1 = QtWidgets.QLabel()
            label_1.setText("键盘动作")
            eval('self.table_%s' % str(index)).setCellWidget(eval('self.table_%s_row' % index), 2, label_1)
            # 创建下拉控件,显示所有特殊键
            combox_1 = QtWidgets.QComboBox()
            for p in ['enter','esc','tab','command','capslock','shift','ctrl','alt', 'backspace','delete']:
                combox_1.addItem(p)
            eval('self.table_%s' % str(index)).setCellWidget(eval('self.table_%s_row' % index), 3, combox_1)

            # 绑定按钮点击事件
            def button_event():
                key = str(combox_1.currentText())
                self.wf.single_keyboard_event(key)
            row = eval('self.table_%s_row' % index)
            pushbutton_1.clicked.connect(button_event)
        if str(work) == '软件控制':
            # 创建下拉控件,显示所有软件控制功能
            combox_1 = QtWidgets.QComboBox()
            for p in ['打开软件','关闭软件','重启软件']:
                combox_1.addItem(p)
            eval('self.table_%s' % str(index)).setCellWidget(eval('self.table_%s_row' % index), 2, combox_1)
            # 创建button选择app路径
            pushbutton_app = QtWidgets.QPushButton()
            pushbutton_app.setText("选择软件")
            eval('self.table_%s' % str(index)).setCellWidget(eval('self.table_%s_row' % index), 3, pushbutton_app)
            #创建label显示app路径
            label_1 = QtWidgets.QLabel()
            label_1.setText("")
            eval('self.table_%s' % str(index)).setCellWidget(eval('self.table_%s_row' % index), 4, label_1)
            # 绑定选择app按钮点击事件
            app_path = ''
            def select_app():
                app_path, file_type = QtWidgets.QFileDialog.getOpenFileName(self.MainWindow, '选择软件', '/Applications','*.app')
                label_1.setText(app_path)
            pushbutton_app.clicked.connect(select_app)
            # 绑定运行按钮点击事件
            def button_event():
                app_control_type = str(combox_1.currentText())
                app_path = str(label_1.text())
                self.wf.app_control_event(app_control_type,app_path)
            row = eval('self.table_%s_row' % index)
            pushbutton_1.clicked.connect(button_event)

        # 将需要编辑的单元格背景颜色设为绿色
        for r in range(20):
            for c in range(1, 20):
                try:
                    widget = eval('self.table_%s' % str(index)).cellWidget(r, c)
                    if type(widget) != QtWidgets.QLabel:
                        widget.setStyleSheet("background-color: rgb(0, 255, 0);")
                except:
                    pass

        exec('self.table_%s_row += 1' % index)  # 当前行数+1
        self.comboBox_add_work.setCurrentIndex(0)  # 将当前combox切回第一个

    def remove_work(self):
        # 获取当前工作流tab
        index = self.tabWidget.currentIndex()
        if index == -1 or eval('self.table_%s_row' % index) == 0:
            QtWidgets.QMessageBox.information(self.MainWindow, '提示', '当前无可删除的Work！')
            return
        row = eval('self.table_%s' % str(index)).currentIndex().row()  # 获取选中文本所在的行
        col = eval('self.table_%s' % str(index)).currentIndex().column()  # 获取选中文本所在的列
        if row == -1:
            QtWidgets.QMessageBox.information(self.MainWindow, '提示', '请先选中某一行后，再移除Work！')
            return
        #TODO:禁止删除空行
        reply = QtWidgets.QMessageBox.question(self.MainWindow, '删除工作流', '是否删除第%s行工作' % str(row + 1),
                                               QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            eval('self.table_%s' % str(index)).removeRow(row)
            exec('self.table_%s_row -= 1' % index)  # 当前行数-1
            eval('self.table_%s' % str(index)).setRowCount(20)

    def show_position(self):
        """刷新坐标值"""
        while self.position_measurement_flag:
            position = self.wf.position_measurement()
            self.label_position_measurement.setText(str(position))

    def thread_get_position(self):
        """刷新坐标线程"""
        if not self.position_measurement_flag:
            self.position_measurement_flag = True
            t = threading.Thread(target=self.show_position)
            t.setDaemon(True)
            t.start()
        else:
            self.position_measurement_flag = False

    def show_rgb(self):
        """刷新rgb值"""
        while self.rgb_measurement_flag:
            rgb = self.wf.rgb_measurement()
            self.label_rgb_measurement.setText(str(rgb))

    def thread_get_rgb(self):
        """刷新rgb线程"""
        if not self.rgb_measurement_flag:
            self.rgb_measurement_flag = True
            t = threading.Thread(target=self.show_rgb)
            t.setDaemon(True)
            t.start()
        else:
            self.rgb_measurement_flag = False


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = WorkFlowEditor(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
