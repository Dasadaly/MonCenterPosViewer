import sqlite3
import numpy as np
from pathlib import Path

from PyQt5.QtWidgets import QTableWidgetItem


def fillDataBase(inputListFiles):
    connect = sqlite3.connect("DataBase.db")
    cursor = connect.cursor()
    for ind, d in enumerate(inputListFiles):
        with open(d) as f:
            data = f.read()
            data = data.split("\n")
            start_data_ind = 0
            for i in data:
                if not i[0] == '%':
                    start_data_ind = data.index(i)
                    break
            name_col = ['0'] + data[start_data_ind - 1].split()[1:]
            data = data[start_data_ind:-1]
            data = [data[i].split() for i in range(len(data))]
        if (ind == 0):
            q = "CREATE TABLE DATA ("
            for i, d in enumerate(name_col):
                if (i == 0):
                    continue
                if (i == 1):
                    q += "\"" + d + "\" datetime" + ","
                else:
                    q += "\"" + d + "\" REAL" + ","
            q = q[:-1]
            q += ")"
            cursor.execute(q)
        for i, d in enumerate(data):
            data[i] = [data[i][0] + " " + data[i][1]] + data[i][2:]
        add = "insert into DATA ("
        for i in name_col:
            if (i == "0"):
                continue
            add += "\"" + i + "\"" + ","
        add = add[:-1]
        add += ") VALUES ("
        for i in name_col:
            if (i == "0"):
                continue
            add += "?,"
        add = add[:-1]
        add += ")"
        cursor.executemany(add, data)
        connect.commit()


def returnBestSolutions(StartDate, EndDate):
    con = sqlite3.connect("DataBase.db")
    cursor = con.cursor()
    sql1 = f'''SELECT *,
        [sdx(m)] AS x,
        [sdy(m)] AS y,
        [sdz(m)] AS z
    FROM DATA
    WHERE substr(GPST, 1, 10) BETWEEN '{StartDate}' and '{EndDate}'
    GROUP BY substr(GPST, 1, 10)
    HAVING (x*x + y*y + z*z) = (
        SELECT MIN(x*x + y*y + z*z)
        FROM DATA AS D
        WHERE substr(D.GPST, 1, 10) = substr(GPST, 1, 10)
    );'''
    cursor.execute(sql1)
    data = cursor.fetchall()
    data = [list(item) for item in data]
    for i, d in enumerate(data):
        data[i] = data[i][:-3]
        data[i][1] = round(data[i][1], 4)
        data[i][2] = round(data[i][2], 4)
        data[i][3] = round(data[i][3], 4)
    return data


def calt_metric(best_list):
    listX = [sol[1] for sol in best_list]
    listY = [sol[2] for sol in best_list]
    listZ = [sol[3] for sol in best_list]
    listQ = [sol[4] for sol in best_list]
    listNS = [sol[5] for sol in best_list]

    metric = {
        'x': {
            'max': round(max(listX), 4),
            'min': round(min(listX), 4),
            'Avg': round(sum(listX) / len(listX),4),
            'Std': round(np.std(listX), 4)},
        'y': {
            'max': round(max(listY), 4),
            'min': round(min(listY), 4),
            'Avg': round(sum(listY) / len(listY), 4),
            'Std': round(np.std(listY), 4)},
        'z': {
            'max': round(max(listZ), 4),
            'min': round(min(listZ), 4),
            'Avg': round(sum(listZ) / len(listZ), 4),
            'Std': round(np.std(listZ), 4)},
        'ns': {
            'AvgNS': round(sum(listNS) / len(listNS), 4)
        },
        'q': {
            'PercentQ1': round((listQ.count(1.0) / len(listQ)) * 100, 2),
            'PercentQ2': round((listQ.count(2.0) / len(listQ)) * 100, 2),
            'CountQ1': listQ.count(1.0),
            'CountQ2': listQ.count(2.0),
        }
    }
    return metric


def getNameFiles(inputListFiles):
    ListFile = [Path(File).name for File in inputListFiles]
    return ListFile

def getUniqueDates():
    sql = "SELECT DISTINCT substr(GPST, 1, 10) AS UniqueDates FROM DATA;"
    connect = sqlite3.connect("DataBase.db")
    cursor = connect.cursor()
    cursor.execute(sql)
    UniqueDates = cursor.fetchall()
    UniqueDates = [i[0] for i in UniqueDates]
    return UniqueDates

def getListSolutionsForDay(Date):
    connect = sqlite3.connect("DataBase.db")
    cursor = connect.cursor()
    sql = f"SELECT * FROM DATA where GPST like '%{Date}%'"
    cursor.execute(sql)
    Solutions = cursor.fetchall()
    Solutions = [list(i) for i in Solutions]
    for i, d in enumerate(Solutions):
        Solutions[i][0] = Solutions[i][0].split(" ")[1]
    return Solutions

def getListDelta(best_list):
    deltaBestList = best_list.copy()
    deltaBestList = [list(item) for item in deltaBestList]
    for i, d in enumerate(deltaBestList):
        deltaBestList[i][1] = round(best_list[0][1] - best_list[i][1], 4)
        deltaBestList[i][2] = round(best_list[0][2] - best_list[i][2], 4)
        deltaBestList[i][3] = round(best_list[0][3] - best_list[i][3], 4)
    return deltaBestList


def FillTable(Stats, TableWidget, StatsNs, StatsQ=None, Q=False):
    TableWidget.setItem(0, 0, QTableWidgetItem(str(Stats['min'])))
    TableWidget.setItem(0, 1, QTableWidgetItem(str(Stats['max'])))
    TableWidget.setItem(0, 2, QTableWidgetItem(str(Stats['Avg'])))
    TableWidget.setItem(0, 3, QTableWidgetItem(str(StatsNs['AvgNS'])))
    TableWidget.setItem(0, 4, QTableWidgetItem(str(Stats['Std'])))
    if (Q):
        TableWidget.setItem(0, 5, QTableWidgetItem(str(StatsQ['CountQ1'])))
        TableWidget.setItem(0, 6, QTableWidgetItem(str(StatsQ['CountQ2'])))
        TableWidget.setItem(0, 7, QTableWidgetItem(str(StatsQ['PercentQ1'])))
        TableWidget.setItem(0, 8, QTableWidgetItem(str(StatsQ['PercentQ2'])))




