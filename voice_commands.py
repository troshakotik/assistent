from pathlib import Path
import yaml
import subprocess

import config

class VoiceCommand:
    def __init__(self,name,action,sounds,group,cli_cmd,cli_args,exe_path,exe_args,is_user_command):
        self.exe_path = exe_path
        self.name = name
        self.group = group
        self.action = action
        self.cli_cmd = cli_cmd
        self.cli_args = cli_args
        self.exe_args = exe_args
        self.sounds = sounds
        self.is_user_command = is_user_command

        self.execute = {"ahk":self.do_ahk_script,"cli":self.do_cmd_script,"terminate":self.terminate,"voice":lambda:None}[action]
        self.full_path = "{}\{}\{}".format(config.COMMANDS_PATH,self.group,config.COMMANDS_FILE_NAME)
    

    def do_ahk_script(self):
        ahk_script_path = "{}\{}\{}".format(config.COMMANDS_PATH,self.group,self.exe_path)
        to_subprocess = [config.AUTOHOTKEY_PATH, ahk_script_path]

        if exe_args := self.exe_args:
            to_subprocess.extend(map(str,exe_args))

        subprocess.run(to_subprocess)
    
    def do_cmd_script(self):
        to_subprocess = [self.cli_cmd]
        if self.cli_args:
            to_subprocess.extend(self.cli_args)
        
        subprocess.run(to_subprocess)
    
    def terminate(self):
        exit()
    
    def __eq__(self,other):
        if not isinstance(other,type(self)):
            return False
        
        return other.name == self.name



class CommandPhraseExists(Exception):
    def __init__(self,phrase):
        self.phrase = phrase

class CommandNameExists(Exception):
    def __init__(self,name):
        self.name = name

class VoiceCommandsStorage:
    _commands_dict = {}
    CommandPhraseExists = CommandPhraseExists
    CommandNameExists = CommandNameExists               

    def __init__(self):
        commands_path = Path(config.COMMANDS_PATH)

        for command_group in commands_path.iterdir():
            for file in command_group.iterdir():
                if file.name == config.COMMANDS_FILE_NAME:
                    commands_yaml = yaml.safe_load(file.read_text(encoding="utf-8"))["list"]

                    for cmd in commands_yaml:
                        phrases_key = tuple(map(lambda s:s.lower(),cmd["phrases"]))
                        self._commands_dict[phrases_key] = (
                            VoiceCommand(
                                name=cmd["command"]["name"],
                                action=cmd["command"]["action"],
                                sounds=cmd["voice"]["sounds"],
                                group=command_group.stem,
                                cli_cmd=cmd["command"].get("cli_cmd"),
                                cli_args=cmd["command"].get("cli_args"),
                                exe_path=cmd["command"].get("exe_path"),
                                exe_args=cmd["command"].get("exe_args"),
                                is_user_command=cmd["command"].get("is_user_command")
                            )
                        )


    def get_command(self,phrase) -> VoiceCommand:
        phrase = phrase.lower()
        for phrases, command in self._commands_dict.items():
            if phrase in phrases:
                return command


    def create_new_command(self,new_command:VoiceCommand,phrases):
        for command_phrases, command in self._commands_dict.items():
            if command.name == new_command.name:
                raise self.CommandNameExists(command.name)

            for phrase in phrases:
                if phrase in command_phrases:
                    raise self.CommandPhraseExists(phrase)

        self._add_command_to_yaml(new_command,phrases)
        self._commands_dict[tuple(phrases)] = new_command


    def delete_command(self,deleted_command:VoiceCommand):
        for phrases, command in self._commands_dict.items():
            if command.name == deleted_command.name:
                self._commands_dict.pop(phrases)
                break

        self._delete_from_yaml(deleted_command)

    def _delete_from_yaml(self,deleted_command:VoiceCommand):
        with open(deleted_command.full_path,"r",encoding="utf-8") as command_yaml_file:
            command_list = yaml.safe_load(command_yaml_file)

            for i, command in enumerate(command_list["list"]):
                if command["command"]["name"] == deleted_command.name:
                    command_list["list"].pop(i)
        
        with open(deleted_command.full_path,"w",encoding="utf-8") as command_yaml_file:
            yaml.dump(command_list,command_yaml_file,allow_unicode=True)


    def _add_command_to_yaml(self,command:VoiceCommand,phrases):
        command_dict = {
            "name":command.name,
            "action":command.action,
            "is_user_command":command.is_user_command
        }

        if command.action == "ahk":
            command_dict["exe_path"] = command.exe_path
            command_dict["exe_args"] = command.exe_args

        elif command.action == "cmd":
            command_dict["cli_cmd"] = command.cli_cmd
            command_dict["cli_args"] = command.cli_args
        
        new_command = {
            "command" : command_dict,
            "voice" : {"sounds":command.sounds},
            "phrases" : phrases
        }

        with open(command.full_path,"r",encoding="utf-8") as command_yaml_file:
            command_list = yaml.safe_load(command_yaml_file)
            command_list["list"].append(new_command)
        
        with open(command.full_path,"w",encoding="utf-8") as command_yaml_file:
            yaml.dump(command_list,command_yaml_file,allow_unicode=True)

    def __iter__(self):
        yield from self._commands_dict.items()