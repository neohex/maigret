from http.cookiejar import MozillaCookieJar
from http.cookies import Morsel

import requests
from aiohttp import CookieJar


class ParsingActivator:
    @staticmethod
    def twitter(site, logger, cookies={}):
        try:
             headers = dict(site.headers)
             del headers["x-guest-token"]
             r = requests.post(site.activation["url"], headers=headers)
             logger.info(r)
             j = r.json()
             guest_token = j[site.activation["src"]]
             site.headers["x-guest-token"] = guest_token
        except BaseException as e:
             logger.error(e)

    @staticmethod
    def vimeo(site, logger, cookies={}):
        headers = dict(site.headers)
        if "Authorization" in headers:
            del headers["Authorization"]
        r = requests.get(site.activation["url"], headers=headers)
        try:
            jwt_token = r.json()["jwt"]
            site.headers["Authorization"] = "jwt " + jwt_token
        except BaseException as e:
            logger.error(e)
        

    @staticmethod
    def spotify(site, logger, cookies={}):
        headers = dict(site.headers)
        if "Authorization" in headers:
            del headers["Authorization"]
        r = requests.get(site.activation["url"])
        bearer_token = r.json()["accessTtoken"]
        site.headers["authorization"] = f"Bearer {bearer_token}"


def import_aiohttp_cookies(cookiestxt_filename):
    cookies_obj = MozillaCookieJar(cookiestxt_filename)
    cookies_obj.load(ignore_discard=True, ignore_expires=True)

    cookies = CookieJar()

    cookies_list = []
    for domain in cookies_obj._cookies.values():
        for key, cookie in list(domain.values())[0].items():
            c = Morsel()
            c.set(key, cookie.value, cookie.value)
            c["domain"] = cookie.domain
            c["path"] = cookie.path
            cookies_list.append((key, c))

    cookies.update_cookies(cookies_list)

    return cookies
