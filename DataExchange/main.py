import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QGridLayout
from PyQt5.QtWidgets import QLabel, QTabWidget, QPushButton
from PyQt5.QtWidgets import QSpacerItem, QSizePolicy
from PyQt5.QtWidgets import QMenu, QAction
from PyQt5.QtCore import Qt


class QMainWindowWithTabs(QMainWindow):
    def __init__(self):
        super().__init__()
        self.loaging_window = None
        self.update_window = None
        body = {
            "Файлы": None,
            "Карты": None,
            "Докобмен":{
                "Справочники": {
                        "Предложения": {
                                "ВУЗы": None,
                                "Категория": None,
                                "Выполнить": None
                            }
                        },
                "ГУК": {
                        "Выгрузка в ГУК" : {
                            "БД": None,
                            "Изменения":None,
                            "Данные": None,
                            "Выполнить": None
                            },
                        "Загрузка из ГУК" : None
                    },
                "ОВУ_вч": {
                        "Выгрузка в ОВУ_вч" : None,
                        "Загрузка из ОВУ_вч" : None
                    },
                "ВК": {
                        "Выгрузка в ВК" : None,
                        "Загрузка из ВК" : None
                    },
                "ВУЗы": {
                        "Выгрузка в ВУЗы" : None,
                        "Загрузка из ВУЗы" : None
                    },
                "Резерв1": None,
                "Резерв2": None,
                },
            "Администрирование": None,
            "Вид": None,
            "Отчёты": None,
            }
        # Создаем QTabWidget для вкладок
        self.tab_widget = QTabWidget()
        
        layout = QVBoxLayout()

        spacer = QSpacerItem(2000, 4000, QSizePolicy.Maximum, QSizePolicy.Maximum)

        layout.addWidget(self.tab_widget)
        layout.addItem(spacer)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.Tab_Files()
        self.Tab_Maps()
        self.Tab_DocExch()
        self.Tab_Administration()
        '''
        # Размещаем QTabWidget в основном окне
        for key1 in body:
            # Создаем виджеты для каждой вкладки
            tab1_widget = QTabWidget()
            self.tab_widget.addTab(tab1_widget, key1)
            # Первый уровень вложенности
            body2 = body[key1]
            if body2 is not None:
                for key2 in body2:
                    # Создаем QWidget для вкладок
                    tab2_widget = QWidget()
                    tab1_widget.addTab(tab2_widget, key2)
                    layout1 = QHBoxLayout(tab2_widget)
                    tab2_widget.setMinimumHeight(50)
                    tab2_widget.setMaximumHeight(50)
                    body3 = body2[key2]
                    if body3 is not None:
                        for key3 in body3:
                            button = QPushButton(key3)
                            button.clicked.connect(self.action(key3, body3[key3]))
                            layout1.addWidget(button)
                            '''   
    def Tab_Files(self):
        FilesTab = QTabWidget()
        self.tab_widget.addTab(FilesTab, "Файлы")
        
    def Tab_Maps(self):
        MapsTab = QTabWidget()
        self.tab_widget.addTab(MapsTab, "Карты")
        
    def Tab_DocExch(self):
        DocExchTab = QTabWidget()
        self.tab_widget.addTab(DocExchTab, "Докобмен")

        GuideTab = QWidget()
        DocExchTab.addTab(GuideTab, "Справочники")

        layout1 = QHBoxLayout(GuideTab)
        GuideTab.setMinimumHeight(50)
        GuideTab.setMaximumHeight(50)
        
        button = QPushButton("Загрузка")
        layout1.addWidget(button)
        button.clicked.connect(lambda: Loading(self).show())

        button = QPushButton("Обновление")
        layout1.addWidget(button)
        button.clicked.connect(lambda: Update(self).show())
        
        button = QPushButton("Предложения")
        layout1.addWidget(button)
        button.clicked.connect(lambda: Loading(self).show())
        
    def Tab_Administration(self):
        AdministrationTab = QTabWidget()
        self.tab_widget.addTab(AdministrationTab, "Администрирование")


class Loading(QMainWindow):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.setGeometry(200, 300, 200, 100)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowMinMaxButtonsHint)
        
        layout = QVBoxLayout()
        layout1 = QVBoxLayout()
        layout2 = QHBoxLayout()
        layout.addLayout(layout1)
        layout.addLayout(layout2)

        path_button = QPushButton("Путь к файлу")
        layout1.addWidget(path_button)
        path_button.clicked.connect(lambda: None)

        execute_button = QPushButton("Выполнить")
        layout2.addWidget(execute_button)
        execute_button.setStyleSheet("background-color: #80FF80;")#Зелёный
        execute_button.clicked.connect(lambda: None)
        
        cancel_button = QPushButton("Отмена")
        layout2.addWidget(cancel_button)
        cancel_button.setStyleSheet("background-color: #FF8080;")#Красный
        cancel_button.clicked.connect(lambda: None)
        
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

class Update(QMainWindow):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.setGeometry(200, 300, 200, 100)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowMinMaxButtonsHint)
        
        layout = QVBoxLayout()
        layout1 = QVBoxLayout()
        layout2 = QHBoxLayout()
        layout.addLayout(layout1)
        layout.addLayout(layout2)

        path_button = QPushButton("Путь к файлу")
        layout1.addWidget(path_button)
        path_button.clicked.connect(lambda: None)

        execute_button = QPushButton("Выполнить")
        layout2.addWidget(execute_button)
        execute_button.setStyleSheet("background-color: #80FF80;")#Зелёный
        execute_button.clicked.connect(lambda: None)
        
        cancel_button = QPushButton("Отмена")
        layout2.addWidget(cancel_button)
        cancel_button.setStyleSheet("background-color: #FF8080;")#Красный
        cancel_button.clicked.connect(lambda: None)
        
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
'''
class LittleWindow(QMainWindow):
    def __init__(self, name, body, parent = None):
        super().__init__(parent)
        self.setWindowTitle(name)
        self.setGeometry(200, 300, 300, 300)
        
        if body is not None:
            for key in body:
                button = QPushButton(key)
                button.clicked.connect(self.action(key))
                layout.addWidget(button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
    def goBack(self):
        #self.parent().show()
        self.hide()
    def action(self, name):
        title = name
        if title == "Отмена":
            return self.goBack
        def f():
            return 0
        return f
'''


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = QMainWindowWithTabs()
    window.setGeometry(200, 300, 600, 500)
    window.show()
    sys.exit(app.exec_())
