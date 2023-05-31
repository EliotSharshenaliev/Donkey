import requests
from kivy import Logger
from requests import exceptions

from lib.api.const import Constant


class HttpConnectionThread(Constant):
    def __init__(self):
        self.session = requests.Session()

    def main(self):
        try:
            r = self.session.get(self.url["main"])
            self.session.cookies.update(r.cookies)
            return r.content
        except exceptions.RequestException as e:
            Logger.debug("Url requests error: {0}".format(e.args))

