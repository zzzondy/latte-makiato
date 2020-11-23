from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidgetItem, QTableView
from PyQt5 import uic
import sqlite3
import sys


class CoffeeTable(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Таблица кофиев')
        self.con = sqlite3.connect('coffee.db')
        self.modified = {}
        self.titles = None
        self.tableWidget.horizontalHeader().resizeSection(2, 150)
        self.tableWidget.horizontalHeader().resizeSection(3, 150)
        self.update_result()

    def update_result(self):
        cur = self.con.cursor()
        result = cur.execute("SELECT * FROM coffee").fetchall()
        self.tableWidget.setRowCount(len(result))
        self.tableWidget.setColumnCount(len(result[0]))
        self.titles = [description[0] for description in cur.description]
        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))
        self.modified = {}


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = CoffeeTable()
    ex.show()
    sys.exit(app.exec_())