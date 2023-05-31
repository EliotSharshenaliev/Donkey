def get_error_or_success_from_response(response, msg):
    try:
        if response["wsdlErrorNm"] == "실패":
            return msg["NotVisitable"]
    except KeyError as e:
        pass

    try:
        if response["result"] == 0:
            return msg["captcha"]
    except KeyError as e:
        pass

    try:
        if response["param"]["errYn"] == "Y":
            return f"{msg['InknowErro']}, {response}"
    except KeyError as e:
        pass

    return msg["succes_ordered"]