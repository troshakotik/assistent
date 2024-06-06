from PyQt6.QtCore import QSize
from PyQt6.QtGui import QCloseEvent
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel


import sys
from voice_recognation_thread import VoiceRecognationTread



class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.init_ui()
        self.init_voice_thread()

    def init_ui(self):
        self.setWindowTitle("Lolly")
        self.setFixedSize(QSize(400,400))
        self.label = QLabel()
        self.setCentralWidget(self.label)
        self.label.setText("Готов слушать")

    def init_voice_thread(self):
        self.voice_thread = VoiceRecognationTread()
        self.voice_thread.recognized_text_signal.connect(self.after_recognition_phrase)
        self.voice_thread.start_listen_signal.connect(self.start_listen_process)
        self.voice_thread.stop_listen_signal.connect(self.stop_listen_process)
    
    def closeEvent(self, a0: QCloseEvent) -> None:
        self.voice_thread
        super().closeEvent(a0)
    
    def start_listen_process(self):
        self.setStyleSheet("background-color: red;")
    
    def stop_listen_process(self):
        self.setStyleSheet("background-color: white;")
    
    def after_recognition_phrase(self,result):
        if result["is_recognitioned"]:
            self.label.setText(result["text"])
        else:
            self.label.setText("Не распознал")



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()