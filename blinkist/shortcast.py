from functools import cached_property

import yaml

from .config import FILENAME_COVER, FILENAME_RAW
# from .shortcast_episode import ShortcastEpisode
from .console import track


class Shortcast:
    def __init__(self, data):
        self.data = data

        # pylint: disable=C0103
        self.id = data['id']
        self.slug = data['slug']
        self.title = data['title']

    @cached_property
    def episodes(self):
        return [
            ShortcastEpisode.from_id(self, episode['id'])
            for episode in track(self.data['episodes'], description='Fetching episodes…')
            if episode['kind'] == 'episode'
        ]

    @staticmethod
    def from_slug_or_uuid(slug_or_uuid: str) -> 'Shortcast':
        """
        Loads a collection by its slug/UUID.
        """
        return Shortcast(api_request_web(f"shortcasts/{slug_or_uuid}"))

# ---

import logging
from pathlib import Path  # typing only

from .common import api_request_web, download


class ShortcastEpisode:
    def __init__(self, episode_data: dict):
        self.data = episode_data

        # pylint: disable=C0103
        self.id = episode_data['id']
        self.number = episode_data['episodeNumber']
        self.title = episode_data['title']

    @staticmethod
    def from_id(shortcast, episode_id) -> 'ShortcastEpisode':
        episode_data = api_request_web(f'shortcasts/{shortcast.slug}/episodes/{episode_id}')
        return ShortcastEpisode(episode_data)

    def serialize(self) -> dict:
        """
        Serializes the episode to a dict.
        """
        return self.data

    def download_raw_yaml(self, target_dir: Path) -> None:
        """
        Downloads the raw YAML to the given directory.
        """
        file_path = target_dir / f"episode.yaml" # TODO: move to config like FILENAME_RAW
        file_path.write_text(
            yaml.dump(
                self.serialize(),
                default_flow_style=False,
                allow_unicode=True,
            ),
            encoding='utf-8',
        )


    def download_audio(self, target_dir: Path) -> None:
        file_path = target_dir / f"{self.number} – {self.title}.m4a"

        assert 'm4a' in self.data['audio_url']
        download(self.data['audio_url'], file_path)

    def download_cover(self, target_dir: Path) -> None:
        """
        Downloads the cover image to the given directory,
        in the highest resolution available.
        """
        # find the URL of the largest version
        urls = set()
        for source in self.data['image']['sources']:
            urls.add(source['src'])
            urls |= set(source['srcset'].values())
        # FIXME: This is not actually an example for a shortcast episode.
        # example: 'https://images.blinkist.io/images/books/617be9b56cee07000723559e/1_1/470.jpg' → 470
        url = sorted(urls, key=lambda x: int(x.split('/')[-1].rstrip('.jpg')), reverse=True)[0]

        file_path = target_dir / f"{FILENAME_COVER}.jpg"

        assert url.endswith('.jpg')
        download(url, file_path)
