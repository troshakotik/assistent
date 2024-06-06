from PyQt6.QtCore import QObject, QThread, pyqtSignal
from wake_word import Recognizer, WakeWordListener
from voice_assistent import VoiceAssistant

from utils import play_wake_world_sound, play_end_of_user_phrase_sound


class VoiceRecognationTread(QThread):
    recognized_text_signal = pyqtSignal(dict)
    start_listen_signal = pyqtSignal()
    stop_listen_signal = pyqtSignal()

    def __init__(self) -> None:
        super().__init__()
        self.recognizer = Recognizer()
        self.wake_word_listener = WakeWordListener()
        self.voice_assistent = VoiceAssistant()

    def run(self) -> None:
        self.wake_word_listener.start()

        while True:
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