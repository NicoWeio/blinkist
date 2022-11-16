from typing import Dict, List, Optional

from .book import Book
from .common import api_request_app, api_request_web, scraper
from .config import HEADERS_ALGOLIA
from .console import track
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
    ids = [item['item_id'] for item in get_free_items() if item['item_type'] == 'curated_list']
    return [CuratedList.from_slug_or_uuid(id_) for id_ in track(ids, description="Retrieving free curated lists…")]


def search_books(query: str, limit: Optional[int] = None, languages: Optional[List[str]] = None) -> List[Book]:
    """
    Search for books using the Algolia API.
    20 results are returned by default.
    """
    filter_languages = " OR ".join(f'language:{language}' for language in languages) if languages else None

    data = {
        'query': query,
        'attributesToRetrieve': [
            'title',
            'author',
            'slug',
            'language',
            'bundle'
        ],
        # 'hitsPerPage': limit,
        # 'attributesToHighlight': [
        #     'title',
        #     'author'
        # ],
        # 'filters': 'publishedAt < 1668591285 AND (language:de OR language:en)',
    }
    if limit:
        # NOTE: Silently ignores limit == 0
        data['hitsPerPage'] = limit
    if filter_languages:
        data['filters'] = filter_languages

    r = scraper.post(
        'https://p3sczpah8s-dsn.algolia.net/1/indexes/books-production/query',
        headers=HEADERS_ALGOLIA,
        json=data,
    )
    r.raise_for_status()
    slugs = [result['slug'] for result in r.json()['hits']]
    return [Book.from_slug(slug) for slug in track(slugs, description="Retrieving search results…")]
