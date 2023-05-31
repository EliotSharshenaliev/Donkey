import threading
from kivy.metrics import dp
from kivy.uix.screenmanager import SlideTransition
from kivymd.toast import toast
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFillRoundFlatButton
from kivymd.uix.fitimage import FitImage
from kivymd.uix.screen import MDScreen
from kivymd.uix.spinner import MDSpinner
from kivymd.uix.textfield import MDTextField

from lib.api.login_api import LoginAPI


class LoginScreen(MDScreen):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        self.auth = None
        self.Layout = MDBoxLayout()
        self.api = LoginAPI()
        self.Layout.auth = None
        self.Layout.orientation = "vertical"
        self.Layout.spacing = "20dp"
        self.Layout.size_hint_x = .8
        self.Layout.pos_hint = {"center_x": .5, "center_y": .5}
        self.Layout.adaptive_height = True

        self.LogoMofa = FitImage(
            source="static/logo.png",
            size_hint=(None, None),
            size=(self.width + 80, self.height + 80),
            pos_hint={"center_x": .5, "center_y": .5}
        )
        self.EmailField = MDTextField(
            hint_text="Email",
            helper_text="Be careful! Here doesn't any validation exceptions!",
            helper_text_mode="persistent",
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            size_hint_x=None,
            width=500
        )

        self.LoginButton = MDFillRoundFlatButton(
            text="Login to consular service",
            text_color="white",
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            size_hint_x=None,
        )

        self.LoginButton.bind(on_release=self.on_login_button_click)
        self.spinner = MDSpinner(
            size_hint=(None, None),
            size=(dp(27), dp(27)),
            pos_hint={'center_x': .5, 'center_y': 0.5},
            active=False,
            palette=[
                [0.28627450980392155, 0.8431372549019608, 0.596078431372549, 1],
                [0.3568627450980392, 0.3215686274509804, 0.8666666666666667, 1],
                [0.8862745098039215, 0.36470588235294116, 0.592156862745098, 1],
                [0.8784313725490196, 0.9058823529411765, 0.40784313725490196, 1],
            ]
        )
        self.Layout.add_widget(self.LogoMofa)
        self.Layout.add_widget(self.EmailField)
        self.Layout.add_widget(self.LoginButton)

        self.add_widget(self.spinner)
        self.add_widget(self.Layout)

    def on_login_button_click(self, instance):
        threading.Thread(target=self.api.auth, name="authentication_thread", args=[
            self.on_authentication,
            self.handle_change_loader_state,
            self.EmailField.text,
        ]).start()

    def on_authentication(self, *args, **kwargs):
        screen_manager = self.manager
        screen_manager.transition = SlideTransition(direction='left')
        screen_manager.current = 'MainScreen'

    def handle_change_loader_state(self, loading=True):
        self.spinner.active = loading
        self.Layout.disabled = loading

    def on_enter(self, *args):
        threading.Thread(target=self.api.get_fist_requests,name="get_first_cookie_thread", args=[self.handle_change_loader_state, toast]).start()
