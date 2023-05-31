import json
from kivy.clock import Clock
from kivy import Logger
import time
from constant import STATIC
from lib.api.const import LoginObj
from lib.api.index_init_api import HttpConnectionThread
from lib.utills.get_username_html import get_username


class LoginAPI(HttpConnectionThread):

    def auth(self,
             on_authentication,
             handle_change_loader_state,
             email,
             ) -> str | int:
        try:
            handle_change_loader_state(True)
            payload_class = LoginObj(email=email)
            response = self.session.post(self.url["login"], data=payload_class.__dict__, headers=self.headers)
            if response.status_code == 200:
                username = get_username(response_html=response.content)
                if username:
                    with open(STATIC.get("cookies"), "w") as file:
                        json.dump(self.session.cookies.get_dict(), file)
                    Clock.schedule_once(on_authentication)
            else:
                return 0

        except Exception as e:
            return 0

        finally:
            handle_change_loader_state(False)

    def get_fist_requests(self, handle_change_loader_state, on_error):
        Clock.schedule_once(lambda x: handle_change_loader_state(True))
        while True:
            try:
                r = self.session.get(self.url["main"])
                self.session.cookies.update(r.cookies)
                Clock.schedule_once(lambda x: handle_change_loader_state(False))
                break
            except Exception as e:
                Clock.schedule_once(lambda x: on_error("Connection error"))
                time.sleep(3)