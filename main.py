#!/usr/bin/env python3
from datetime import datetime
from pathlib import Path

import click
from rich.progress import track

from blinkist.blinkist import get_free_daily
from blinkist.config import LOCALES
from blinkist.console import console


def download_freedaily(
    locale: str,
    library_dir: Path,
    yaml: bool = True,
    markdown: bool = True,
    audio: bool = True,
    cover: bool = True,
):
    # check library directory
    # This comes first so we can fail early if the path doesn't exist.
    assert library_dir.exists()

    with console.status(f"Retrieving free daily in {locale}…"):
        book = get_free_daily(locale=locale)
    console.print(f"Today's free daily in {locale} is: “{book.title}”")

    # setup book directory
    book_dir = library_dir / f"{datetime.today().strftime('%Y-%m-%d')} – {book.slug}"
    book_dir.mkdir(exist_ok=True)  # We don't make parents in order to avoid user error.

    # prefetch chapter_list and chapters for nicer progress info
    with console.status("Retrieving list of chapters…"):
        _ = book.chapter_list
    # this displays a progress bar itself ↓
    _ = book.chapters

    # download raw (YAML)
    # This comes first so we have all information saved as early as possible.
    if yaml:
        with console.status("Downloading raw YAML…"):
            book.download_raw_yaml(book_dir)

    # download text (Markdown)
    if markdown:
        with console.status("Downloading text…"):
            book.download_text_md(book_dir)

    # download audio
    if audio:
        for chapter in track(book.chapters, description='Downloading audio…'):
            chapter.download_audio(book_dir)

    # download cover
    if cover:
        with console.status("Downloading cover…"):
            book.download_cover(book_dir)


@click.command()
@click.argument('library_dir', type=click.Path(exists=True, dir_okay=True, writable=True, path_type=Path))
@click.option('--locale', '-l', help="Locale to download free daily in. Defaults to all locales.", type=click.Choice(LOCALES), default=None)
@click.option('--yaml/--no-yaml', help="Save content as YAML", default=True)
@click.option('--markdown/--no-markdown', help="Save content as Markdown", default=True)
@click.option('--audio/--no-audio', help="Download audio", default=True)
@click.option('--cover/--no-cover', help="Download cover", default=True)
def main(locale, library_dir, **kwargs):
    for locale_ in ([locale] if locale else LOCALES):
        download_freedaily(locale_, library_dir, **kwargs)


if __name__ == '__main__':
    main()
