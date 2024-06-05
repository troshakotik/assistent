import yaml
from pathlib import Path
from pydub import AudioSegment 
from pydub.playback import play

from random import choice
import subprocess

import playsound

from config import COMMANDS_PATH, COMMANDS_FILE_NAME, SOUNDS_PATH, AUTOHOTKEY_PATH


def play_audio(sound):
    audio = AudioSegment.from_file("{}/{}.mp3".format(SOUNDS_PATH,sound))
    play(audio)
    


def parse_commands():
    commands_path = Path(COMMANDS_PATH)

    for command_dir in commands_path.iterdir():
        for file in command_dir.iterdir():
            if file.name == COMMANDS_FILE_NAME:
                data = yaml.safe_load(file.read_text(encoding="utf-8"))
                data["path"] = str(command_dir)
                yield data

def fetch_command(phrase):
    phrase = phrase.lower()
    to_lower = lambda p: p.lower()

    for commands_list in parse_commands():
        for cmd in commands_list["list"]:
            if phrase in map(to_lower,cmd["phrases"]):
                cmd["command_path"] = commands_list["path"]
                return cmd


def execute_command(phrase):
    cmd = fetch_command(phrase)

    if cmd is None:
        return

    sound = choice(cmd["voice"]["sounds"])
    
    if cmd["command"]["action"] == "ahk":
        ahk_script_path = "{}\{}".format(cmd["command_path"],cmd["command"]["exe_path"])
        subprocess.run([AUTOHOTKEY_PATH, ahk_script_path])
    
    play_audio(sound)





print(execute_command("отключи игровой режим"))