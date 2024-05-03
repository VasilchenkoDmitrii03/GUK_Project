import sqlite3
import sys

from PyQt5.QtWidgets import QFileDialog, QMainWindow, QLineEdit, QGridLayout, QLabel, QApplication, QWidget, \
    QPushButton, QDialog, QMessageBox, QComboBox, QAction, QTableWidget, QTableWidgetItem

import Authorization.main
import DictionaryModule.basicFunctions


class Authorization(QMainWindow):
    def __init__(self):
        super().__init__()
        self.design_set()

    #DESIGN SETTINGS
    def design_set(self):
        self.Passed = False
        self.setWindowTitle('Справочники')
        self.ComboBoxLabel = QLabel("Текущий справочник")
        self.DictComboBox = QComboBox()
        self.DictComboBox.currentIndexChanged.connect(self.changedComboBox)
        self.updateComboBoxItems()
        self.AddButton = QPushButton("Новый справочник")
        self.AddButton.clicked.connect(self.newDictionary)
        self.create_menu()
        self.ComboBoxLabel.setAutoFillBackground(True)
        central_widget = QWidget()

        self.layout = QGridLayout(central_widget)

        self.layout.addWidget(self.ComboBoxLabel, 1, 0)
        self.layout.addWidget(self.DictComboBox, 2, 0)
        self.layout.addWidget(self.AddButton, 0, 0)

        self.layout.setColumnMinimumWidth(0, 150)
        self.layout.setColumnMinimumWidth(1, 150)
        self.layout.setColumnMinimumWidth(2, 150)
        self.create_redactor_ui()
        self.setCentralWidget(central_widget)
    def create_menu(self):
        self.menu = self.menuBar()
        file_menu = self.menu.addMenu("&ФАЙЛ")
        button_action_1 = QAction("&Импорт", self)
        button_action_1.triggered.connect(self.import_csv)
        file_menu.addAction(button_action_1)
        button_action_2 = QAction("&Экспорт", self)
        button_action_2.triggered.connect(self.export_csv)
        file_menu.addAction(button_action_2)

    def create_redactor_ui(self):
        self.DeleteButton = QPushButton("Удалить")
        self.DeleteButton.clicked.connect(self.removeDictionary)
        self.AcceptButton = QPushButton("Сохранить изменения")
        self.AcceptButton.clicked.connect(self.saveChanges)
        self.RemoveLastButton = QPushButton("Удалить последний")
        self.RemoveLastButton.clicked.connect(self.removeLastRow)
        self.NameTextBox = QLineEdit()
        self.TableElement = QTableWidget()
        self.AddElementButton = QPushButton("Добавить элемент")
        self.AddElementButton.clicked.connect(self.addRow)
        self.layout.addWidget(self.AcceptButton, 0, 2)
        self.layout.addWidget(self.DeleteButton, 0, 3)
        self.layout.addWidget(QLabel("Имя"),1, 2)
        self.layout.addWidget(self.NameTextBox, 1, 3)
        self.layout.addWidget(QLabel("Элементы справочника"), 2, 2)
        self.layout.addWidget(self.TableElement, 2, 3, 4, 3)
        self.layout.addWidget(self.AddElementButton, 3, 2)
        self.layout.addWidget(self.RemoveLastButton, 4, 2)
        self.changedComboBox(0)
    def addRow(self):

        rowCount = self.TableElement.rowCount()
        self.TableElement.setColumnCount(1)
        self.TableElement.setRowCount(rowCount + 1)
        self.TableElement.setItem(rowCount, 0, QTableWidgetItem("элемент"))
    def removeLastRow(self):
        rowCount = self.TableElement.rowCount()
        self.TableElement.setRowCount(rowCount - 1)
    def changedComboBox(self, index):
        try:
            dictName = list(DictionaryModule.basicFunctions.get_total_dictionary().keys())[index] #выбранный справочник
            values = DictionaryModule.basicFunctions.get_total_dictionary()[dictName]
            self.NameTextBox.setText(dictName)
            self.updateTable(values)
        except:
            print('error')
    def updateTable(self, record:list):
        self.TableElement.setColumnCount(1)
        self.TableElement.setRowCount(len(record))
        for i in range(len(record)):
            self.TableElement.setItem(i, 0, QTableWidgetItem(record[i]))
    def removeDictionary(self):
        index = self.DictComboBox.currentIndex()
        dictName = list(DictionaryModule.basicFunctions.get_total_dictionary().keys())[index]
        DictionaryModule.basicFunctions.remove_dict(dictName)
        self.clearRedactor()
        self.updateComboBoxItems()
    def clearRedactor(self):
        self.TableElement.setRowCount(0)
        self.NameTextBox.setText("")

    def newDictionary(self):
        self.clearRedactor()
        self.NameTextBox.setText("Имя")
        self.addRow()

    def getDataFromTable(self):
        lst = list()
        name = self.NameTextBox.text()
        if name == '':
            msg_box = QMessageBox()
            msg_box.setText("Имя не может быть пустым")
            retval = msg_box.exec_()
            return
        for i in range(self.TableElement.rowCount()):
            lst.append(self.TableElement.item(i, 0).text())
        if len(lst) == 0:
            msg_box = QMessageBox()
            msg_box.setText("Список элементов не может быть пустым")
            retval = msg_box.exec_()
            return
        return (name, lst)
    def saveChanges(self):
        name, lst = self.getDataFromTable()
        if name in DictionaryModule.basicFunctions.get_total_dictionary().keys():
            DictionaryModule.basicFunctions.edit_dict(name, lst)
        else:
            DictionaryModule.basicFunctions.add_dict(name, lst)
        self.updateComboBoxItems()
    def import_csv(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Сохранить как CSV", "", "CSV Files (*.csv)")
        DictionaryModule.basicFunctions.import_csv(file_path)
    def export_csv(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Сохранить как CSV", "", "CSV Files (*.csv)")
        DictionaryModule.basicFunctions.export_csv(file_path)
    def updateComboBoxItems(self):
        self.DictComboBox.clear()
        self.DictComboBox.addItems(DictionaryModule.basicFunctions.get_total_dictionary().keys())




if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Authorization()
    window.setGeometry(200, 300, 1000, 750)
    window.show()
    sys.exit(app.exec_())