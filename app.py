from PyQt6.QtCore import QSize
from PyQt6.QtGui import QCloseEvent
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget, QFrame, QBoxLayout


from wake_word import WakeWordListener, Recognizer
from commands import COMMAND_DICT

import sys
import asyncio




class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.wake_world_listener = WakeWordListener()
        self.recognizer = Recognizer()

        self.frame_main = QFrame()
        self.layout_top = QBoxLayout()
        self.layout_top.setParent(self.frame_main)
        self.frame_main.setLayout(self.layout_top)
        self.setCentralWidget(self.frame_main)

        self.setWindowTitle("Lolly")
        self.setFixedSize(QSize(400,400))

        button1 = QPushButton("Прослушать")
        button1.clicked.connect(self.button_click)
        button1.setFixedSize(QSize(50,50))

        button2 = QPushButton("Нажми")
        button2.clicked.connect(lambda : print("Нажали"))
        button2.setFixedSize(QSize(50,50))


    def closeEvent(self, a0: QCloseEvent) -> None:
        self.wake_world_listener.stop_listen_process()
        super().closeEvent(a0)
    
    def button_click(self):
        # asyncio.ensure_future(self.listen_user_command_and_execute())
        print("Нажали на первую кнопку")


    
    async def listen_user_command_and_execute(self):
        self.wake_world_listener.start()

        while True:
            if self.wake_world_listener.is_wake_world():
                print("Слушаю вас!")
                try:
                    user_query = self.recognizer.recognize_speech()
                    print(user_query)
                except Recognizer.UnknownValueError:
                    print("Не распознал")

                command = COMMAND_DICT.get(user_query)
                if command is not None:
                    command(self)





if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()