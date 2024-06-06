import pydub
import pydub.playback
from threading import Thread

from config import SOUNDS_PATH, WAKE_WORLD_SOUND_NAME, END_OF_USER_PHRASE_SOUND_NAME


def _play_sound(sound_name):
    audio = pydub.AudioSegment.from_file("{}/{}.mp3".format(SOUNDS_PATH,sound_name))
    pydub.playback.play(audio)

def play_sound(sound_name):
    Thread(target=_play_sound,args=(sound_name,)).run()

def play_wake_world_sound():
    play_sound(WAKE_WORLD_SOUND_NAME)

def play_end_of_user_phrase_sound():
    play_sound(END_OF_USER_PHRASE_SOUND_NAME)