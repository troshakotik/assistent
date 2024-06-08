from PyQt6.QtCore import QSize
from PyQt6.QtGui import QCloseEvent
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QListWidget, QListWidgetItem


import sys
from voice_recognation_thread import VoiceRecognationTread
from voice_assistent import VoiceAssistant


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.init_ui()
        self.init_voice_thread()
        self.command_window = None

    def init_ui(self):
        self.setWindowTitle("Lolly")
        self.setFixedSize(QSize(400,400))

        layout = QHBoxLayout()

        self.label = QLabel()
        self.label.setText("Готов слушать")

        self.show_command_button = QPushButton("список комманд")
        self.show_command_button.clicked.connect(self.show_command_button_on_click)

        layout.addWidget(self.label)
        layout.addWidget(self.show_command_button)

        central_widget = QWidget()
        central_widget.setLayout(layout)

        self.setCentralWidget(central_widget)

    
    def show_command_button_on_click(self):
        self.command_window = CommandWindow(self.voice_assistant.commands)
        self.command_window.show()

    def init_voice_thread(self):
        self.voice_assistant = VoiceAssistant()
        self.voice_thread = VoiceRecognationTread(self.voice_assistant)
        self.voice_thread.recognized_text_signal.connect(self.after_recognition_phrase)
        self.voice_thread.start_listen_signal.connect(self.start_listen_process)
        self.voice_thread.stop_listen_signal.connect(self.stop_listen_process)

    
    def start_listen_process(self):
        self.setStyleSheet("background-color: red;")
    
    def stop_listen_process(self):
        self.setStyleSheet("background-color: white;")
    
    def after_recognition_phrase(self,result):
        if result["is_recognitioned"]:
            self.label.setText(result["text"])
        else:
            self.label.setText("Не распознал")


class CommandItem(QWidget):
    def __init__(self,command):
        super().__init__()

        self.phrases_label = QLabel()
        phrases = ",\n".join(command["phrases"])
        self.phrases_label.setText(f"Фразы: {phrases}")

        layout = QHBoxLayout()
        layout.addWidget(self.phrases_label)
        self.setLayout(layout)


class CommandWindow(QWidget):
    def __init__(self,commands):
        super().__init__()
        self.init_ui(commands)

    def init_ui(self,commands):
        self.setWindowTitle("Список доступных комманд")
        self.setGeometry(100,100,200,300)

        layout = QVBoxLayout()
        self.list_widget = QListWidget(self)

        for command in commands:
            item = QListWidgetItem(self.list_widget)
            command_item = CommandItem(command)
            item.setSizeHint(command_item.sizeHint())

            self.list_widget.addItem(item)
            self.list_widget.setItemWidget(item,command_item)
        
        layout.addWidget(self.list_widget)
        self.setLayout(layout)





if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()