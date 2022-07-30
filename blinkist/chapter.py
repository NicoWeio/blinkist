from pathlib import Path  # typing only

from .common import api_request_web, request
from .console import console


class Chapter:
    def __init__(self, chapter_data: dict):
        self.data = chapter_data

        # pylint: disable=C0103
        self.id = chapter_data['id']

    @staticmethod
    def from_id(book, chapter_id) -> 'Chapter':
        chapter_data = api_request_web(f'books/{book.id}/chapters/{chapter_id}')
        return Chapter(chapter_data)

    def serialize(self) -> dict:
        """
        Serializes the chapter to a dict.
        """
        return self.data

    def download_audio(self, target_dir: Path) -> None:
        if not self.data.get('signed_audio_url'):
            # NOTE: In books where is_audio is true, every chapter should have audio, so this should never happen.
            console.print(f'No audio for chapter {self.id}')
            return

        file_path = target_dir / f"chapter_{self.data['order_no']}.m4a"

        assert 'm4a' in self.data['signed_audio_url']
        response = request(self.data['signed_audio_url'])
        assert response.status_code == 200
        file_path.write_bytes(response.content)
