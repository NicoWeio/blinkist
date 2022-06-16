#!/usr/bin/env python3
import cloudscraper
from datetime import datetime
from pathlib import Path
from rich import print
from rich.progress import track
import tenacity

BASE_URL = 'https://www.blinkist.com/'

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:101.0) Gecko/20100101 Firefox/101.0',
    'x-requested-with': 'XMLHttpRequest',
}

CLOUDFLARE_MAX_ATTEMPTS = 10
CLOUDFLARE_WAIT_TIME = 2

LOCALES = ['en', 'de']
DOWNLOAD_DIR = Path.home() / 'Musik' / 'Blinkist'

scraper = cloudscraper.create_scraper()


@tenacity.retry(
    retry=tenacity.retry_if_exception_type(cloudscraper.exceptions.CloudflareChallengeError),
    wait=tenacity.wait_fixed(CLOUDFLARE_WAIT_TIME),
    stop=tenacity.stop_after_attempt(CLOUDFLARE_MAX_ATTEMPTS),
    # before_sleep=lambda attempt, delay: print(f"Retrying after {delay} seconds…"),
)
def _api_request(endpoint, params=None):
    url = f"{BASE_URL}api/{endpoint}"
    response = scraper.get(url, params=params, headers=HEADERS)

    # handle Cloudflare errors
    if response.status_code == 403 or "complete the security check" in response.text:
        # TODO: reset scraper for the next try?
        raise cloudscraper.exceptions.CloudflareChallengeError()

    response.raise_for_status()  # handle other errors
    return response.json()


def get_book_dir(book):
    return DOWNLOAD_DIR / f"{datetime.today().strftime('%Y-%m-%d')} – {book['slug']}"


def get_free_daily(locale):
    # see also: https://www.blinkist.com/en/content/daily
    return _api_request('free_daily', params={'locale': locale})


def get_chapters(book_slug):
    return _api_request(f'books/{book_slug}/chapters')['chapters']


def get_chapter(book_id, chapter_id):
    return _api_request(f'books/{book_id}/chapters/{chapter_id}')


def download_chapter_audio(book, chapter_data):
    book_dir = get_book_dir(book)
    book_dir.mkdir(exist_ok=True)
    file_path = book_dir / f"chapter_{chapter_data['order_no']}.m4a"

    if file_path.exists():
        print(f"Skipping existing file: {file_path}")
        return

    assert 'm4a' in chapter_data['signed_audio_url']
    response = scraper.get(chapter_data['signed_audio_url'], headers=HEADERS)
    assert response.status_code == 200
    file_path.write_bytes(response.content)


for locale in LOCALES:
    free_daily = get_free_daily(locale=locale)
    book = free_daily['book']
    print(f"Today's free daily in {locale} is: “{book['title']}”")

    # list of chapters without their content
    chapter_list = get_chapters(book['slug'])

    # fetch chapter content
    chapters = [get_chapter(book['id'], chapter['id']) for chapter in track(chapter_list, description='Fetching chapters…')]

    # download audio
    for chapter in track(chapters, description='Downloading audio…'):
        download_chapter_audio(book, chapter)
