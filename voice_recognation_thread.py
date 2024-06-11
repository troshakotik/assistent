from PyQt6.QtCore import QObject, QThread, pyqtSignal
from wake_word import Recognizer, WakeWordListener

from utils import play_wake_world_sound, play_end_of_user_phrase_sound


class VoiceRecognationTread(QThread):
    recognized_text_signal = pyqtSignal(dict)
    start_listen_signal = pyqtSignal()
    stop_listen_signal = pyqtSignal()
    recognizer = Recognizer()
    wake_word_listener = WakeWordListener()
    is_stop = False

    def __init__(self,voice_assistent) -> None:
        super().__init__()
        self.voice_assistent = voice_assistent
    
    def quit(self) -> None:
        self.is_stop = True
        super().quit()
    
    def start(self):
        self.is_stop = False
        super().start()

    def run(self) -> None:
        self.wake_word_listener.start()

        while not self.is_stop:
            if self.wake_word_listener.is_wake_world():
                self.start_listen_signal.emit()
                play_wake_world_sound()

                try:
                    user_phrase = self.recognizer.recognize_speech()
                except Recognizer.UnknownValueError:
                    play_end_of_user_phrase_sound()
                    self.stop_listen_signal.emit()
                    self.recognized_text_signal.emit({"is_recognitioned":False})
                    continue

                play_end_of_user_phrase_sound()
                self.stop_listen_signal.emit()

                self.voice_assistent.react(user_phrase)
                self.recognized_text_signal.emit({"is_recognitioned" : True,"text":user_phrase})