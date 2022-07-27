from typing import Dict, List

from .book import Book
from .common import api_request_app, api_request_web
from .curated_list import CuratedList


def get_free_daily(locale) -> Book:
    """
    Returns the "free daily" book for the given locale.

    NOTE: There might be a subtle difference between `locale` and `language`.
    I'll stick with Blinkist's naming convention here.
    """
    # see also: https://www.blinkist.com/en/content/daily
    free_daily = api_request_web('free_daily', params={'locale': locale})
    return Book(free_daily['book'])


def get_free_items() -> List[Dict]:
    """
    Returns a list of free items, each consisting of a type and an ID.
    Known item types are 'curated_list', 'book' and 'episode'.
    """
    return api_request_app('contentaccess/free_items')['items']


def get_free_curated_lists() -> List[CuratedList]:
    """
    Returns a list of books from the "free curated lists" collection.
    """
    return [CuratedList.from_slug_or_uuid(item['item_id']) for item in get_free_items() if item['item_type'] == 'curated_list']
