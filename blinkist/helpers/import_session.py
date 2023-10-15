"""
Helper for importing the Blinkist session cookie from Firefox.
Adapted from https://github.com/instaloader/instaloader/blob/master/docs/codesnippets/615_import_firefox_session.py
"""

from glob import glob
from os.path import expanduser
from platform import system
from sqlite3 import OperationalError, connect


def get_cookiefile():
    default_cookiefile = {
        "Windows": "~/AppData/Roaming/Mozilla/Firefox/Profiles/*/cookies.sqlite",
        "Darwin": "~/Library/Application Support/Firefox/Profiles/*/cookies.sqlite",
    }.get(system(), "~/.mozilla/firefox/*/cookies.sqlite")
    cookiefiles = glob(expanduser(default_cookiefile))
    if not cookiefiles:
        raise RuntimeError("No Firefox cookies.sqlite file found.")
    return cookiefiles[0]


def import_session():
    cookiefile = get_cookiefile()
    # print(f"Using cookies from {cookiefile}")
    conn = connect(f"file:{cookiefile}?immutable=1", uri=True)
    try:
        cookie_data = conn.execute(
            "SELECT name, value FROM moz_cookies WHERE baseDomain='blinkist.com'"
        )
    except OperationalError:
        cookie_data = conn.execute(
            "SELECT name, value FROM moz_cookies WHERE host LIKE '%blinkist.com'"
        )

    cookie_data = dict(cookie_data)

    # TODO: Test login, e.g. via /api/me

    # TODO: Save session

    try:
        return {
            k: cookie_data[k]
            for k in ['_blinkist-webapp_session']
        }
    except KeyError as e:
        raise RuntimeError("Could not find session cookie in Firefox cookies.sqlite file.") from e


def import_session_or_none():
    try:
        return import_session()
    except RuntimeError:
        return None
