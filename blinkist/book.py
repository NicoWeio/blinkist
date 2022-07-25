from pathlib import Path  # typing only
from typing import List  # typing only

from .common import api_request, request
from .console import console


class Book:
    def __init__(self, book_data: dict) -> None:
        self.data = book_data

        # pylint: disable=C0103
        self.id = book_data['id']
        self.title = book_data['title']
        self.slug = book_data['slug']

    def __repr__(self) -> str:
        return f"Book <{self.title}>"

    def get_chapter_list(self) -> List[dict]:
        """
        Returns the chapter list straight from the API.
        Does not include their respective contents.
        """
        return api_request(f'books/{self.slug}/chapters')['chapters']

    def download_cover(self, target_dir: Path) -> None:
        """
        Downloads the cover image to the given directory,
        in the highest resolution available.
        """
        # find the URL of the largest version
        urls = set()
        for source in self.data['image']['sources']:
            urls.add(source['src'])
            urls |= set(source['srcset'].values())
        # example: 'https://images.blinkist.io/images/books/617be9b56cee07000723559e/1_1/470.jpg' → 470
        url = sorted(urls, key=lambda x: int(x.split('/')[-1].rstrip('.jpg')), reverse=True)[0]

        file_path = target_dir / "cover.jpg"

        if file_path.exists():
            console.print(f"Skipping existing file: {file_path}")
            return

        assert url.endswith('.jpg')
        response = request(url)
        assert response.status_code == 200
        file_path.write_bytes(response.content)
