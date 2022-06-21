#!/usr/bin/env python3
import cloudscraper
from datetime import datetime
from pathlib import Path
from rich.console import Console
from rich.progress import track
import tenacity

BASE_URL = 'https://www.blinkist.com/'

HEADERS = {
    'x-requested-with': 'XMLHttpRequest',
}

CLOUDFLARE_MAX_ATTEMPTS = 10
CLOUDFLARE_WAIT_TIME = 2

LOCALES = ['en', 'de']
DOWNLOAD_DIR = Path.home() / 'Musik' / 'Blinkist'

console = Console()
scraper = cloudscraper.create_scraper()


@tenacity.retry(
    retry=tenacity.retry_if_exception_type(cloudscraper.exceptions.CloudflareChallengeError),
    wait=tenacity.wait_fixed(CLOUDFLARE_WAIT_TIME),
    stop=tenacity.stop_after_attempt(CLOUDFLARE_MAX_ATTEMPTS),
    before_sleep=lambda retry_state: console.print(f"Retrying in {retry_state.next_action.sleep} seconds…"),
)
def _request(url, **kwargs):
    """
    Wrapper for verifying and retrying GET requests.
    """
    kwargs.setdefault('headers', HEADERS)
    response = scraper.get(url, **kwargs)

    # handle Cloudflare errors
    # We don't check the reponse content here; it could be large binary data and slow things down.
    if response.status_code == 403:
        # TODO: reset scraper for the next try?
        raise cloudscraper.exceptions.CloudflareChallengeError()

    response.raise_for_status()  # handle other errors
    return response


def _api_request(endpoint, params=None):
    """
    Wrapper for verifying and retrying GET requests to the Blinkist API.
    Returns the parsed JSON response.
    Calls `_request` internally.
    """
    url = f"{BASE_URL}api/{endpoint}"
    response = _request(url, params=params, headers=HEADERS)
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
        console.print(f"Skipping existing file: {file_path}")
        return

    assert 'm4a' in chapter_data['signed_audio_url']
    response = _request(chapter_data['signed_audio_url'])
    assert response.status_code == 200
    file_path.write_bytes(response.content)


def download_book_cover(book):
    # find the URL of the largest version
    urls = set()
    for source in book['image']['sources']:
        urls.add(source['src'])
        urls |= set(source['srcset'].values())
    # example: 'https://images.blinkist.io/images/books/617be9b56cee07000723559e/1_1/470.jpg' → 470
    url = sorted(urls, key=lambda x: int(x.split('/')[-1].rstrip('.jpg')), reverse=True)[0]

    book_dir = get_book_dir(book)
    book_dir.mkdir(exist_ok=True)
    file_path = book_dir / "cover.jpg"

    if file_path.exists():
        console.print(f"Skipping existing file: {file_path}")
        return

    assert url.endswith('.jpg')
    response = _request(url)
    assert response.status_code == 200
    file_path.write_bytes(response.content)


for locale in LOCALES:
    with console.status(f"Retrieving free daily in {locale}…"):
        free_daily = get_free_daily(locale=locale)
    book = free_daily['book']
    console.print(f"Today's free daily in {locale} is: “{book['title']}”")

    # list of chapters without their content
    with console.status(f"Retrieving chapters of {book['title']}…"):
        chapter_list = get_chapters(book['slug'])

    # fetch chapter content
    chapters = [get_chapter(book['id'], chapter['id'])
                for chapter in track(chapter_list, description='Fetching chapters…')]

    # download audio
    for chapter in track(chapters, description='Downloading audio…'):
        download_chapter_audio(book, chapter)

    # download cover
    with console.status(f"Downloading cover…"):
        download_book_cover(book)
