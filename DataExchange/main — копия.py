import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QMenu

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Обычное меню с подменю")

        # Создаем меню "Файл"
        file_menu = self.menuBar().addMenu("Файл")

        # Создаем действие "Новый"
        new_action = QAction("Новый", self)
        file_menu.addAction(new_action)

        # Создаем подменю для действия "Новый"
        new_submenu = QMenu()
        new_action.setMenu(new_submenu)

        # Добавляем действия в подменю
        html_action = QAction("HTML", self)
        pdf_action = QAction("PDF", self)
        new_submenu.addAction(html_action)
        new_submenu.addAction(pdf_action)

        # Соединяем сигналы со слотами
        html_action.triggered.connect(lambda: self.create_new_file("HTML"))
        pdf_action.triggered.connect(lambda: self.create_new_file("PDF"))

    def create_new_file(self, file_format):
        print("Создан новый файл в формате", file_format)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
