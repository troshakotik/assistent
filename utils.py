import pydub
import pydub.playback
from threading import Thread
import yaml
from pathlib import Path

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

def beatiful_string(string:str):
    return " ".join([s.capitalize() for s in string.split(" ")])

def add_command(**kwargs):
    new_command = {
        "command" : {
            "name" : kwargs["name"],
            "action" : "ahk",
            "exe_path" : kwargs["exe_path"],
            "exe_args" : kwargs["exe_args"]
        },
        "voice" : {"sounds" : ["hello"]},
        "phrases" : kwargs["phrases"]
    }
    with open(kwargs["command_path"],"r",encoding="utf-8") as command_yaml_file:
        command_list = yaml.safe_load(command_yaml_file)
        command_list["list"].append(new_command)

    with open(kwargs["command_path"],"w",encoding="utf-8") as command_yaml_file:
        yaml.dump(command_list,command_yaml_file,allow_unicode=True)