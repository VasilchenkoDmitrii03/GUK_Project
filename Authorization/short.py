import sqlite3
import sys

from PyQt5.QtWidgets import QFileDialog, QMainWindow, QLineEdit, QGridLayout, QLabel, QApplication, QWidget, \
    QPushButton, QDialog, QMessageBox

import Authorization.main


class Authorization(QDialog):
    def __init__(self):
        super().__init__()
        self.design_set()
        self.create_db()

    #DESIGN SETTINGS
    def design_set(self):
        self.Passed = False
        self.setWindowTitle('Авторизация')
        self.LoginTextBox = QLineEdit()
        self.PasswordTextBox = QLineEdit()
        self.LineEdits = [self.LoginTextBox, self.PasswordTextBox]
        self.LabelsText = ['Логин', 'Пароль']

        self.CancelButton = QPushButton("Отмена")
        self.CancelButton.clicked.connect(self.cancelClick)
        self.OkButton = QPushButton("Ок")
        self.OkButton.clicked.connect(self.okClick)
        self.RegisterButton = QPushButton("Регистрация")
        self.RegisterButton.clicked.connect(self.registrationClick)

        self.layout = QGridLayout()
        for i in range(len(self.LabelsText)):
            self.layout.addWidget(QLabel(self.LabelsText[i]),i, 0)
            self.layout.addWidget(self.LineEdits[i], i, 1)
        self.layout.addWidget(self.RegisterButton, 2, 1)
        self.layout.addWidget(self.CancelButton, 2, 0)
        self.layout.addWidget(self.OkButton, 3, 0)
        self.setLayout(self.layout)
    def create_db(self):
        try:
            connection = sqlite3.connect('users_db.db')
            cursor = connection.cursor()
            cursor.execute('''
                    CREATE TABLE IF NOT EXISTS Users (
                    Organization TEXT, 
                    Login  TEXT PRIMARY KEY,
                    Password TEXT, 
                    Surname TEXT, 
                    Name TEXT, 
                    FatherName TEXT,
                    Post TEXT, 
                    Contacts TEXT,
                    Add1 TEXT, 
                    Add2 TEXT,
                    Add3 TEXT,
                    Add4 TEXT
                    );''')
            connection.commit()
            cursor.close()
            connection.close()
        except:
            print('error')
    def add_new_user(self, record:list):
        try:
            connection = sqlite3.connect('users_db.db')
            cursor = connection.cursor()
            columns = "Organization,  Login ,Password ,Surname , Name, FatherName,Post, Contacts, Add1, Add2,Add3,Add4"
            columnLen = 12
            while len(record) < 12:
                record.append("")
            for i in range(len(record)):
                record[i] = '"' + str(record[i]) + '"'
            params = ','.join(record)
            print(f'INSERT INTO DictData ({columns}) VALUES ({params})')
            cursor.execute(f'INSERT INTO Users ({columns}) VALUES ({params});')
            connection.commit()
            cursor.close()
            connection.close()
        except Exception:
            print(Exception.args)
            msg_box = QMessageBox()
            msg_box.setText("Проверьте корректность данных")
            retval = msg_box.exec_()
    def checkPassword(self, login:str, password:str) -> bool:
        try:
            connection = sqlite3.connect('users_db.db')
            cursor = connection.cursor()
            cursor.execute(f'SELECT * FROM Users WHERE Login = "{login}"')
            value = cursor.fetchall()
            connection.commit()
            cursor.close()
            connection.close()
        except Exception:
            print(Exception.args)
            return False
        if len(value) == 0:
            msg_box = QMessageBox()
            msg_box.setText("Пользователя с таким логином нет")
            retval = msg_box.exec_()
            return False
        elif password != value[0][2]:
            msg_box = QMessageBox()
            msg_box.setText("Неверный пароль")
            retval = msg_box.exec_()
            return False
        return True
    def testcheckPassword(self, login:str, password:str) -> bool:
        connection = sqlite3.connect('users_db.db')
        cursor = connection.cursor()
        cursor.execute(f'SELECT * FROM Users WHERE Login = "{login}"')
        value = cursor.fetchall()
        connection.commit()
        cursor.close()
        connection.close()
    def registrationClick(self):
        dialog = Authorization.main.Regisration()
        if dialog.exec_():
            self.add_new_user(dialog.get_data())
    def okClick(self):
        self.Accepted = self.checkPassword(self.LoginTextBox.text(), self.PasswordTextBox.text())
        if self.Accepted:
            self.accept()
    def cancelClick(self):
        self.Accepted = False
        self.accept()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Authorization()
    window.setGeometry(200, 300, 250, 120)
    window.show()
    sys.exit(app.exec_())