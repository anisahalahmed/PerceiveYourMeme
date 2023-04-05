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


class NotFoundException(Exception):
    pass


def get(url: str) -> Response:
    sleep(30)
    for i in range(4):
        sleep(randint(1000, 8000) / 1000.0)
        try:
            res = http.get(url, timeout=10)
        except Exception as e:
            print("error", e, "retries", i)
            continue
        if res.status_code == 404:
            raise NotFoundException
        elif res.status_code >= 400:
            print("error", res.status_code, "retries", i, "response", res.text)
        else:
            return res

    raise Exception()
