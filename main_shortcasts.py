#!/usr/bin/env python3
# %%
import logging
from pathlib import Path
from time import sleep

import click
from rich.logging import RichHandler

from blinkist.console import console, status, track, track_context
from blinkist.shortcast import Shortcast, ShortcastEpisode

logging.basicConfig(
    level=logging.DEBUG,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler()],
)
logging.getLogger('urllib3').setLevel(logging.WARNING)

# %%

def download_shortcast_episode(
    shortcast: Shortcast,
    episode: ShortcastEpisode,
    library_dir: Path,
    # ---
    yaml: bool = True,
    markdown: bool = True,
    audio: bool = True,
    cover: bool = True,
    # ---
    redownload: bool = False,
    continue_on_error: bool = False,
    # ---
    **kwargs,
):
    # check library directory
    # This comes first so we can fail early if the path doesn't exist.
    assert library_dir.exists()

    # set up final shortcast directory
    shortcast_dir = library_dir / shortcast.slug
    shortcast_dir.mkdir(exist_ok=True)
    episode_dir = shortcast_dir / f"{episode.number} – {episode.title}"

    if episode_dir.exists() and not redownload:
        logging.info(f"Skipping “{episode.title}” – already downloaded.")
        # TODO: this doss not check if the download was complete! Can we do something about that
        return

    # set up temporary shortcast directory
    episode_tmp_dir = episode_dir.parent / f"{episode_dir.name}.tmp"
    i = 0
    while episode_tmp_dir.exists():
        i += 1
        episode_tmp_dir = episode_dir.parent / f"{episode_dir.name}.tmp{i}"
    episode_tmp_dir.mkdir()  # We don't make parents in order to avoid user error.

    try:
        # download raw (YAML)
        # This comes first so we have all information saved as early as possible.
        if yaml:
            with status("Downloading raw YAML…"):
                episode.download_raw_yaml(episode_tmp_dir)

        # download audio
        if audio:
            episode.download_audio(episode_tmp_dir)

        # download cover
        if cover:
            with status("Downloading cover…"):
                episode.download_cover(episode_tmp_dir)

        # move tmp dir to final dir
        assert not episode_dir.exists()  # in case it was created by another process
        episode_tmp_dir.rename(episode_dir)

    except Exception as e:
        logging.error(f"Error downloading “{episode.title}”: {e}")
        logging.info(f"Keeping temporary output directory “{episode_tmp_dir.name}”")

        if continue_on_error:
            logging.info("Continuing with next episode… (--continue-on-error was set)")
            # TODO: close status stuff…
        else:
            logging.critical("Exiting…")
            logging.critical("Hint: Try using --continue-on-error.")
            raise

# %%

@click.command()
# ▒ arguments ↓
@click.argument('library_dir', type=click.Path(exists=True, dir_okay=True, writable=True, path_type=Path))
# ▒ file format switches ↓
# …
@click.option('--shortcast-slug', help="Download a shortcast by its slug.", type=str, default=None)
# …
# ▒▒ raw
@click.option('--audio/--no-audio', help="Download audio", default=True)
@click.option('--cover/--no-cover', help="Download cover", default=True)
@click.option('--yaml/--no-yaml', help="Save content as YAML", default=True)
def main(**kwargs):
    with track_context:
        shortcast = Shortcast.from_slug_or_uuid(kwargs['shortcast_slug'])

            # # prefetch episodes for nicer progress info
            # with status("Retrieving list of episodes…"):
            #     _ = shortcast.episodes
            # # this displays a progress bar itself ↓
            # _ = shortcast.episodes

        for episode in track(shortcast.episodes, description="Downloading episodes…"):
            download_shortcast_episode(shortcast, episode, kwargs['library_dir'])

# %%
if __name__ == '__main__':
    main()
