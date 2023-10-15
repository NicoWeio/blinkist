import pytest

from blinkist import blinkist
from blinkist.chapter import Chapter

# book = Book.from_slug('get-smart-en')
book = blinkist.get_free_daily('en')


@pytest.mark.skip(reason="Requires Blinkist Premium.")
def test_from_slug():
    # ↓ book-specific
    assert book.title == "Get Smart!"


def test_chapter_list():
    assert book.chapter_list
    assert all('id' in chapter for chapter in book.chapter_list)


def test_chapters():
    assert book.chapters
    assert all(isinstance(chapter, Chapter) for chapter in book.chapters)
    assert all(chapter.data['text'] for chapter in book.chapters)

    # ↓ book-specific
    # assert len(book.chapters) == 1+9+1


def test_download_cover(tmp_path):
    book.download_cover(tmp_path)
    assert (tmp_path / 'cover.jpg').is_file()


def test_download_text_md(tmp_path):
    book.download_text_md(tmp_path)
    assert (tmp_path / 'book.md').is_file()

# def test_serialize():

# def test_download_raw_yaml():
