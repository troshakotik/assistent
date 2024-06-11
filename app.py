# from PyQt6.QtCore import QSize, Qt
# from PyQt6.QtWidgets import (
#     QApplication, 
#     QMainWindow,
#     QLabel,
#     QWidget,
#     QPushButton,
#     QHBoxLayout,
#     QVBoxLayout,
#     QListWidget,
#     QListWidgetItem,
#     QLineEdit,
#     QMessageBox
# )


# import sys
# from voice_recognation_thread import VoiceRecognationTread
# from voice_assistent import VoiceAssistant
# from utils import beatiful_string, add_command
# import config


# class MainWindow(QMainWindow):
#     def __init__(self) -> None:
#         super().__init__()
#         self.init_ui()
#         self.init_voice_thread()
#         self.command_window = None

#     def init_ui(self):
#         self.setWindowTitle("Lolly")
#         self.setFixedSize(QSize(400,400))

#         layout = QHBoxLayout()

#         self.label = QLabel()
#         self.label.setText("Готов слушать")

#         self.show_command_button = QPushButton("список комманд")
#         self.show_command_button.clicked.connect(self.show_command_button_click)

#         self.stop_listen_button = QPushButton("Перестать слушать")
#         self.stop_listen_button.clicked.connect(self.stop_listen_button_click)

#         layout.addWidget(self.label)
#         layout.addWidget(self.show_command_button)
#         layout.addWidget(self.stop_listen_button)

#         central_widget = QWidget()
#         central_widget.setLayout(layout)

#         self.setCentralWidget(central_widget)

    
#     def show_command_button_click(self):
#         self.command_window = CommandWindow(self.voice_assistant.commands)
#         self.command_window.show()
    
#     def stop_listen_button_click(self):
#         if self.voice_thread.isFinished():
#             self.voice_thread.start()
#         else:
#             self.voice_thread.quit()
#             self.voice_thread.wait()


#     def init_voice_thread(self):
#         self.voice_assistant = VoiceAssistant()
#         self.voice_thread = VoiceRecognationTread(self.voice_assistant)
#         self.voice_thread.start()
    
#         self.voice_thread.recognized_text_signal.connect(self.after_recognition_phrase)
#         self.voice_thread.start_listen_signal.connect(self.start_listen_process)
#         self.voice_thread.stop_listen_signal.connect(self.stop_listen_process)

#         self.voice_thread.finished.connect(self.voice_thread_finished)
#         self.voice_thread.started.connect(self.voice_thread_started)

    
#     def start_listen_process(self):
#         self.setStyleSheet("background-color: red;")
    
#     def stop_listen_process(self):
#         self.setStyleSheet("background-color: white;")

#     def voice_thread_finished(self):
#         print("voice thread is finished")
    
#     def voice_thread_started(self):
#         print("voice thread is starting")
    
#     def after_recognition_phrase(self,result):
#         if result["is_recognitioned"]:
#             self.label.setText(result["text"])
#         else:
#             self.label.setText("Не распознал")


# class CommandItem(QWidget):
#     def __init__(self,command):
#         super().__init__()

#         self.phrases_label = QLabel()
#         phrases = ",\n".join(command["phrases"])
#         self.phrases_label.setText(f"Фразы:\n {phrases}")

#         self.name_label = QLabel()
#         name = beatiful_string(command["command"]["name"])
#         self.name_label.setText(name)

#         layout = QHBoxLayout()
#         layout.addWidget(self.name_label)
#         layout.addWidget(self.phrases_label)
#         self.setLayout(layout)


# class CommandWindow(QWidget):
#     def __init__(self,commands):
#         super().__init__()
#         self.init_ui(commands)

#     def init_ui(self,commands):
#         self.setWindowTitle("Список доступных комманд")
#         self.setGeometry(100,100,200,300)

#         self.to_add_command_button = QPushButton("Добавить команду")
#         self.add_command_window = None
#         self.to_add_command_button.clicked.connect(self.to_add_command_window)

#         layout = QVBoxLayout()
#         self.list_widget = QListWidget(self)

#         for command in commands:
#             item = QListWidgetItem(self.list_widget)
#             command_item = CommandItem(command)
#             item.setSizeHint(command_item.sizeHint())

#             self.list_widget.addItem(item)
#             self.list_widget.setItemWidget(item,command_item)

#         layout.addWidget(self.to_add_command_button)
#         layout.addWidget(self.list_widget)
#         self.setLayout(layout)
    
#     def to_add_command_window(self):
#         self.add_command_window = AddCommandMainWindow()
#         self.add_command_window.show()


# class AddCommandWindowBase(QWidget):
#     def __init__(self) -> None:
#         super().__init__()
#         self.init_ui()
    
#     def init_ui(self):
#         pass
    
#     def add_important_widget_in_layout(self,layout):
#         self.name_input, self.phrase_input = QLineEdit(),QLineEdit()
#         self.name_input.setPlaceholderText("Имя команды")
#         self.phrase_input.setPlaceholderText("Фразы, через запятую")

#         self.add_button = QPushButton("Создать")
#         self.add_button.clicked.connect(self.add_button_click)

#         layout.addWidget(self.name_input)
#         layout.addWidget(self.phrase_input)
#         layout.addWidget(self.add_button)

#         return layout


#     def add_button_click(self):
#         phrases = [p.strip() for p in self.phrase_input.text().split(",")]
#         command_name = self.name_input.text().strip()

#         msg_box = QMessageBox()
        
#         if not len(phrases):
#             msg_box.setIcon(QMessageBox.Icon.Warning)
#             msg_box.setText("Введите хотя бы одну фразу")
#         elif not command_name:
#             msg_box.setIcon(QMessageBox.Icon.Warning)
#             msg_box.setText("Введите имя комманды")
        
#         return command_name, phrases, msg_box



# class AddBrowserCommandWindow(AddCommandWindowBase):
#     def init_ui(self):
#         self.setWindowTitle("Новая команда: Открытие сайта")
#         self.url_input = QLineEdit()
#         self.url_input.setPlaceholderText("Адрес сайта")

#         layout = QHBoxLayout()
#         layout.addWidget(self.url_input)
#         self.setLayout(self.add_important_widget_in_layout(layout))
    
#     def url_check(self,url):
#         from re import search
#         url_pattern = r"(https:\/\/www\.|http:\/\/www\.|https:\/\/|http:\/\/)?[a-zA-Z0-9]{2,}(\.[a-zA-Z0-9]{2,})(\.[a-zA-Z0-9]{2,})?"
#         return search(url_pattern,url) is not None

#     def add_button_click(self):
#         command_name, phrases, msg_box = super().add_button_click()
#         url = self.url_input.text()

#         if not self.url_check(url):
#             msg_box.setIcon(QMessageBox.Icon.Warning)
#             msg_box.setText("Вы ввели неверный адрес сайта")
#         else:
#             add_command(
#                 name=command_name,
#                 exe_path="ahk/Run browser.ahk",
#                 exe_args=[url],
#                 phrases=phrases,
#                 command_path=r"{}\{}\{}".format(config.COMMANDS_PATH,"browser",config.COMMANDS_FILE_NAME)
#             )
#             msg_box.setText("Успешно добавлено")
#             msg_box.setIcon(QMessageBox.Icon.Information)

#         self.close()
#         msg_box.exec()




# class AddFolderExeCommandWindow(AddCommandWindowBase):
#     def init_ui(self):
#         self.setWindowTitle("Новая команда: Показ каталога")
#         self.folder_path_input = QLineEdit()
#         self.folder_path_input.setPlaceholderText("Путь")

#         layout = QHBoxLayout()
#         layout.addWidget(self.folder_path_input)
#         self.setLayout(self.add_important_widget_in_layout(layout))
    
#     def check_folder_path(self,path):
#         import os
#         return os.path.exists(path)
    
#     def add_button_click(self):
#         command_name, phrases, msg_box = super().add_button_click()
#         folder_path = self.folder_path_input.text()

#         if not self.check_folder_path(folder_path):
#             msg_box.setIcon(QMessageBox.Icon.Warning)
#             msg_box.setText("По такому пути нет каталога")
#         else:
#             add_command(
#                 name=command_name,
#                 exe_path="ahk/Open file.ahk",
#                 exe_args=[folder_path],
#                 phrases=phrases,
#                 command_path=r"{}\{}\{}".format(config.COMMANDS_PATH,"windows",config.COMMANDS_FILE_NAME)
#             )
#             msg_box.setText("Успешно добавлено")
#             msg_box.setIcon(QMessageBox.Icon.Information)

#         self.close()
#         msg_box.exec()


# class AddApplicationCommandWindow(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.init_ui()
    
#     def init_ui(self):
#         self.setWindowTitle("Новая команда: Запуск приложения")

# class AddGameCommandWindow(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.init_ui()
    
#     def init_ui(self):
#         self.setWindowTitle("Новая команда: Включение игры")


# class AddCommandMainWindow(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.init_ui()
    
#     def init_ui(self):
#         self.setWindowTitle("Добавление новой команды")

#         self.browser_button = QPushButton("Открытие сайта")
#         self.folder_exe_button = QPushButton("Показ каталога\приложения")
#         self.game_button = QPushButton("Включение игры")

#         self.browser_button.clicked.connect(self.button_click("browser"))
#         self.folder_exe_button.clicked.connect(self.button_click("folder_exe"))
#         self.game_button.clicked.connect(self.button_click("game"))

#         self.window1 = None
#         self.window2 = None
#         self.window3 = None

#         layout = QHBoxLayout()
#         layout.addWidget(self.browser_button)
#         layout.addWidget(self.folder_exe_button)
#         layout.addWidget(self.game_button)

#         self.setLayout(layout)
    
#     def button_click(self,button_name):
#         to_open_window_type, window_name =  {
#             "browser" : (AddBrowserCommandWindow,"window1"),
#             "folder_exe" : (AddFolderExeCommandWindow,"window2"),
#             "game" : (AddGameCommandWindow,"window3")
#         }[button_name]

#         def helper():
#             setattr(self,window_name,to_open_window_type())
#             getattr(self,window_name).show()
        
#         return helper


if __name__ == "__main__":
    from voice_assistent import VoiceAssistant
    v = VoiceAssistant()
    v.react("заблокируй компьютер")