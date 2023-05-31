import json
import os.path
import time
import uuid
from kivy import Logger
from kivy.clock import Clock
from requests import exceptions

from constant import STATIC
from lib.api.const import Constant
from lib.api.index_init_api import HttpConnectionThread
from lib.utills.get_username_html import get_username
import requests

from lib.utills.valitators.reservation_response import get_error_or_success_from_response


class MainAPI(HttpConnectionThread):
    def __init__(self):
        super().__init__()
        self.attacking = False
        self.last_captcha_name = None
        self.is_catching = None

    def load_cookie(self):
        try:
            with open(STATIC.get("cookies"), "r") as file:
                self.session.cookies.update(json.load(file))
                return 1
        except FileNotFoundError as e:
            return 0

    def delete_cookies(self):
        self.session.cookies.clear()

    def get_main_page(self,
                      handle_change_loader_state,
                      handle_change_title_toolbar,
                      on_logout):
        Clock.schedule_once(lambda x: handle_change_loader_state(True))
        try:
            response = self.main()
            user = get_username(response)
            if user:
                Clock.schedule_once(lambda x: handle_change_title_toolbar(user))
            else:
                Clock.schedule_once(lambda x: on_logout())
        except Exception as e:
            pass
        finally:
            Clock.schedule_once(lambda x: handle_change_loader_state(False))

    def get_captcha_image(self, on_stop_reload_captcha, instance):
        try:
            instance.text = "Loading..."
            import time
            if os.path.exists(f"static/captcha/{self.last_captcha_name}.jpg"):
                os.remove(f"static/captcha/{self.last_captcha_name}.jpg")
            name_of_captcha = uuid.uuid1()
            response = self.session.get(self.url["get_captcha"] + f"?g={int(time.time() * 1000)}&objGubn=captchaImg")
            if response.status_code == 200:
                with open(f"static/captcha/{name_of_captcha}.jpg", 'wb') as f:
                    f.write(response.content)
                    self.last_captcha_name = name_of_captcha
                    Clock.schedule_once(lambda xt: on_stop_reload_captcha(f"static/captcha/{name_of_captcha}.jpg"))
        except exceptions.RequestException as e:
            instance.text = "Error!"
            Logger.debug('UrlRequest: {0} Fetch url <{1}>'.format(
                id(self), e))
        instance.text = "Reload the captcha"

    def start_catching_session(self):
        self.is_catching = True

    def catch_session(self, set_error, on_logout):
        while self.is_catching:
            time.sleep(self.catching_timer)  # для заддержки что бы не брокировал сайт
            try:
                response = self.session.get(self.url.get("main"))
                self.session.cookies.update(response.cookies)
                if not get_username(response.content):
                    if self.attacking:
                        self.attacking = False
                    Clock.schedule_once(lambda xt: on_logout())
            except Exception as e:
                Clock.schedule_once(lambda x: set_error("Looking connection error"))

    def stop_catching_session(self):
        self.is_catching = False

    def start_attack(self, visitDe, index_of_time, captcha, remk, messager, to_stop_attack):
        self.attacking = True
        obj = self.get_possible_place(visitDe=visitDe, prefixTime=index_of_time)
        if obj:
            payload = self.data
            payload["visitDe"] = obj["visitDe"]
            payload["resveTimeNm"] = obj["timeNm"][:5]
            payload["timeCd"] = obj["timeCd"]
            payload["visitResveId"] = obj["visitResveId"]
            payload["remk"] = remk
            payload["captchaTxt"] = captcha

            with self.session.post(url=self.url["insertResveVisitEng"], data=payload) as r:
                if r.status_code == 200:
                    response = json.loads(r.content)
                    message = get_error_or_success_from_response(response=response, msg=self.msg)
                    Clock.schedule_once(lambda x: messager(message))
        else:
            Clock.schedule_once(lambda x: messager("Please select another date to reservation"))

        self.attacking = False
        Clock.schedule_once(lambda x: to_stop_attack())


    def get_possible_place(self, visitDe: str, prefixTime=None):

        while self.attacking:
            try:
                payload = {
                    "emblCd": self.emblCd,
                    "visitDe": visitDe,
                    "visitResveBussGrpCd": self.visitResveBuss
                }

                res = self.session.post(
                    url=self.url.get("selectVisitReserveTime"),
                    headers=self.headers,
                    data=payload
                )

                response = json.loads(res.content)
                if response["resveResult"][prefixTime]["visitYn"] == self.Yn:
                    return response["resveResult"][prefixTime]
            except Exception as e:
                return 0

    def stop_attacking(self):
        self.attacking = False