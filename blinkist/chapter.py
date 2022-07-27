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
        if 'signed_audio_url' not in self.data:
            console.print(f'No audio for chapter {self.id}')
            # NOTE: Probably, the whole book has no audio. We might want to handle this there.
            return

        file_path = target_dir / f"chapter_{self.data['order_no']}.m4a"

        assert 'm4a' in self.data['signed_audio_url']
        response = request(self.data['signed_audio_url'])
        assert response.status_code == 200
        file_path.write_bytes(response.content)
