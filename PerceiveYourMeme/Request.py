from random import randint
from time import sleep

from fake_useragent import UserAgent
from requests import session, Response

ua = UserAgent()

HEADERS = {
    "User-Agent": ua.chrome,
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip",
    "Accept-Language": "en-US,en;q=0.9,es;q=0.8",
    "Connection": "keep-alive",
    "sec-ch-ua": '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
}

http = session()
http.headers.update(HEADERS)


def get(url: str) -> Response:
    for i in range(4):
        sleep(30 + randint(0, 10000) / 1000.0)
        res = http.get(url)
        if not res or res.status_code >= 400:
            print("error", i, res.status_code, res.text)
        else:
            return res

    raise Exception()
