import cloudscraper
import tenacity

from .config import CLOUDFLARE_MAX_ATTEMPTS, CLOUDFLARE_WAIT_TIME, HEADERS
from .console import console

scraper = cloudscraper.create_scraper()


@tenacity.retry(
    retry=tenacity.retry_if_exception_type(cloudscraper.exceptions.CloudflareChallengeError),
    wait=tenacity.wait_fixed(CLOUDFLARE_WAIT_TIME),
    stop=tenacity.stop_after_attempt(CLOUDFLARE_MAX_ATTEMPTS),
    before_sleep=lambda retry_state: console.print(f"Retrying in {retry_state.next_action.sleep} seconds…"),
)
def request(url, **kwargs):
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
