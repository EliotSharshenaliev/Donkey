from bs4 import BeautifulSoup


def get_username(response_html):
    try:
        b4 = BeautifulSoup(response_html, "html.parser")
        username = b4.find('span', class_='username').get_text()
    except Exception as e:
        username = ""
        pass

    return username.encode('utf-8').decode('utf-8')


