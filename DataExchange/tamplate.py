import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QGridLayout
from PyQt5.QtWidgets import QLabel, QTabWidget, QPushButton
from PyQt5.QtWidgets import QSpacerItem, QSizePolicy
from PyQt5.QtWidgets import QMenu, QAction

class QMainWindowWithTabs(QMainWindow):
    def __init__(self):
        super().__init__()
        self.LittleSon = None
        body = {
            "Файлы": None,
            "Карты": None,
            "Докобмен":{
                "Справочники": {
                        "Загрузка": None,
                        "Обновление": {
                                "Путь к файлу": None,
                                "Выполнить": None,
                                "Отмена": None
                            },
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
        # Размещаем QTabWidget в основном окне
        #self.setCentralWidget(self.tab_widget)
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
        layout = QVBoxLayout()
        spacer = QSpacerItem(2000, 4000, QSizePolicy.Maximum, QSizePolicy.Maximum)
        layout.addWidget(self.tab_widget)
        layout.addItem(spacer)
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
        
    def action(self, name, body):
        def f():
            if self.LittleSon is not None:
                self.LittleSon.deleteLater()
            self.LittleSon = LittleWindow(name, body, self)
            self.LittleSon.show()
            #self.hide()
            return
        return f

class LittleWindow(QMainWindow):
    def __init__(self, name, body, parent = None):
        super().__init__(parent)
        self.setWindowTitle(name)
        self.setGeometry(200, 300, 300, 300)
        
        layout = QVBoxLayout()
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

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = QMainWindowWithTabs()
    window.setGeometry(200, 300, 600, 500)
    window.show()
    sys.exit(app.exec_())
