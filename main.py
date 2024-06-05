from speech_recognition import Recognizer, Microphone, UnknownValueError

sr = Recognizer()
sr.pause_threshold = 0.5



def recognize_speech():
    try:
        with Microphone() as mic:
            sr.adjust_for_ambient_noise(source=mic,duration=1)
            audio = sr.listen(source=mic)
            query = sr.recognize_google(audio_data=audio,language='ru-RU').lower()

    except Exception as e:
        raise e
    
    return query
