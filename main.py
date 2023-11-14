"""
TODO
1. подписи дат
2. повторная загрузка файлов, крашится
3. стирать базу данных при повторной загрузке файлов

"""
import logging
import os

from PyQt5 import QtWidgets, QtCore, QtGui, Qt
from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
import consol
import sys
import Tools4Data
import Tools4Graph
import numpy as np
import pdb
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class Window(QMainWindow, consol.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.add_functions()
        self.inputListFiles = None
        self.data_range_ok_Button.clicked.connect(self.on_click_data_range_ok_Button)
        #BestSol = Tools4Data.returnBestSolutions()
        #BestXSol = [i[1] for i in BestSol]
        #date_list = Tools4Data.getUniqueDates()
        #Tools4Graph.best_x_chart(date_list, BestXSol, self.test_widget)


    def on_click_data_range_ok_Button(self):
        self.qwer(self.start_dateEdit.text(), self.end_dateEdit.text())

    def add_functions(self):
        self.upload_files_Button.clicked.connect(self.on_click)

    def on_click(self):
        try:
            os.remove('DataBase.db')
        except:
            pass
        self.comboBox.currentIndexChanged.connect(self.selectionchange)
        dlg = QFileDialog.getOpenFileNames(self, "OpenFile")
        self.inputListFiles = dlg[0]
        Tools4Data.fillDataBase(self.inputListFiles)
        date_list = Tools4Data.getUniqueDates()
        date_list.sort()
        self.start_dateEdit.setDisplayFormat("yyyy/MM/dd")
        y, m, d = date_list[0].split("/")
        self.start_dateEdit.setDate(QDate(int(y), int(m), int(d)))
        y, m, d = date_list[-1].split("/")
        self.end_dateEdit.setDisplayFormat("yyyy/MM/dd")
        self.end_dateEdit.setDate(QDate(int(y), int(m), int(d)))
        self.AddDatesToList(date_list)
        self.qwer(date_list[0], date_list[-1])
        for i in date_list:
            self.comboBox.addItem(i)

    def qwer(self, StartDate, EndDate):
        BestSol = Tools4Data.returnBestSolutions(StartDate, EndDate)
        date_list = [i[0].split(" ")[0] for i in BestSol]
        Metrics = Tools4Data.calt_metric(BestSol)
        FilesList = Tools4Data.getNameFiles(self.inputListFiles)
        BestXSol = [i[1] for i in BestSol]
        BestYSol = [i[2] for i in BestSol]
        BestZSol = [i[3] for i in BestSol]
        BestDeltaSol = Tools4Data.getListDelta(BestSol)
        BestXDelta = [i[1] for i in BestDeltaSol]
        BestYDelta = [i[2] for i in BestDeltaSol]
        BestZDelta = [i[3] for i in BestDeltaSol]
        MetricsDelta = Tools4Data.calt_metric(BestDeltaSol)
        Tools4Graph.best_x_chart(date_list, BestXSol, self.best_x)
        Tools4Graph.best_x_chart(date_list, BestYSol, self.best_y)
        Tools4Graph.best_x_chart(date_list, BestZSol, self.best_z)
        Tools4Graph.best_x_chart(date_list, BestXDelta, self.delta_x)
        Tools4Graph.best_x_chart(date_list, BestYDelta, self.delta_y)
        Tools4Graph.best_x_chart(date_list, BestZDelta, self.delta_z)
        Tools4Graph.best_x_chart(BestXSol, BestYSol, self.chart_2d, False, True)
        Tools4Graph.best_3d_chart(BestXSol, BestYSol, BestZSol, self.chart_3d)
        Tools4Data.FillTable(Metrics['x'], self.table_best_x, Metrics['ns'])
        Tools4Data.FillTable(Metrics['y'], self.table_best_y, Metrics['ns'])
        Tools4Data.FillTable(Metrics['z'], self.table_best_y_3, Metrics['ns'])
        Tools4Data.FillTable(MetricsDelta['x'], self.table_delta_x, Metrics['ns'])
        Tools4Data.FillTable(MetricsDelta['y'], self.table_delta_y, Metrics['ns'])
        Tools4Data.FillTable(MetricsDelta['z'], self.table_delta_z, Metrics['ns'])


    def AddDatesToList(self, DateList):
        self.model = QtGui.QStandardItemModel(self)
        self.methods = [Date for Date in DateList]
        for method in self.methods:
            item = QtGui.QStandardItem(method)
            item.setData(method)
            self.model.appendRow(item)
        self.listView.setModel(self.model)

    def selectionchange(self):
        Date = self.comboBox.currentText()
        data = Tools4Data.getListSolutionsForDay(Date)
        MetricsFullDay = Tools4Data.calt_metric(data)
        Tools4Data.FillTable(MetricsFullDay['x'], self.table_full_x, MetricsFullDay['ns'], MetricsFullDay['q'], True)
        Tools4Data.FillTable(MetricsFullDay['y'], self.table_full_y, MetricsFullDay['ns'], MetricsFullDay['q'], True)
        Tools4Data.FillTable(MetricsFullDay['z'], self.table_full_z, MetricsFullDay['ns'], MetricsFullDay['q'], True)
        data = data[::200]
        TimeList = [i[0] for i in data]
        ListXDay = [i[1] for i in data]
        ListYDay = [i[2] for i in data]
        ListZDay = [i[3] for i in data]
        Tools4Graph.best_x_chart(TimeList, ListXDay, self.full_x, True)
        Tools4Graph.best_x_chart(TimeList, ListYDay, self.full_y, True)
        Tools4Graph.best_x_chart(TimeList, ListZDay, self.full_z, True)







def application():
    app = QApplication(sys.argv)
    window = Window()

    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    try:
        pass
        #os.remove(r"C:\Users\Данил\Desktop\project\MonCenterPosViewer\DataBase.db")
    except:
        pass
    application()