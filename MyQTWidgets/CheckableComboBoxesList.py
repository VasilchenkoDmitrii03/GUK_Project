import sys

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from PyQt5 import QtGui
import MyQTWidgets.checkableComboBox


class MyWidget(QtWidgets.QWidget):

    def __init__(self, itemsList):
        super().__init__()
        self.grid = QGridLayout()
        self.setLayout(self.grid)
        self.BaseList = []
        self.TotalDict = dict()
    def createComboBoxes(self, dct:dict):
        self.comboBoxesList = []
        lst = list(dct.keys())
        for i in range(len(lst)):
            tmp = MyQTWidgets.checkableComboBox.CheckableComboBox(self)
            a = dct[lst[i]]
            tmp.setObjectList(a)
            lab = QLabel(self)
            lab.setText(lst[i])
            self.comboBoxesList.append(tmp)
            self.grid.addWidget(lab, 0, i)
            self.grid.addWidget(tmp, 1, i)
        self.setLayout(self.grid)
        self.BaseList = lst.copy()

    def getChosenValues(self):
        self.TotalDict = dict()
        for i in range(len(self.BaseList)):
            self.comboBoxesList[i].updateSelectedValueList()
            if not(self.comboBoxesList[i].NoLimitation):
                self.TotalDict[self.BaseList[i]] = self.comboBoxesList[i].SelectedValuesList



