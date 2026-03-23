import logging
from pathlib import Path

import tenacity

from .config import CLOUDFLARE_MAX_ATTEMPTS, CLOUDFLARE_WAIT_TIME, HEADERS
from .console import track

try:
    from curl_cffi import requests as curl_requests
    _USE_CURL_CFFI = True
except ImportError:
    import cloudscraper
    _USE_CURL_CFFI = False


class CloudflareChallengeError(Exception):
    pass


if _USE_CURL_CFFI:
    scraper = curl_requests.Session(impersonate="chrome")
else:
    scraper = cloudscraper.create_scraper()


@tenacity.retry(
    retry=tenacity.retry_if_exception_type(CloudflareChallengeError),
    wait=tenacity.wait_fixed(CLOUDFLARE_WAIT_TIME),
    stop=tenacity.stop_after_attempt(CLOUDFLARE_MAX_ATTEMPTS),
    before_sleep=lambda retry_state: logging.info(f"Retrying in {retry_state.next_action.sleep} seconds…"),
)
def request(url, **kwargs):
    """
    Wrapper for verifying and retrying GET requests.
    """
    kwargs.setdefault('headers', HEADERS)
    if _USE_CURL_CFFI:
        stream = kwargs.pop('stream', False)
        response = scraper.get(url, stream=stream, **kwargs)
    else:
        response = scraper.get(url, **kwargs)

    if response.status_code == 403:
        raise CloudflareChallengeError()

    response.raise_for_status()
    return response


def api_request(base_url: str, endpoint: str, params=None):
    """
    Wrapper for verifying and retrying GET requests to the Blinkist API.
    Returns the parsed JSON response.
    Calls `request` internally.
    """
    url = base_url + endpoint
    response = request(url, params=params, headers=HEADERS)
    return response.json()


def api_request_web(endpoint: str, params=None):
    """
    Wrapper for verifying and retrying GET requests to the Blinkist web API (https://blinkist.com/api/).
    Returns the parsed JSON response.
    """
    return api_request('https://blinkist.com/api/', endpoint, params=params)


def api_request_app(endpoint: str, params=None):
    """
    Wrapper for verifying and retrying GET requests to the Blinkist app API (https://api.blinkist.com/).
    Returns the parsed JSON response.
    """
    return api_request('https://api.blinkist.com/', endpoint, params=params)


def download(url: str, file_path: Path):
    """
    Downloads a file from the given URL to the given path
    and shows a progress bar!
    """
    # adapted from https://stackoverflow.com/a/15645088
    with open(file_path, 'wb') as f:
        response = request(url, stream=True)
        assert response.status_code == 200
        total_length = response.headers.get('content-length')

        if total_length is None:
            f.write(response.content)
        else:
            for data in track(
                # FIXME: The displayed numbers won't be easily interpretable.
                response.iter_content(chunk_size=4096),
                total=int(total_length) // 4096,
                description="Downloading…",
            ):
                f.write(data)
