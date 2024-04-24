import sys
from PyQt6 import uic
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QMainWindow
import resources, interface

waiting = False
btn = None
match = {
    Qt.KeyboardModifier.ControlModifier: "Ctrl",
    Qt.KeyboardModifier.ShiftModifier: "Shift",
    Qt.KeyboardModifier.AltModifier: "Alt",
    Qt.KeyboardModifier.MetaModifier: "Meta",
    Qt.KeyboardModifier.NoModifier: "",
    Qt.KeyboardModifier.ControlModifier|Qt.KeyboardModifier.AltModifier: "Ctrl + Alt",
    Qt.KeyboardModifier.ShiftModifier|Qt.KeyboardModifier.AltModifier: "Shift + Alt",
    Qt.KeyboardModifier.ControlModifier|Qt.KeyboardModifier.ShiftModifier: "Ctrl + Shift",
    Qt.KeyboardModifier.AltModifier|Qt.KeyboardModifier.ShiftModifier: "Alt + Shift",
}


class ExampleApp(QMainWindow, interface.Ui_MainWindow):
    def __init__(self):
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле design.py
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.save_layout)
        self.pushButton_2.clicked.connect(self.load_layout)
        self.pushButton_3.clicked.connect(self.close)
        self.keypad_buttons = [self.pushButton_4, self.pushButton_5, self.pushButton_7, self.pushButton_8,
                   self.pushButton_9, self.pushButton_10, self.pushButton_11, self.pushButton_12,
                   self.pushButton_13, self.pushButton_14, self.pushButton_15, self.pushButton_16] 
        for keypad_button in self.keypad_buttons:
            keypad_button.setText("Не задано")
            keypad_button.clicked.connect(self.change_button) 

    def load_layout(self):
        with open("layout.txt", "r", encoding="utf-8") as f:
            for keypad_button in self.keypad_buttons:
                text = f.readline().split(":")[1]
                keypad_button.setText(text.rstrip())

    def save_layout(self):
        with open("layout.txt", "w", encoding="utf-8") as f:
            for keypad_button in self.keypad_buttons:
                text = keypad_button.objectName() + ":" + keypad_button.text() + "\n"
                f.write(text)                                          

    def change_button(self):
        global waiting
        global btn
        waiting = True

        btn = self.sender()
        btn.setText("Нажмите любую клавишу")

    def keyPressEvent(self, e):
        global waiting 
        global btn
        global match

        if waiting:
            super().keyPressEvent(e)
            mod_text = match[e.modifiers()]
            if e.text():
                if mod_text:
                    btn.setText(mod_text + " + " + str(e.text()))
                else:btn.setText(str(e.text()))
            else:
                btn.setText(mod_text)                      
            waiting = False

def main():
    app = QApplication(sys.argv)  # Новый экземпляр QApplication
    window = ExampleApp()  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    app.exec()  # и запускаем приложение

if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()