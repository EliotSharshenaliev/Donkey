import datetime
import os.path
import time


class LoginObj:
    def __init__(self, email):
        self.ksignInputMberId = ""
        self.loginType = "idpw"
        self.failResult = ""
        self.cffdnCd = ""
        self.callCd = ""
        self.loginId = email
        self.loginPwd = "Marat12!"
        self.captchaTxt = ""


class Constant:
    emblCd = "KY"
    visitResveBuss = "KY0001"
    Yn = "Y"

    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
    }

    url = {
        "get_captcha": "https://consul.mofa.go.kr/biz/common/captchaImage.do",
        "login": "https://consul.mofa.go.kr/cipl/0100/loginProcess.do",
        "main": "https://consul.mofa.go.kr/en/main.do",
        "selectVisitReserveTime": "https://consul.mofa.go.kr/ciph/0800/selectVisitReserveTime.do",
    }

    catching_timer = 2

    time_table = {
        "09:30": 0,
        "09:45": 1,
        "10:00": 2,
        "10:15": 3,
        "10:30": 4,
        "10:45": 5,
        "11:00": 6,
        "11:15": 7,
        "11:30": 8,
        "11:45": 9
    }

    time_list = ["09:30", "09:45", "10:00", "10:15", "10:30", "10:45", "11:00", "11:15", "11:30", "11:45"]

    def get_index(self, target_time):
        current_time_str = target_time.strftime("%H:%M")

        index = None
        previous_key = None
        for key in sorted(self.time_table.keys()):
            if current_time_str >= key:
                index = self.time_table[key]
                previous_key = key
            else:
                break
        return index

    data = {"emblCd": "KY", "visitDe": "",
            "resveTimeNm": "",
            "timeCd": "",
            "visitResveId": "",
            "businessNm": "{\"mainKindNm\":[\"비자 접수\"],\"cffdnNm\":[\"비자 접수\"]}",
            "grpNmListDB": "비자 접수", "cffdnNmDB": "비자 접수",
            "mainKind": "KY0001", "subKind": "KY0001",
            "natnCd": "130", "remk": "",
            "captchaTxt": "",
            "totcnt": 1,
            "onedaycnt": 1
            }

    msg = {
        "NotVisitable": "Your reservation has been closed at the \ntime you selected. Please choose a \ndifferent time.",
        "captcha": "Captcha entered wrong",
        "InknowErro": "Something went wrong, Error place Y",
        "succes_ordered": "Application has been completed.\n Reservation receipt has been sent to {} email address.",
    }