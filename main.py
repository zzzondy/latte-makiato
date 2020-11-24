from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidgetItem, QTableView, QWidget
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
        self.add_edit.clicked.connect(self.openAddEditCoffee)
        self.update.clicked.connect(self.update_result)
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

    def openAddEditCoffee(self):
        self.addEdit = AddEditCoffee()
        self.addEdit.show()


class AddEditCoffee(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('addEditCoffeeForm.ui', self)
        self.initUI()

    def initUI(self):
        self.add_coffee.clicked.connect(self.add)
        self.edit_coffee.clicked.connect(self.edit)

    def add(self):
        self.addCoffeeForm = AddCoffee()
        self.addCoffeeForm.show()

    def edit(self):
        self.editCoffeeForm = EditCoffee()
        self.editCoffeeForm.show()


class AddCoffee(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('addCoffee.ui', self)
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Добавить запись о кофе')
        self.con = sqlite3.connect('coffee.db')
        self.add_coffee.clicked.connect(self.add_value)

    def add_value(self):
        cur = self.con.cursor()
        que = "INSERT INTO coffee VALUES(" + self.id.text() + ", '" + self.sort.text() + \
              "', '" + self.hot.text() + "', '" + self.type.text() + "', '" + self.tasty.text() + "', " + \
              self.price.text() + ", " + self.volume.text() + ")"
        cur.execute(que)
        self.con.commit()
        self.close()


class EditCoffee(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('editCoffee.ui', self)
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Изменить запись о кофе')
        self.con = sqlite3.connect('coffee.db')
        self.modified = {}
        self.titles = None
        self.tableWidget.horizontalHeader().resizeSection(2, 150)
        self.tableWidget.horizontalHeader().resizeSection(3, 150)
        self.tableWidget.itemChanged.connect(self.item_changed)
        self.save_table.clicked.connect(self.save_results)
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

    def item_changed(self, item):
        """Контролирует изменения."""
        # Если значение в ячейке было изменено,
        # то в словарь записывается пара: название поля, новое значение
        self.modified[self.titles[item.column()]] = item.text()

    def save_results(self):
        """Сохраняет таблицу если есть изменения."""
        if self.modified:
            cur = self.con.cursor()
            que = "UPDATE coffee SET\n"
            for key in self.modified.keys():
                que += "{}='{}'\n".format(key, self.modified.get(key))
            que += "WHERE id = ?"
            cur.execute(que, (self.spinBox.text(),))
            self.con.commit()
            self.modified.clear()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = CoffeeTable()
    ex.show()
    sys.exit(app.exec_())
