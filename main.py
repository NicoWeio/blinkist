import cloudscraper
from datetime import datetime
from pathlib import Path
import requests
from rich import print

BASE_URL = 'https://www.blinkist.com/'

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:101.0) Gecko/20100101 Firefox/101.0',
    'x-requested-with': 'XMLHttpRequest',
}

LOCALES = ['en', 'de']
DOWNLOAD_DIR = Path.home() / 'Musik' / 'Blinkist'

scraper = cloudscraper.create_scraper()


def get_free_daily(locale):
    # see also: https://www.blinkist.com/en/content/daily
    response = scraper.get(
        BASE_URL + 'api/free_daily',
        params={'locale': locale}
    )
    return response.json()


def get_chapters(book_slug):
    url = f"{BASE_URL}/api/books/{book_slug}/chapters"
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    return response.json()['chapters']


def get_chapter(book_id, chapter_id):
    url = f"{BASE_URL}/api/books/{book_id}/chapters/{chapter_id}"
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    return response.json()


def download_chapter_audio(book, chapter_data):
    book_dir = DOWNLOAD_DIR / f"{datetime.today().strftime('%Y-%m-%d')} – {book['slug']}"
    book_dir.mkdir(exist_ok=True)
    file_path = book_dir / f"chapter_{chapter_data['order_no']}.m4a"

    if file_path.exists():
        print(f"Skipping existing file: {file_path}")
        return

    assert 'm4a' in chapter_data['signed_audio_url']
    response = scraper.get(chapter_data['signed_audio_url'])
    assert response.status_code == 200
    file_path.write_bytes(response.content)
    print(f"Downloaded chapter {chapter_data['order_no']}")


for locale in LOCALES:
    free_daily = get_free_daily(locale=locale)
    book = free_daily['book']
    print(f"Today's free daily in {locale} is: “{book['title']}”")

    chapters = get_chapters(book['slug'])
    print(
        f"{len(chapters)} chapters:",
        ', '.join([c['action_title'] for c in chapters]),
    )

    for chapter in chapters:
        chapter_data = get_chapter(book['id'], chapter['id'])
        download_chapter_audio(book, chapter_data)
