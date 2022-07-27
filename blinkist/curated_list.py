from functools import cached_property

from rich.progress import track

from .book import Book
from .common import api_request_app


class CuratedList:
    def __init__(self, data):
        self.data = data

        # pylint: disable=C0103
        self.id = data['id']
        self.title = data['title']

    @cached_property
    def books(self):
        return [
            Book.from_slug(content_item['content_item_id'])
            for content_item in track(self.data['content_items'], description='Fetching books…')
            if content_item['content_item_type'] == 'book'
        ]

    @staticmethod
    def from_slug_or_uuid(slug_or_uuid: str) -> 'CuratedList':
        """
        Loads a collection by its slug/UUID.
        """
        return CuratedList(api_request_app(f"content/curated_lists/{slug_or_uuid}")['curated_list'])
