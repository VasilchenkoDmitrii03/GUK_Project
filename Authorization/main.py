import sys
import sqlite3
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QTableWidget, \
    QTableWidgetItem, QDialog, QFileDialog, QLabel, QGridLayout, QLineEdit, QComboBox, QAbstractItemView, \
    QCalendarWidget, QMessageBox, QCheckBox
from PyQt5.QtGui import QColor
from StaticResources import TableData
class Regisration(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Регистрация нового пользователя")
        self.UI()
    def UI(self):
        self.ElementsCount = 1
        self.layout = QGridLayout()
        self.init_static()
        self.ComboBox = QComboBox()
        self.ComboBox.addItems(["ВК", "ОВУ в/ч", "ВВУЗ", "ГУК"])
        #self.ComboBox.currentIndexChanged.connect(self.changedComboBox())
        self.ComboBox.currentTextChanged.connect(self.changedComboBox)

        self.StaticElementsLabelsText = ["Фамилия", "Имя", "Отчество", "Должность", "Контакты", "Логин", "Пароль" ]
        self.setLayout(self.layout)
        self.layout.addWidget(QLabel("Организация"), 0, 0)
        self.layout.addWidget(self.ComboBox, 0, 1)

        self.createVK_UI()
        self.createStatic_UI()
        self.addButtons()
    def init_static(self):
        self.SurnameTextBox = QLineEdit()
        self.Name = QLineEdit()
        self.FatherName = QLineEdit()
        self.Post = QLineEdit()
        self.Contacts = QLineEdit()
        self.Login = QLineEdit()
        self.Password = QLineEdit()
        self.StaticElements = [self.SurnameTextBox, self.Name, self.FatherName, self.Post, self.Contacts, self.Login,
                               self.Password]
    def createStatic_UI(self):
        self.StaticLabels = []
        self.init_static()
        for i in range(len(self.StaticElementsLabelsText)):
            tmp = QLabel(self.StaticElementsLabelsText[i])
            self.StaticLabels.append(tmp)
            self.layout.addWidget(tmp, i+ self.ElementsCount, 0)
            self.layout.addWidget(self.StaticElements[i], i + self.ElementsCount, 1)
            self.layout.setRowMinimumHeight(i, 10)
    def addButtons(self):
        self.CancelButton = QPushButton()
        self.CancelButton.setText("Отмена")
        self.OKButton = QPushButton()
        self.OKButton.setText("Сохранить")
        self.OKButton.clicked.connect(self.Finish)
        self.layout.addWidget(self.CancelButton,self.ElementsCount + 7, 0)
        self.layout.addWidget(self.OKButton, self.ElementsCount + 7, 1)
    def getDynamicComboBoxLists(self):
        return ['Var1', 'Var2', 'Var3']
    def Finish(self):
        if self.checkForFilling():
            self.get_data()
            self.accept()
        else:
            msg_box = QMessageBox()
            msg_box.setText("Заполните все поля")
            retval = msg_box.exec_()
    def createVK_UI(self):
        self.OkrugComboBox = QComboBox()
        self.OkrugComboBox.addItems(self.getDynamicComboBoxLists())
        self.VKSubjectComboBox = QComboBox()
        self.VKSubjectComboBox.addItems(self.getDynamicComboBoxLists())
        self.MunVKComboBox = QComboBox()
        self.MunVKComboBox.addItems(self.getDynamicComboBoxLists())
        self.VKComboBoxes = [self.OkrugComboBox, self.VKSubjectComboBox, self.MunVKComboBox]
        strlst = ["Округ", "ВК субъекта", "Муниципальный ВК"]
        self.VKLabels = []
        for i in strlst:
            if i == "Муниципальный ВК":
                tmp = QCheckBox()
                tmp.setChecked(True)
                tmp.setText(i)
                self.VKLabels.append(tmp)
            else:
                self.VKLabels.append(QLabel(i))
        for i in range(len(strlst)):
            self.layout.addWidget(self.VKLabels[i], i +1, 0)
            self.layout.addWidget(self.VKComboBoxes[i], i+1, 1)
        #self.addButtons( self.StaticElementsCount + len(strlst))
        self.ElementsCount = 4
    def createOVU_UI(self):
        self.OkrugComboBox = QComboBox()
        self.VChComboBox = QComboBox()
        self.VChComboBox.setEditable(True)
        self.OkrugComboBox.addItems(self.getDynamicComboBoxLists())
        self.VChComboBox.addItems(self.getDynamicComboBoxLists())
        self.OVUComboBoxes= [self.OkrugComboBox, self.VChComboBox]
        strlst = ["ОВУ", "ВЧ"]
        self.OVULabels = []
        for i in strlst:
            if i == 'ВЧ':
                check = QCheckBox()
                check.setChecked(True)
                check.setText(i)
                self.OVULabels.append(check)
            else:
                self.OVULabels.append(QLabel(i))
        for i in range(len(strlst)):
            self.layout.addWidget(self.OVULabels[i], i+1,  0)
            self.layout.addWidget(self.OVUComboBoxes[i], i+1, 1)
        self.ElementsCount = 3
        #self.addButtons(self.StaticElementsCount + len(strlst))
    def createVVUZ_UI(self):
        self.VVUZComboBox = QComboBox()
        self.VVUZComboBox.addItems(self.getDynamicComboBoxLists())
        self.VVUZComboBoxes = [self.VVUZComboBox]
        strlst = ["ВУЗ"]
        self.VVUZLabels = []
        for i in strlst:
            self.VVUZLabels.append(QLabel(i))
        for i in range(len(strlst)):
            self.layout.addWidget(self.VVUZLabels[i], i+1, 0)
            self.layout.addWidget(self.VVUZComboBoxes[i], i+1, 1)
        self.ElementsCount = 2
        #self.addButtons(self.StaticElementsCount + len(strlst))
    def hide_all(self):
        try:
            self.OKButton.deleteLater()
            self.CancelButton.deleteLater()
        except:
            print('error')
        try:
            self.hide_VK()
        except:
            print('error')
        try:
            self.hide_OVU()
        except:
            print('error')
        try:
            self.hide_VVUZ()
        except:
            print('error')
        try:
            self.hide_static()
        except:
            print('error')
    def hide_VK(self):
        lst = [self.OkrugComboBox, self.VKSubjectComboBox, self.MunVKComboBox]
        self.tryToDelete(lst)
        self.tryToDelete(self.VKLabels)
    def hide_OVU(self):
        lst = [self.OkrugComboBox, self.VChComboBox]
        self.tryToDelete(lst)
        self.tryToDelete(self.OVULabels)
    def hide_VVUZ(self ):
        lst = [ self.VVUZComboBox]
        self.tryToDelete(lst)
        self.tryToDelete(self.VVUZLabels)
    def hide_static(self):
        self.tryToDelete(self.StaticElements)
        self.tryToDelete(self.StaticLabels)
    def tryToDelete(self, lst:list):
        for i in lst:
            try:
                i.deleteLater()
            except:
                print("not deleted")
    def changedComboBox(self, index):
        print(self.ComboBox.currentText())
        self.hide_all()
        if self.ComboBox.currentText() == "ВК":
            self.createVK_UI()
        elif self.ComboBox.currentText() == "ОВУ в/ч":
            self.createOVU_UI()
        elif self.ComboBox.currentText() == "ВВУЗ":
            self.createVVUZ_UI()
        elif self.ComboBox.currentText() == "ГУК":
            self.ElementsCount = 1
        self.createStatic_UI()
        self.addButtons()
    def checkForFilling(self):
        lst = []
        for i in range(len(self.StaticElements)):
            txt = ""
            if isinstance(self.StaticElements[i], QLineEdit):
                txt = self.StaticElements[i].text()
            elif isinstance(self.StaticElements[i], QComboBox):
                txt = self.StaticElements[i].currentText()
            if(txt == ""):
                return False
        return True
    def getVKData(self):
        return [self.OkrugComboBox.currentText(), self.VKSubjectComboBox.currentText(), self.VKLabels[2].isChecked(),self.MunVKComboBox.currentText()]
    def getOVUData(self):
        return [self.OkrugComboBox.currentText(), self.OVULabels[1].isChecked(), self.VChComboBox.currentText()]
    def getVVUZData(self):
        return [self.VVUZComboBox.currentText()]
    def getStaticData(self):
        return [self.Login.text(), self.Password.text(), self.SurnameTextBox.text(), self.Name.text(), self.FatherName.text(), self.Post.text(), self.Contacts.text()]
    def addList(self, list1:list, list2:list):
        for i in list2:
            list1.append(i)
        return list1
    def get_data(self):
        reslist = []
        if self.ComboBox.currentText() == "ВК":
            stat = self.getStaticData()
            dyn = self.getVKData()
            reslist.append("ВК")
            reslist = self.addList(reslist, stat)
            reslist = self.addList(reslist, dyn)
        elif self.ComboBox.currentText() == "ОВУ в/ч":
            stat = self.getStaticData()
            dyn = self.getOVUData()
            reslist.append("ВК")
            reslist = self.addList(reslist, stat)
            reslist = self.addList(reslist, dyn)
        elif self.ComboBox.currentText() == "ВВУЗ":
            stat = self.getStaticData()
            dyn = self.getVVUZData()
            reslist.append("ВК")
            reslist = self.addList(reslist, stat)
            reslist = self.addList(reslist, dyn)
        else:
            reslist.append("ГУК")
            reslist = self.addList(reslist, self.getStaticData())
        print(reslist)
        return reslist

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Regisration()
    window.setGeometry(200, 300, 500, 500)
    window.show()
    sys.exit(app.exec_())
