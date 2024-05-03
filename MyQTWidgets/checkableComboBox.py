import qtconsole.completion_html
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys


class CheckableComboBox(QComboBox):

    # constructor
    def __init__(self, parent=None):
        super(CheckableComboBox, self).__init__(parent)
        self.view().pressed.connect(self.handleItemPressed)
        self.setModel(QStandardItemModel(self))
        self.Count = 0
        self.SelectedValuesList = []
        self.BaseList = []
        self.NoLimitation = True

    # action called when item get checked
    def do_action(self):
        return 0

    # when any item get pressed
    def setObjectList(self, list:list):
        self.addItems(list)
        for i in range(len(list)):
            self.model().item(i).setCheckState(Qt.Checked)
        self.Count = len(list)
        self.SelectedValuesList = list.copy()
        self.BaseList = list.copy()
        self.NoLimitation = True
    def updateSelectedValueList(self):
        self.SelectedValuesList.clear()
        for i in range(self.Count):
            if self.model().item(i).checkState() == Qt.Checked:
                self.SelectedValuesList.append(self.BaseList[i])
        self.NoLimitation = len(self.SelectedValuesList) == self.Count

    def handleItemPressed(self, index):

        # getting the item
        item = self.model().itemFromIndex(index)

        # checking if item is checked
        if item.checkState() == Qt.Checked:

            # making it unchecked
            item.setCheckState(Qt.Unchecked)


        # if not checked
        else:
            # making the item checked
            item.setCheckState(Qt.Checked)
        self.updateSelectedValueList()