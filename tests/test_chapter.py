import pytest

from blinkist import blinkist
from blinkist.book import Book
from blinkist.chapter import Chapter

# book = Book.from_slug('get-smart-en')
book = blinkist.get_free_daily('en')
chapter = book.chapters[0]


@pytest.mark.skip(reason="Requires Blinkist Premium.")
def test_from_id():
    chapter = Chapter.from_id(book, '58da6e44232de90004a6e66d')
    assert chapter.data['text']


def test_download_audio(tmp_path):
    chapter.download_audio(tmp_path)
    assert (tmp_path / 'chapter_0.m4a').is_file()


@pytest.mark.skip(reason="There don't seem to be any books of this kind left.")
def test_download_audio_without_audio(tmp_path):
    book_without_audio = Book.from_slug('100-plus-en')
    chapter_without_audio = book_without_audio.chapters[0]
    chapter_without_audio.download_audio(tmp_path)
    assert not (tmp_path / 'chapter_0.m4a').is_file()
