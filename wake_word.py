import pvporcupine
from pvrecorder import PvRecorder
from speech_recognition import Recognizer as SpeechRecognizer, Microphone, UnknownValueError



ACCESS_KEY = "9ikPPkZ0kX3/bRJwMcsaRM/sZTk20JziKldZJekb1b02kyjSHPR66g=="
KEYWORD_PATH = "./wake-up-model/Listen-me_en_windows_v3_0_0.ppn"



class WakeWordListener:
    def __init__(self):
        self.porcupine = pvporcupine.create(access_key=ACCESS_KEY, keyword_paths=[KEYWORD_PATH])
        self.recoder = PvRecorder(device_index=-1, frame_length=self.porcupine.frame_length)
    
    def start(self):
        self.recoder.start()

    def is_wake_world(self):
        keyword_index = self.porcupine.process(self.recoder.read())
        return keyword_index >= 0

    def stop_listen_process(self):
        self.porcupine.delete()
        self.recoder.delete()


class Recognizer:
    UnknownValueError = UnknownValueError

    def __init__(self):
        self.sr = SpeechRecognizer()
        self.sr.pause_threshold = 0.5
    
    def recognize_speech(self):
        with Microphone() as mic:
            self.sr.adjust_for_ambient_noise(source=mic,duration=1)
            audio = self.sr.listen(source=mic)
            query = self.sr.recognize_google(audio_data=audio,language='ru-RU').lower()

        return query