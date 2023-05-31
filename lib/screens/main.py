import datetime
import os
import shutil
import threading

from kivy.properties import BooleanProperty
from kivy.uix.screenmanager import SlideTransition
from kivymd.toast import toast
from kivymd.uix.screen import MDScreen
from constant import STATIC
from lib.api.main_api import MainAPI
from lib.components.date_picker import CustomizedDateTimePicker


class MainScreen(MDScreen, CustomizedDateTimePicker):
    isWorking = BooleanProperty(defaultvalue=False)
    isAttacking = BooleanProperty(defaultvalue=False)

    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.api = MainAPI()
        self.date = None
        self.time = None
        self.catching_tsk = None

    def handle_change_loader_state(self, loading=True):
        self.ids.spinner.start() if loading else self.ids.spinner.stop()
        self.ids.center_layout.disabled = loading

    def handle_change_title_toolbar(self, state):
        self.ids.toolbar.title = state

    def on_enter(self):

        if self.api.load_cookie():
            threading.Thread(target=self.api.get_main_page,
                             name="get_main_page_thread",
                             args=[self.handle_change_loader_state,
                                   self.handle_change_title_toolbar, self.on_logout, ]
                             ).start()
            self.on_press_reload_captcha()
        else:
            self.on_logout()

    def on_logout(self, *args, **kwargs):
        if os.path.exists(STATIC.get("cookies")):
            os.remove(STATIC.get("cookies"))

        if os.path.exists(STATIC.get("captcha")):
            shutil.rmtree(STATIC.get("captcha"))

        os.makedirs(STATIC.get("captcha"))
        self.api.delete_cookies()
        screen_manager = self.manager
        screen_manager.transition = SlideTransition(direction='right')
        screen_manager.current = 'LoginScreen'

    # ////////////////////// DateTime Picker functionality

    def on_save_date(self, instance, value, date_range):
        self.ids.DateLabel.color = "black"
        self.ids.DateLabel.text = str(value)
        self.date = str(value)

    def on_save_time(self, instance, time):
        start_time = datetime.time(9, 30)
        end_time = datetime.time(12, 00)

        if start_time <= time <= end_time:
            self.ids.TimeLabel.color = "black"
            self.ids.TimeLabel.text = str(time)
            self.time = time
        else:
            toast("Please select time 9:30 AM ~ 12:00 AM")

    # /// captcha side

    def on_press_reload_captcha(self, *args, **kwargs):
        self.ids.CaptchaField.text = ""
        threading.Thread(target=self.api.get_captcha_image,
                         name="reload_captcha_thread",
                         args=[self.on_stop_reload_captcha, self.ids.reload_captcha_btx]
                         ).start()

    def on_stop_reload_captcha(self, source: str):
        self.ids.captchaImage.source = ""
        self.ids.captchaImage.source = source

    # MAIN BUTTONS FOR ATTACK OR CATCH Place
    #  the functions is main functional of this project

    def on_click_catch(self):
        if not self.date:
            self.ids.DateLabel.text = "The date field is required"
            self.ids.DateLabel.color = "red"
            return

        if not self.time:
            self.ids.TimeLabel.text = "The time field is required"
            self.ids.TimeLabel.color = "red"
            return

        captcha = self.ids.CaptchaField
        if not captcha.text:
            captcha.error = True
            return

        text_field = self.ids.UserInformationField
        if not text_field.text:
            text_field.error = True
            return
        self.isWorking = 1

        self.api.start_catching_session()
        self.ids.spinner.start()

        threading.Thread(
            target=self.api.catch_session,
            name="catch_session_thread",
            args=[toast, self.on_logout]
        ).start()

    def on_click_stop_catch(self):
        self.ids.spinner.stop()
        self.api.stop_catching_session()
        self.isWorking = 0

    def on_click_attack(self):
        self.isAttacking = 1
        index_of_time = self.api.get_index(self.time)
        if index_of_time:
            threading.Thread(
                target=self.api.start_attack,
                name="attacking_thread",
                args=[
                    self.date,
                    index_of_time,
                    self.ids.CaptchaField.text,
                    self.ids.UserInformationField.text,
                    toast,
                    self.on_click_stop_attacking
                ]
            ).start()

    def on_click_stop_attacking(self):
        self.api.stop_attacking()
        self.isAttacking = 0

    def print_running_threads(self):
        threads = threading.enumerate()
        print(f"Running threads: {len(threads)}")
        for thread in threads:
            print(f"Thread name: {thread.name}")