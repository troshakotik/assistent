from pathlib import Path
import yaml
import random
import subprocess

import config
from utils import play_sound
from giga_chat_api import GigaChat



class VoiceAssistant:
    def __init__(self):
        self.commands = self._parse_commands()
        self.giga_chat = GigaChat()
    
    def _fetch_command(self,phrase):
        phrase = phrase.lower()
        to_lower = lambda p: p.lower()

        for cmd in self.commands:
            if phrase in map(to_lower,cmd["phrases"]):
                return cmd
    
    def do_ahk_script_command(self,command):
        ahk_script_path = "{}\{}".format(command["command_path"],command["command"]["exe_path"])
        to_subprocess = [config.AUTOHOTKEY_PATH, ahk_script_path]

        if exe_args := command["command"].get("exe_args"):
            to_subprocess.extend(map(str,exe_args))

        subprocess.run(to_subprocess)
    
    def do_cmd_command(self,command):
        to_subprocess = [command["command"]["cli_cmd"]]
        if cli_args := command["command"].get("cli_args"):
            to_subprocess.extend(cli_args)
        
        subprocess.run(to_subprocess)


    def voice_over_phrase(self,phrase):
        print(f"Todo, phrase : {phrase}")

    def react(self,phrase):
        cmd = self._fetch_command(phrase)

        if cmd is None:
            return False

        sound_name = random.choice(cmd["voice"]["sounds"])
        play_sound(sound_name)

        if cmd["command"]["action"] == "ahk":
            self.do_ahk_script_command(cmd)
        elif cmd["command"]["action"] == "cli":
            self.do_cmd_command(cmd)
        elif cmd["command"]["action"] == "terminate":
            exit()

        return True

    def _parse_commands(self):
        commands = []
        commands_path = Path(config.COMMANDS_PATH)

        for command_dir in commands_path.iterdir():
            for file in command_dir.iterdir():
                if file.name == config.COMMANDS_FILE_NAME:
                    commands_list = yaml.safe_load(file.read_text(encoding="utf-8"))["list"]

                    for cmd in commands_list:
                        cmd["command_path"] = str(command_dir)
                        commands.append(cmd)

        return commands