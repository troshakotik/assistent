from pathlib import Path
import pydub.playback
import yaml
import pydub
import random
import subprocess

import config
from utils import play_sound


class VoiceAssistant:
    def __init__(self):
        self.commands = self._parse_commands()
    
    def _fetch_command(self,phrase):
        phrase = phrase.lower()
        to_lower = lambda p: p.lower()

        for commands_list in self.commands:
            for cmd in commands_list["list"]:
                if phrase in map(to_lower,cmd["phrases"]):
                    cmd["command_path"] = commands_list["path"]
                    return cmd


    def react(self,phrase):
        cmd = self._fetch_command(phrase)

        if cmd is None:
            return False

        sound_name = random.choice(cmd["voice"]["sounds"])
        play_sound(sound_name)

        if cmd["command"]["action"] == "ahk":
            ahk_script_path = "{}\{}".format(cmd["command_path"],cmd["command"]["exe_path"])
            subprocess.run([config.AUTOHOTKEY_PATH, ahk_script_path])

        return True

    def _parse_commands(self):
        commands = []
        commands_path = Path(config.COMMANDS_PATH)

        for command_dir in commands_path.iterdir():
            for file in command_dir.iterdir():
                if file.name == config.COMMANDS_FILE_NAME:
                    data = yaml.safe_load(file.read_text(encoding="utf-8"))
                    data["path"] = str(command_dir)
                    commands.append(data)
        
        return commands