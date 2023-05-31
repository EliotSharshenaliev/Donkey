from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager

from lib.screens.login import LoginScreen
from lib.screens.main import MainScreen


class DonkeyApp(MDApp):
    def build(self):
        Builder.load_file("lib/ui/main.kv")
        AppRouter = MDScreenManager()
        AppRouter.current = "MainScreen"
        return AppRouter


if __name__ == '__main__':
    DonkeyApp().run()
