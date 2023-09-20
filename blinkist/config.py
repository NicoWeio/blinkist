BASE_URL = 'https://www.blinkist.com/'

HEADERS = {
    'x-requested-with': 'XMLHttpRequest',
}

HEADERS_ALGOLIA = {
    'x-algolia-api-key': '1a09a41ec4e8624c821ac861d8fa8fe1',
    'x-algolia-application-id': 'P3SCZPAH8S',
}

CLOUDFLARE_MAX_ATTEMPTS = 10
CLOUDFLARE_WAIT_TIME = 2

LANGUAGES = ['en', 'de']

# Default names for downloaded files if --name-format is not specified.
DEFAULT_FILENAME_COVER = "cover"
DEFAULT_FILENAME_TEXT = "book"
DEFAULT_FILENAME_RAW = "book"
