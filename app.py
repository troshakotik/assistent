from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import (
    QApplication, 
    QMainWindow,
    QLabel,
    QWidget,
    QPushButton,
    QHBoxLayout,
    QVBoxLayout,
    QListWidget,
    QListWidgetItem,
    QLineEdit,
    QMessageBox,
    QLayout
)


import sys
from voice_recognation_thread import VoiceRecognationTread
from voice_commands import VoiceCommandsStorage,VoiceCommand
from utils import beatiful_string, RUSSIAN_LOW_LETTERS


class MainWidget(QWidget):
    def __init__(self,show_command_button_click,stop_listen_button_click):
        super().__init__()
        self.show_command_button_click = show_command_button_click
        self.stop_listen_button_click = stop_listen_button_click
        self.init_ui()

    def init_ui(self):
        layout = QHBoxLayout()

        self.label = QLabel()
        self.label.setText("Готов слушать")

        self.show_command_button = QPushButton("список комманд")
        self.show_command_button.clicked.connect(self.show_command_button_click)

        self.stop_listen_button = QPushButton("Перестать слушать")
        self.stop_listen_button.clicked.connect(self.stop_listen_button_click)

        layout.addWidget(self.label)
        layout.addWidget(self.show_command_button)
        layout.addWidget(self.stop_listen_button)

        self.setLayout(layout)


class MainWindow(QMainWindow):
    voice_commands = VoiceCommandsStorage()


    def __init__(self) -> None:
        super().__init__()
        self.init_ui()
        self.init_voice_thread()

    def init_ui(self):
        self.setWindowTitle("Lolly")
        self.setFixedSize(QSize(450,450))
        self.setMainCentralWidget()
    
    def setMainCentralWidget(self):
        central_widget = MainWidget(self.show_command_button_click,self.stop_listen_button_click)
        self.setCentralWidget(central_widget)


    def show_command_button_click(self):
        # self.command_window = CommandWindow(self.voice_commands)
        # self.command_window.show()
        self.setCentralWidget(CommandWindow(self.voice_commands,self))
    
    def stop_listen_button_click(self):
        if self.voice_thread.isFinished():
            self.voice_thread.start()
        else:
            self.voice_thread.quit()
            self.voice_thread.wait()


    def init_voice_thread(self):
        self.voice_thread = VoiceRecognationTread(self.voice_commands)
        self.voice_thread.start()
    
        self.voice_thread.recognized_text_signal.connect(self.after_recognition_phrase)
        self.voice_thread.start_listen_signal.connect(self.start_listen_process)
        self.voice_thread.stop_listen_signal.connect(self.stop_listen_process)

        self.voice_thread.finished.connect(self.voice_thread_finished)
        self.voice_thread.started.connect(self.voice_thread_started)

    
    def start_listen_process(self):
        self.setStyleSheet("background-color: red;")
    
    def stop_listen_process(self):
        self.setStyleSheet("background-color: white;")

    def voice_thread_finished(self):
        print("voice thread is finished")
    
    def voice_thread_started(self):
        print("voice thread is starting")
    
    def after_recognition_phrase(self,result):
        if result["is_recognitioned"]:
            pass
            # main_widget = MainWidget(self.show_command_button_click,self.stop_listen_button_click)
            # main_widget.label.setText(result["text"])
            # self.setCentralWidget(main_widget)
        else:
            pass
            # self.label.setText("Не распознал")


class CommandItem(QWidget):
    def __init__(self,phrases,command:VoiceCommand,voice_commands:VoiceCommandsStorage):
        super().__init__()

        layout = QHBoxLayout()

        self.phrases_label = QLabel()
        phrases = ",\n".join(phrases)
        self.phrases_label.setText(f"Фразы:\n {phrases}")

        self.name_label = QLabel()
        name = beatiful_string(command.name)
        self.name_label.setText(name)

        if command.is_user_command:
            self.delete_button = QPushButton("Удалить")
            self.delete_button.clicked.connect(self.delete_button_on_click(command,voice_commands))
            layout.addWidget(self.delete_button)

        layout.addWidget(self.name_label)
        layout.addWidget(self.phrases_label)

        self.setLayout(layout)

    def delete_button_on_click(self,command:VoiceCommand,voice_commands:VoiceCommandsStorage):
        def helper():
            voice_commands.delete_command(command)

            nonlocal self
            self.phrases_label.setText("")
            self.name_label.setText("")
            self.delete_button.setText("")
        
        return helper


class CommandWindow(QWidget):
    def __init__(self,voice_commands:VoiceCommandsStorage,main_window:MainWindow):
        super().__init__()
        self.voice_commands = voice_commands
        self.main_window = main_window
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Список доступных комманд")
        self.setGeometry(100,100,200,300)

        self.back_button = QPushButton("Назад")
        self.back_button.clicked.connect(self.back_button_click)

        self.to_add_command_button = QPushButton("Добавить команду")
        self.add_command_window = None
        self.to_add_command_button.clicked.connect(self.to_add_command_window)

        layout = QVBoxLayout()
        self.list_widget = QListWidget(self)

        for phrases,command in self.voice_commands:
            item = QListWidgetItem(self.list_widget)
            command_item = CommandItem(phrases,command,self.voice_commands)
            item.setSizeHint(command_item.sizeHint())

            self.list_widget.addItem(item)
            self.list_widget.setItemWidget(item,command_item)

        layout.addWidget(self.to_add_command_button)
        layout.addWidget(self.list_widget)
        layout.addWidget(self.back_button)
        self.setLayout(layout)

    def to_add_command_window(self):
        # self.add_command_window = AddCommandMainWindow(self.voice_commands)
        # self.add_command_window.show()
        self.main_window.setCentralWidget(AddCommandMainWindow(self.voice_commands,self.main_window))
    
    def back_button_click(self):
        self.main_window.setMainCentralWidget()


class AddCommandWindowBase(QWidget):
    def __init__(self,voice_commands:VoiceCommandsStorage, main_window:MainWindow) -> None:
        super().__init__()
        self.voice_commands = voice_commands
        self.main_window = main_window
        self.init_ui()
    
    def init_ui(self):
        pass

    def clear_phrase_input(self,phrase_input:str):
        import re

        phrase_input = re.sub(r"\s{2,}","",phrase_input.lower().strip())

        for letter in phrase_input:
            if letter not in (RUSSIAN_LOW_LETTERS + (" ",",")):
                return False, phrase_input

        return True, phrase_input
    
    def create_command(self,msg_box:QMessageBox,command:VoiceCommand,phrases):
        text = "Команда успешно добавлена"
        try:
            self.voice_commands.create_new_command(command,phrases)
            self.main_window.setMainCentralWidget()
        except self.voice_commands.CommandPhraseExists as error:
            text = f"Фраза `{error.phrase}` уже существует"

        msg_box.setText(text)
        msg_box.exec()


    
    def add_important_widget_in_layout(self,layout):
        self.name_input, self.phrase_input = QLineEdit(),QLineEdit()
        self.name_input.setPlaceholderText("Имя команды")
        self.phrase_input.setPlaceholderText("Фразы, через запятую")
        self.back_button = QPushButton("Назад")
        self.back_button.clicked.connect(self.back_button_click)

        self.add_button = QPushButton("Создать")
        self.add_button.clicked.connect(self.add_button_click)

        layout.addWidget(self.name_input)
        layout.addWidget(self.phrase_input)
        layout.addWidget(self.add_button)
        layout.addWidget(self.back_button)

        return layout
    
    def back_button_click(self):
        self.main_window.setCentralWidget(AddCommandMainWindow(self.voice_commands,self.main_window))


    def add_button_click(self):
        is_phrases_clean, phrase_input = self.clear_phrase_input(self.phrase_input.text())
        phrases = [p.strip() for p in phrase_input.split(",")]
        error_message_text = None
        command_name = self.name_input.text().strip()

        if not is_phrases_clean:
            error_message_text = "Во фразе допускаются только русские буквы, пробелы и запятые"
        elif not len(phrases):
            error_message_text = "Введите хотя бы одну фразу"
        elif not command_name:
            error_message_text = "Введите имя команды"

        msg_box = QMessageBox()

        if error_message_text is not None:
            msg_box.setText(error_message_text)
            msg_box.exec()

        return (error_message_text is not None),command_name, phrases, msg_box



class AddBrowserCommandWindow(AddCommandWindowBase):
    def init_ui(self):
        self.setWindowTitle("Новая команда: Открытие сайта")
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Адрес сайта")

        layout = QVBoxLayout()
        layout.addWidget(self.url_input)
        self.setLayout(self.add_important_widget_in_layout(layout))
    
    def url_check(self,url):
        from re import search
        url_pattern = r"(https:\/\/www\.|http:\/\/www\.|https:\/\/|http:\/\/)?[a-zA-Z0-9]{2,}(\.[a-zA-Z0-9]{2,})(\.[a-zA-Z0-9]{2,})?"
        return search(url_pattern,url) is not None

    def add_button_click(self):
        is_error, command_name, phrases, msg_box = super().add_button_click()
        if is_error:
            return

        url = self.url_input.text()

        if not self.url_check(url):
            msg_box.setIcon(QMessageBox.Icon.Warning)
            msg_box.setText("Вы ввели неверный адрес сайта")
        else:
            command = VoiceCommand(
                    name=command_name,
                    action="ahk",
                    sounds=["hello"],
                    group="browser",
                    cli_cmd=None,
                    cli_args=None,
                    exe_path="ahk/Run browser.ahk",
                    exe_args=[url],
                    is_user_command=True
            )

            self.create_command(msg_box,command,phrases)




class AddFolderExeCommandWindow(AddCommandWindowBase):
    def init_ui(self):
        self.setWindowTitle("Новая команда: Показ каталога")
        self.folder_path_input = QLineEdit()
        self.folder_path_input.setPlaceholderText("Путь")

        layout = QHBoxLayout()
        layout.addWidget(self.folder_path_input)
        self.setLayout(self.add_important_widget_in_layout(layout))
    
    def check_folder_path(self,path):
        import os
        return os.path.exists(path)
    
    def add_button_click(self):
        is_error, command_name, phrases, msg_box = super().add_button_click()
        if is_error:
            return

        folder_path = self.folder_path_input.text()

        if not self.check_folder_path(folder_path):
            msg_box.setIcon(QMessageBox.Icon.Warning)
            msg_box.setText("По такому пути нет каталога")
        else:
            command = VoiceCommand(
                    name=command_name,
                    action="ahk",
                    sounds=["hello"],
                    group="windows",
                    cli_cmd=None,
                    cli_args=None,
                    exe_path="ahk/Open file.ahk",
                    exe_args=[folder_path],
                    is_user_command=True
            )

            self.create_command(msg_box,command,phrases)

class AddGameCommandWindow(AddCommandWindowBase):
    pass


class AddCommandMainWindow(QWidget):
    def __init__(self,voice_commands:VoiceCommandsStorage,main_window:MainWindow):
        super().__init__()
        self.voice_commands = voice_commands
        self.main_window = main_window
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Добавление новой команды")

        self.browser_button = QPushButton("Открытие сайта")
        self.folder_exe_button = QPushButton("Показ каталога\приложения")
        self.game_button = QPushButton("Включение игры")
        self.back_button = QPushButton("Назад")

        self.browser_button.clicked.connect(self.button_click("browser"))
        self.folder_exe_button.clicked.connect(self.button_click("folder_exe"))
        self.game_button.clicked.connect(self.button_click("game"))
        self.back_button.clicked.connect(self.back_button_click)

        layout = QVBoxLayout()
        layout.addWidget(self.browser_button)
        layout.addWidget(self.folder_exe_button)
        layout.addWidget(self.game_button)
        layout.addWidget(self.back_button)

        self.setLayout(layout)

    def back_button_click(self):
        self.main_window.setCentralWidget(CommandWindow(self.voice_commands,self.main_window))
    
    def button_click(self,button_name):
        to_open_window_type =  {
            "browser" : AddBrowserCommandWindow,
            "folder_exe" : AddFolderExeCommandWindow,
            "game" : AddGameCommandWindow
        }[button_name]

        def helper():
            self.main_window.setCentralWidget(to_open_window_type(self.voice_commands,self.main_window))

        return helper

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()