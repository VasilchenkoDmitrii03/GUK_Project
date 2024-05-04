import sys
import os

parent_directory = os.path.abspath('..')
sys.path.append(parent_directory)

import sqlite3

from PyQt5.QtCore import QSize, QDate, Qt
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from PyQt5.QtWidgets import QSplitter, QLCDNumber, QTextEdit, QSplitter, QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QTableWidget, \
    QTableWidgetItem, QDialog, QFileDialog, QLabel, QGridLayout, QLineEdit, QComboBox, QAbstractItemView, QMessageBox, \
    QAction, QToolBar, QCheckBox, QStatusBar, QCalendarWidget
from PyQt5.QtGui import QColor, QIcon, QPixmap
from PyQt5.QtCore import Qt

import MyQTWidgets.checkableComboBox
import MyQTWidgets.CheckableComboBoxesList
import StaticResources.TableData
from MyQTWidgets import checkableComboBox
from PyQt5.uic.properties import QtWidgets


from StaticResources import TableData

DATABASE_PATH = "GUK_MAIN_DB.db"


class EditRowDialog(QDialog):
    def __init__(self, student):
        super().__init__(None)

        self.setWindowTitle('Изменение строки')
        self.column_names = StaticResources.TableData.getShortTableRows()

        layout = QGridLayout()

        self.labels = []
        self.line_edits = []

        print('Building columns')
        for i in range(1, len(self.column_names)):
            cur_name = self.column_names[i]
            label = QLabel(cur_name, self)
            #label.text = student[i-1]
            if cur_name in TableData.getRussianColumnNames().keys():
                combo_box = QComboBox(self)
                lst = TableData.getColumnValues()[TableData.getRussianColumnNames()[cur_name]]
                combo_box.addItems(lst)
                combo_box.setCurrentText(student[i-1])
                self.labels.append(label)
                self.line_edits.append(combo_box)
                layout.addWidget(label, i, 0)
                layout.addWidget(combo_box, i, 1)
            elif cur_name == 'Число, год рождения':
                calendar = QCalendarWidget(self)
                strs = student[i-1].split('-')
                date = QDate(int(strs[2]), int(strs[1]), int(strs[0]))

                calendar.setSelectedDate(date)
                self.labels.append(label)
                self.line_edits.append(calendar)
                layout.addWidget(label, i, 0)
                layout.addWidget(calendar, i, 1)
            else:
                line_edit = QLineEdit(self)
                line_edit.setText(student[i-1])
                self.labels.append(label)
                self.line_edits.append(line_edit)
                layout.addWidget(label, i, 0)
                layout.addWidget(line_edit, i, 1)

        self.add_button = QPushButton('Добавить', self)
        self.add_button.clicked.connect(self.accept)

        layout.addWidget(self.add_button, 10, 0, 1, 2)

        self.setLayout(layout)

    def get_data(self):
        lst = []
        for inp in self.line_edits:
            if isinstance(inp, QComboBox):
                lst.append(inp.currentText())
            elif isinstance(inp, QCalendarWidget):
                lst.append(inp.selectedDate().toString("dd-MM-yyyy"))
            else:
                lst.append(inp.text())
        return lst
        #return [input.currentText() if isinstance(input, QComboBox) else input.text() for input in self.line_edits]


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.design_set()
        self.db()
        self.update_table_view()

    def keyPressEvent(self, event):
        if event.modifiers() == Qt.ControlModifier and event.key() == Qt.Key_D:
            self.close()
        else:
            super().keyPressEvent(event)
    #FORM DESIGN
    def table_settings(self):
        self.table = QTableWidget()
        self.column_names =  TableData.getTableRows()
        self.table.setColumnCount(len(self.column_names))
        self.table.setHorizontalHeaderLabels(self.column_names)
        self.table.resizeColumnsToContents()
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionMode(QTableWidget.ExtendedSelection)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.horizontalHeader().setStretchLastSection(True)

    def design_set(self):
        self.setWindowTitle('Главное окно')

        self.create_menu()
        self.table_settings()

        self.add_row_button = QPushButton('Редактировать строку')
        self.add_row_button.clicked.connect(self.edit_row)
        self.table.selectedItems()

        self.export_button = QPushButton('Экспорт в CSV')
        self.export_button.clicked.connect(self.clever_export)

        self.statistic_button = QPushButton('Статистика')
        self.statistic_button.clicked.connect(self.create_statistic)
        self.import_button = QPushButton('Импорт из CSV')
        self.import_button.clicked.connect(self.import_csv)
        self.FilterButton = QPushButton('Применить фильтры')
        self.FilterButton.clicked.connect(self.update_table_filter_view)
        self.SurnameTextBox = QLineEdit()
        self.create_filter_widget()
        central_widget = QWidget()

        layout = QVBoxLayout(central_widget)
        layout.addWidget(self.checkable_combobox_list)
        layout.addWidget(self.SurnameTextBox)
        layout.addWidget(self.FilterButton)
        layout.addWidget(self.table)
        layout.addWidget(self.statistic_button)
        layout.addWidget(self.add_row_button)
        layout.addWidget(self.export_button)
        layout.addWidget(self.import_button)

        self.setCentralWidget(central_widget)

    def create_filter_widget(self):
        self.checkable_combobox_list = MyQTWidgets.CheckableComboBoxesList.MyWidget(self)
        self.checkable_combobox_list.setGeometry(200, 150, 150, 30)
        self.checkable_combobox_list.createComboBoxes(StaticResources.TableData.getColumnValues())

    def create_menu(self):
        menu = self.menuBar()
        file_menu = menu.addMenu("&ФАЙЛ")
        button_action_1 = QAction( "&Зарузить данные из ВК", self)
        button_action_1.triggered.connect(self.import_csv)
        file_menu.addAction(button_action_1)
        button_action_2 = QAction("&Загрузить данные из ВВУЗ", self)
        file_menu.addAction(button_action_2)
        button_action_3 = QAction("&Выгрузить данные в ВК", self)
        button_action_3.triggered.connect(self.clever_export)
        file_menu.addAction(button_action_3)

    #Table
    def update_table_view(self):
        self.table.setRowCount(0)
        records = self.sql_request_organizer()
        for i in range(len(records)):
            self.add_row_from_db(i, records[i])

    def update_table_filter_view(self):
        records = self.sql_request_organizer()
        self.table.setRowCount(0)
        for i in range(len(records)):
            self.add_row_from_db(i, records[i])

    def add_row_from_db(self, row_number, lst):
        self.table.insertRow(row_number)
        for i in range(len(lst)):
            self.table.setItem(row_number, i, QTableWidgetItem(str(lst[i])))

    #DataBase
    def db(self):
        connection = sqlite3.connect(DATABASE_PATH)
        connection.close()
        self.create_table()

    def create_table(self):
        connection = sqlite3.connect(DATABASE_PATH)
        cursor = connection.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Students (
        ID  PRIMARY KEY,
        PersonalNumber INTEGER,
        Rang TEXT,
        Sex TEXT NOT NULL,
        Surname TEXT NOT NULL,
        Name TEXT NOT NULL,
        FatherName TEXT,
        Birthday DATETIME NOT NULL,
        Contacts TEXT NOT NULL,
        Status  TEXT,
        SeparateQuota TEXT,
        Graduated BOOL NOT NULL,
        District TEXT NOT NULL,
        Subject TEXT NOT NULL,
        VK TEXT NOT NULL,
        University TEXT, 
        RegistrationDate DATETIME NOT NULL,
        SelectionCriteria TEXT NOT NULL,
        ReferalDate DATETIME NOT NULL,
        DocumentNumber TEXT NOT NULL,
        Note TEXT,
        ADD1, 
        ADD2,
        ADD3,
        ADD4,
        ADD5)''')
        connection.commit()
        connection.close()

    def sql_request_organizer(self):
        connection = sqlite3.connect(DATABASE_PATH)
        cursor = connection.cursor()
        self.checkable_combobox_list.getChosenValues()
        keys = self.checkable_combobox_list.TotalDict.keys()
        request = ''
        for k in keys:
            request += self.sql_request(cursor,k, self.checkable_combobox_list.TotalDict[k]) + 'AND '
        request = request[0:len(request) -4]
        # if surname filter
        surnameReq = self.sql_request_surname()
        if surnameReq != "":
            if len(request) > 0:
                request += " AND "
            request += surnameReq
        if len(request) > 0:
            request = "WHERE " + request
        #cursor.execute(f"SELECT * FROM Students ({request})")
        cursor.execute(f"SELECT * FROM Students {request}")
        records = cursor.fetchall()
        print(records)
        connection.commit()
        connection.close()
        return records

    def sql_request(self, cursor, columnName, valuesList):
        values = ''
        for l in valuesList:
            if columnName != 'PersonalNumber':
                values += "'"+ l +"'" + ","
            else:
                values += l +","
        values = values[0:len(values)-1]
        res = f'{columnName} IN ({values})'
        return res
    
    def sql_request_surname(self):
        if self.SurnameTextBox.text() == "":
            return ""
        return f"instr(Surname, \"{self.SurnameTextBox.text()}\") > 0"
    
    def add_record(self, list:list):
        if not(self.check_record_uniqness(list)):
            return
        try:
            connection = sqlite3.connect(DATABASE_PATH)
            cursor = connection.cursor()

            for i in range(len(list)):
                if i != 1:
                    list[i] = "'" + list[i] + "'"
            # Добавляем нового пользователя
            params = ''
            for s in list:
                params += s + ','
            params = params[0:len(params) - 1]
            columns = 'ID, PersonalNumber, Rang, Sex, Surname, Name, FatherName, Birthday, Contacts, Status, SeparateQuota, Graduated, District, Subject, VK, University, RegistrationDate,SelectionCriteria, ReferalDate, DocumentNumber, Note, ADD1, ADD2, ADD3, ADD4, ADD5'
            cursor.execute(f'INSERT INTO Students ({columns}) VALUES ({params})')
            # Сохраняем изменения и закрываем соединение
            connection.commit()
            connection.close()
        except:
            print("Error occured")
    def check_record_uniqness(self, record:list) -> bool: # if record is unique returns true
        id = str(record[0])
        connection = sqlite3.connect(DATABASE_PATH)
        cursor = connection.cursor()
        cursor.execute(f"SELECT * FROM  Students WHERE ID = {id}")
        tmp = len(cursor.fetchall())
        connection.commit()
        connection.close()
        if tmp == 0:
            return True
        else:
            return False
        #id = str(record[0])
        #try:
        #    connection = sqlite3.connect(DATABASE_PATH)
        #    cursor = connection.cursor()
        #    cursor.execute(f"SELECT * FROM  Students WHERE ID = {id}")
        #    connection.commit()
        #    connection.close()
        #    tmp = len(cursor.fetchall())
        #    return tmp == 0
        #except:
        #    print("Error occured")
        #    return False

    def edit_db_row(self, record:list):
        connection = sqlite3.connect(DATABASE_PATH)
        cursor = connection.cursor()
        columns = StaticResources.TableData.getDBColumnsList()
        columnsStr = ','.join(columns)
        newValues = ','.join(record)
        cursor.execute(f"REPLACE INTO Students ({columnsStr}) VALUES ({newValues});")
        connection.commit()
        connection.close()

    # FUNCTIONS

    def edit_row(self):
        #...
        try:
            student = self.get_selected_row()
            if len(student) == 0:
                return
            id = student[0]
            student = student[1:]
            dialog = EditRowDialog(student)
            if dialog.exec_():
                data = dialog.get_data()
                data.insert(0, str(id))# edited row
                for i in range(5):
                    data.append("")
                for i in range(0, len(data)):
                    if i != 1:
                        data[i] = "'" + data[i] + "'"
                self.edit_db_row(data)
                self.update_table_view()
                #row_position = self.SELECTED_INDEX # ищем строку с нужным номером
                #for i, item in enumerate(data):
                #    self.table.setItem(row_position, i, QTableWidgetItem(item))
                #self.set_column_color(1, QColor('blue'))  # второй столбец
                #self.set_column_color(2, QColor('blue'))
        except:
            print("error occured")
    def get_selected_row(self):
        values = []
        if len(self.table.selectedItems()) == 0:
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Information)
            msg_box.setText('Ни одна строка не выделена')
            msg_box.setStandardButtons(QMessageBox.Ok)
            retval = msg_box.exec_()

            return values
        self.SELECTED_INDEX = int(self.table.selectedItems()[0].row())
        for selected_item in self.table.selectedItems():
            # create [item from col 0, item from col 1]
            values.insert(selected_item.column(), selected_item.text())
        return values

    def create_statistic(self):
        self.statistic_window = StatisticWindow()
        self.statistic_window.setGeometry(200, 300, 500, 600)
        self.statistic_window.show()

    def export_csv(self):
        self.update_table_filter_view()
        file_path, _ = QFileDialog.getSaveFileName(self, "Сохранить как CSV", "", "CSV Files (*.csv)")
        if file_path:
            with open(file_path, 'w') as file:
                for row in range(self.table.rowCount()):
                    line = ','.join([self.table.item(row, column).text() for column in range(self.table.columnCount())])
                    file.write(line + '\n')

    def clever_export(self): #expors only data about VUZ
        used_columns = ['ID', 'University', 'RegistrationDate ', 'SelectionCriteria', 'ReferalDate'] # позже перенести в static resources
        rows = self.get_rows(used_columns)
        file_path, _ = QFileDialog.getSaveFileName(self, "Сохранить как CSV", "", "CSV Files (*.csv)")
        if file_path:
            with open(file_path, 'w') as file:
                for row in rows:
                    file.write(','.join(row).removesuffix(',') + '\n')


    def get_rows(self, columns:list) -> list:
        connection = sqlite3.connect(DATABASE_PATH)
        cursor = connection.cursor()
        str_columns = ''
        for col in columns:
            str_columns += col + ','
        str_columns = str_columns[0:len(str_columns) - 1]
        cursor.execute(f"SELECT {str_columns} from Students")
        records = cursor.fetchall()
        print(records)
        connection.commit()
        connection.close()
        return records
    def import_csv(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Выберите файл CSV", "", "CSV Files (*.csv)")
        if file_path:
            with open(file_path, 'r') as file:
                data = file.readlines()
                for line in data:
                    line_edited = line[0: len(line) -1] # to remove \n at the end
                    row_data = line_edited.split(',')
                    self.add_record(row_data)
                self.update_table_view()

    def set_column_color(self, column, color):
        for row in range(self.table.rowCount()):
            item = self.table.item(row, column)
            if item is not None:
                item.setBackground(color)


class TwoRowsWidget(QWidget):
    def __init__(self, line1, line2):
        super().__init__()
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        label1 = QLabel(line1)
        label2 = QLabel(line2)
        self.layout.addWidget(label1)
        self.layout.addWidget(label2)


class TableWithStudentsInUnis(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT University, COUNT(*) AS количество_студентов
            FROM Students
            GROUP BY University
        ''')
        results = cursor.fetchall()
        for row in results:
            print(row[0], row[1])
        conn.close()
        print(results)

        columns = 3
        rows = len(results) // columns + (1 if len(results) % columns else 0)
        layout = QVBoxLayout()

        self.tableWidget = QTableWidget()
        self.tableWidget.setRowCount(rows if rows else 1)
        self.tableWidget.setColumnCount(columns)  # Только один столбец для QLabel
        print(rows, columns)

        # Устанавливаем минимальный и максимальный размеры для ячеек
        self.tableWidget.horizontalHeader().setDefaultSectionSize(150)
        self.tableWidget.verticalHeader().setDefaultSectionSize(75)
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.horizontalHeader().setVisible(False)

        # Добавляем текстовые метки в ячейки
        for i, text in enumerate(results):
            print(i)
            self.tableWidget.setCellWidget(i // columns, i % columns, TwoRowsWidget(str(text[1]) + ' чел.', str(text[0])))

        layout.addWidget(self.tableWidget)
        self.setLayout(layout)

class StatisticWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Статистика")
        # split_vertical = QSplitter()
        split_horizontal = QSplitter(Qt.Vertical)      
        split_horizontal.setSizes([200, 400])

        self.military_districts()
        tmp1 = TableWithStudentsInUnis()
        gen_area = StatsWidget()
        md_area = self.md_table
        ma_area = tmp1.tableWidget

        # widget_with_map = QLabel()
        # widget_with_map.setPixmap(QPixmap("unnamed.jpg"))

        split_horizontal.addWidget(md_area)
        split_horizontal.addWidget(gen_area)
        split_horizontal.addWidget(ma_area)
        # split_vertical.addWidget(split_horizontal)
        # split_vertical.addWidget(ma_area)
        
        self.setCentralWidget(split_horizontal)        
        self.show()

    def military_districts(self):
        self.md_table = QTableWidget()
        self.column_name = TableData.getColumnValues()['District']
        self.md_table.setColumnCount(len(self.column_name))
        self.md_table.setHorizontalHeaderLabels(sorted(self.column_name))
        self.md_table.resizeColumnsToContents()
        self.md_table.verticalHeader().setVisible(False)
        # Подключение к базе данных
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()

        # Выполнение запроса
        cursor.execute('''
            SELECT District, COUNT(*) AS stud_num
            FROM students
            GROUP BY District 
        ''')

        # Получение результатов
        results = cursor.fetchall()
        # Закрытие соединения с базой данных
        conn.close()
        
        tmp = sorted(self.column_name)
        
        self.md_table.insertRow(0)
        for name, numb in results:
            self.md_table.setItem(0, tmp.index(name), QTableWidgetItem(str(numb)))


class StatsWidget(QTableWidget):
    def __init__(self):
        super().__init__()
        self.setColumnCount(2)        
        self.setRowCount(6)

        self.verticalHeader().setVisible(False)
        self.horizontalHeader().setVisible(False)

        connection = sqlite3.connect(DATABASE_PATH)
        cursor = connection.cursor()

        self.setItem(0, 0, QTableWidgetItem('Кандидатов подало заявлений'))
        students_count = cursor.execute("SELECT COUNT(PersonalNumber) FROM Students").fetchone()
        self.setItem(0, 1, QTableWidgetItem(f'{students_count[0]}'))
        
        self.setItem(1, 0, QTableWidgetItem('Мужчин/Женщин'))
        male_count = cursor.execute("SELECT COUNT(*) FROM Students WHERE Sex = 'M'").fetchone()
        female_count = cursor.execute("SELECT COUNT(*) FROM Students WHERE Sex = 'Ж'").fetchone()
        self.setItem(1, 1, QTableWidgetItem(f'{male_count[0]}/{female_count[0]}'))
        
        self.setItem(2, 0, QTableWidgetItem('Зачислен/Отчислен'))
        join_count = cursor.execute("SELECT COUNT(*) FROM Students WHERE Status = 'зачислен'").fetchone()
        left_count = cursor.execute("SELECT COUNT(*) FROM Students WHERE Status = 'отчислен'").fetchone()
        self.setItem(2, 1, QTableWidgetItem(f'{join_count[0]}/{left_count[0]}'))

        self.setItem(3, 0, QTableWidgetItem('Человек в отдельной квоте'))
        qouta_count = cursor.execute("SELECT COUNT(*) FROM Students WHERE SeparateQuota = 'да'").fetchone()
        self.setItem(3, 1, QTableWidgetItem(f'{qouta_count[0]}')) 
 
        self.setItem(4, 0, QTableWidgetItem('Выпускников СВУ, ПКУ, КК минобороны'))
        graduated_count = cursor.execute("SELECT COUNT(*) FROM Students WHERE Graduated = 'да'").fetchone()
        self.setItem(4, 1, QTableWidgetItem(f'{graduated_count[0]}'))

        connection.commit()
        connection.close()

        self.resizeColumnsToContents()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.setGeometry(200, 300, 2000, 750)
    window.show()
    sys.exit(app.exec_())
