from PyQt6.QtCore import QThread, pyqtSignal
import random

import pvporcupine
from pvrecorder import PvRecorder

from utils import play_wake_world_sound, play_end_of_user_phrase_sound, play_sound
from voice_commands import VoiceCommandsStorage
import config

from speech_recognition import Recognizer,Microphone, UnknownValueError



class VoiceRecognitionProcess:
    _is_stop = False

    def __init__(
            self,
            voice_commands:VoiceCommandsStorage,
            start_listen_signal:pyqtSignal,
            stop_listen_signal:pyqtSignal,
            recognized_text_signal:pyqtSignal
        ):

        self.porcupine = pvporcupine.create(
            access_key=config.PORCUPINE_ACCESS_KEY, 
            keyword_paths=[config.PORCUPINE_KEYWORD_PATH]
        )
        self.recorder = PvRecorder(device_index=-1,frame_length=self.porcupine.frame_length)
        self.recognizer = Recognizer()
        self.recognizer.pause_threshold = 0.5

        self.start_listen_signal = start_listen_signal
        self.stop_listen_signal = stop_listen_signal
        self.recognized_text_signal = recognized_text_signal
        self.voice_commands = voice_commands

    def recognize_phrase(self):
        with Microphone() as mic:
            self.recognizer.adjust_for_ambient_noise(source=mic,duration=1)
            play_wake_world_sound()
            audio = self.recognizer.listen(source=mic)
            query = self.recognizer.recognize_google(audio_data=audio,language='ru-RU').lower()
        
        return query

        
    def stop(self):
        self._is_stop = True
    
    def run_loop(self):
        self._is_stop = False
        self.recorder.start()

        while not self._is_stop:
            kwrd_index = self.porcupine.process(self.recorder.read())
            if not kwrd_index >= 0:
                continue

            try:
                user_phrase = self.recognize_phrase()
            except UnknownValueError:
                play_end_of_user_phrase_sound()
                self.stop_listen_signal.emit()
                self.recognized_text_signal.emit({"is_recognitioned":False})
                continue

            play_end_of_user_phrase_sound()
            self.stop_listen_signal.emit()

            self.recognized_text_signal.emit({"is_recognitioned" : True,"text":user_phrase})
            command = self.voice_commands.get_command(user_phrase)

            if command is not None:
                sound_name = random.choice(command.sounds)
                play_sound(sound_name)
                command.execute()
        
        self.porcupine.delete()
        self.recorder.delete()


class VoiceRecognationTread(QThread):
    recognized_text_signal = pyqtSignal(dict)
    start_listen_signal = pyqtSignal()
    stop_listen_signal = pyqtSignal()
    
    def __init__(self,voice_commands:VoiceCommandsStorage):
        super().__init__()
        self.voice_commands = voice_commands
        self.voice_recognition_process = (
            VoiceRecognitionProcess(
                self.voice_commands,
                self.start_listen_signal,
                self.stop_listen_signal,
                self.recognized_text_signal
            )
        )

    def quit(self) -> None:
        self.voice_recognition_process.stop()
        super().quit()

    def run(self):
        self.voice_recognition_process.run_loop()