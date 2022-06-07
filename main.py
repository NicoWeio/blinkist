import cloudscraper
from pathlib import Path
import requests
from rich import print

BASE_URL = 'https://www.blinkist.com/'

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:101.0) Gecko/20100101 Firefox/101.0',
    'x-requested-with': 'XMLHttpRequest',
}

DOWNLOAD_DIR = Path.home() / 'Musik' / 'Blinkist'

scraper = cloudscraper.create_scraper()


def get_free_daily(locale):
    # see also: https://www.blinkist.com/en/content/daily
    response = scraper.get(
        BASE_URL + 'api/free_daily',
        params={'locale': locale}
    )
    return response.json()


# auth ↓
# auth_req = scraper.get(
#     'https://www.blinkist.com/api/mickey_mouse/setup?pathname=/en/nc/new-reader/the-4-stages-of-psychological-safety-en&search=&locale=en')
# print(auth_req.json())


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


def download_chapter(chapter_data):
    assert 'm4a' in chapter_data['signed_audio_url']
    response = scraper.get(chapter_data['signed_audio_url'])
    assert response.status_code == 200

    file_path = DOWNLOAD_DIR / f"chapter_{chapter_data['order_no']}.m4a"
    file_path.write_bytes(response.content)
    print(f"Downloaded chapter {chapter_data['order_no']}")


free_daily = get_free_daily(locale='en')
book = free_daily['book']
print("Today's free daily is:", book['title'])

chapters = get_chapters(book['slug'])
print(
    f"{len(chapters)} chapters:",
    ', '.join([c['action_title'] for c in chapters]),
)

for chapter in chapters:
    print(chapter['action_title'])
    chapter_data = get_chapter(book['id'], chapter['id'])
    print(chapter_data['text'])
    print(chapter_data['signed_audio_url'])
    download_chapter(chapter_data)
    print()
