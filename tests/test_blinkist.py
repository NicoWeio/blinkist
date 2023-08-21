from blinkist import blinkist


def test_get_free_daily():
    book_de = blinkist.get_free_daily('de')
    book_en = blinkist.get_free_daily('en')
    assert book_de.language == 'de'
    assert book_en.language == 'en'
    assert book_de.slug != book_en.slug


def test_get_latest_collections():
    collections = blinkist.get_latest_collections()
    assert len(collections) > 0
    assert len(collections) == 8
    assert collections[0].title
    assert collections[0].books


class TestSearchBooks:
    def test_default(self):
        books = blinkist.search_books("smart")
        assert len(books) == 20

    def test_limit(self):
        books = blinkist.search_books("smart", limit=5)
        assert len(books) == 5

    def test_languages(self):
        books = blinkist.search_books("smart", languages=['de', 'en'], limit=5)
        assert len(books) == 5
        assert all(book.language in ['de', 'en'] for book in books)

        books = blinkist.search_books("smart", languages=['de'], limit=5)
        assert len(books) == 5
        assert all(book.language == 'de' for book in books)
