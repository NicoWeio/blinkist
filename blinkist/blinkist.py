from .book import Book
from .common import api_request


def get_free_daily(locale) -> Book:
    """
    Returns the "free daily" book for the given locale.
    """
    # see also: https://www.blinkist.com/en/content/daily
    free_daily = api_request('free_daily', params={'locale': locale})
    return Book(free_daily['book'])
