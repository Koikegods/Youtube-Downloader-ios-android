from yt_dlp import YoutubeDL
import os
import threading
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from time import sleep

save_addr = f"{os.environ['USERPROFILE']}\Downloads"
print(save_addr)

layout = BoxLayout


class cd:
    """Context manager for changing the current working directory"""
    def __init__(self, newPath):
        self.newPath = os.path.expanduser(newPath)

    def __enter__(self):
        self.savedPath = os.getcwd()
        os.chdir(self.newPath)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedPath)


class App(layout):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            self.orientation = "vertical"
            self.spacing = 20
            self.padding = [10, 10]
            self.cols = 1
            self.label = Label(text="")
            self.add_widget(self.label)
            self.link = TextInput(hint_text="", multiline=False)
            self.add_widget(self.link)
            self.btn = Button(text="Download")
            threading.Thread(self.btn.bind(on_press=lambda x: self.callback())).start()
            self.add_widget(self.btn)
            sleep(3)

        def callback(self):
            video = str(self.link.text)
            with YoutubeDL() as ydl:
                info_dict = ydl.extract_info(video, download=False)
                video_title = info_dict.get('title', None)

            ydl_opts = {'outtmpl': f"{save_addr}\{video_title}" + '.%(ext)s',
                        'format': 'best+mp4'
                        }
            # download
            ydl = YoutubeDL(ydl_opts)
            ydl.download(video)
            self.label.text = f"Download success"
            self.link.text = f"{save_addr}"
            self.btn.text = "Download"

class main(App):
        def build(self):
            return App()
if __name__ == '__main__':
    main().run()