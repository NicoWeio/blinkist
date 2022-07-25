from pathlib import Path

BASE_URL = 'https://www.blinkist.com/'

HEADERS = {
    'x-requested-with': 'XMLHttpRequest',
}

CLOUDFLARE_MAX_ATTEMPTS = 10
CLOUDFLARE_WAIT_TIME = 2

LOCALES = ['en', 'de']
DOWNLOAD_DIR = Path.home() / 'Musik' / 'Blinkist'
