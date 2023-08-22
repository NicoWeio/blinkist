#!/usr/bin/env python3
import logging
from pathlib import Path

import click
from rich.logging import RichHandler

from blinkist.blinkist import (get_free_daily, get_latest_collections,
                               get_trending_books, search_books)
from blinkist.book import Book  # typing only
from blinkist.config import LANGUAGES
from blinkist.console import console, status, track, track_context

logging.basicConfig(
    level=logging.DEBUG,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler()],
)
logging.getLogger('urllib3').setLevel(logging.WARNING)


def download_book(
    book: Book,
    language: str,
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

    # setup book directory
    # book_dir = library_dir / f"{datetime.today().strftime('%Y-%m-%d')} – {book.slug}"
    book_dir = library_dir / book.slug
    if book_dir.exists() and not redownload:
        logging.info(f"Skipping “{book.title}” – already downloaded.")
        # TODO: this doss not check if the download was complete! Can we do something about that
        return
    book_dir.mkdir(exist_ok=True)  # We don't make parents in order to avoid user error.

    try:
        # prefetch chapter_list and chapters for nicer progress info
        with status("Retrieving list of chapters…"):
            _ = book.chapter_list
        # this displays a progress bar itself ↓
        _ = book.chapters

        # download raw (YAML)
        # This comes first so we have all information saved as early as possible.
        if yaml:
            with status("Downloading raw YAML…"):
                book.download_raw_yaml(book_dir)

        # download text (Markdown)
        if markdown:
            with status("Downloading text…"):
                book.download_text_md(book_dir)

        # download audio
        if audio:
            if book.is_audio:
                for chapter in track(book.chapters, description="Downloading audio…"):
                    chapter.download_audio(book_dir)
            else:
                logging.warning("This book has no audio.")

        # download cover
        if cover:
            with status("Downloading cover…"):
                book.download_cover(book_dir)
    except Exception as e:
        logging.error(f"Error downloading “{book.title}”: {e}")

        error_dir = book_dir.parent / f"{book.slug} – ERROR"
        i = 0
        while error_dir.exists() and any(error_dir.iterdir()):
            i += 1
            error_dir = book_dir.parent / f"{book.slug} – ERROR ({i})"

        book_dir.replace(target=error_dir)
        logging.warning(f"Renamed output directory to “{error_dir.relative_to(book_dir.parent)}”")

        if continue_on_error:
            logging.info("Continuing with next book… (--continue-on-error was set)")
        else:
            logging.critical("Exiting…")
            logging.critical("Hint: Try using --continue-on-error.")
            raise


@click.command()
# ▒ arguments ↓
@click.argument('library_dir', type=click.Path(exists=True, dir_okay=True, writable=True, path_type=Path))
# ▒ general options ↓
@click.option('--continue-on-error', '-c', help="Continue downloading the next book after an error.", is_flag=True, default=False)
@click.option('--language', '-l', help="Language to download content in. Other languages will be skipped. Defaults to all languages.", type=click.Choice(LANGUAGES), default=None)
# FIXME: Invocations with --no-download shouldn't need the library_dir argument
@click.option('--no-download', '-n', help="Don't actually save anything, just print what would be downloaded.", is_flag=True, default=False)
@click.option('--redownload', '-r', help="Redownload all files, even if they already exist. Otherwise, skip all downloads if the book directory exists. Incomplete downloads won't be completed!", is_flag=True, default=False)
# ▒ what books to download ↓
@click.option('--book-slug', help="Download a book by its slug.", type=str, default=None)
@click.option('--freedaily', help="Download the free daily.", is_flag=True, default=False)
@click.option('--latest-collections', help="Download the latest collections. Limited to 8 results by default; this limit cannot currently be changed.", is_flag=True, default=False)
@click.option('--search', help="Search for books. Limited to 20 results by default. Use --limit to override.", type=str, default=None)
@click.option('--trending', help="Download trending books. Limited to 8 results by default. Use --limit to override.", is_flag=True, default=False)
# ▒▒ meta
@click.option('--limit', help="Limit the number of books to download. Defaults to no limit.", type=int, default=None)
# ▒ file format switches ↓
# ▒▒ raw
@click.option('--audio/--no-audio', help="Download audio", default=True)
@click.option('--cover/--no-cover', help="Download cover", default=True)
@click.option('--yaml/--no-yaml', help="Save content as YAML", default=True)
# ▒▒ processed
@click.option('--markdown/--no-markdown', help="Save content as Markdown", default=True)
def main(**kwargs):
    languages_to_download = [kwargs['language']] if kwargs['language'] else LANGUAGES  # default to all languages
    books_to_download = set()

    if kwargs['book_slug']:
        books_to_download.add(Book.from_slug(kwargs['book_slug']))

    if kwargs['latest_collections']:
        with track_context:
            # NOTE: The `--limit` option is for the number of books, not collections, so we don't pass it here.
            collections = get_latest_collections()
        logging.info(f"Found {len(collections)} collections.")

        with track_context:
            for collection in track(collections, description="Retrieving books from collections…"):
                logging.info(f"Collection: “{collection.title}”")
                books_to_download |= set(collection.books)

    if kwargs['freedaily']:
        for language_ in languages_to_download:
            with console.status(f"Retrieving free daily in {language_}…"):
                book = get_free_daily(locale=language_)
            books_to_download.add(book)

    if kwargs['search']:
        with track_context:
            books_to_download |= set(search_books(
                kwargs['search'],
                languages=(languages_to_download if kwargs['language'] else None),
                limit=kwargs['limit'],
            ))

    if kwargs['trending']:
        with track_context:
            books_to_download |= set(get_trending_books(limit=kwargs['limit']))

    # filter out books in non-selected languages
    books_to_download = [book for book in books_to_download if book.language in languages_to_download]

    # limit number of books to download
    if kwargs['limit']:
        # NOTE: kwargs['limit'] == 0 is silently ignored
        books_to_download = books_to_download[:kwargs['limit']]

    if not books_to_download:
        logging.info("No books to download.")
        logging.info("Hint: Try --freedaily or --freecurated.")
        if kwargs['language']:
            logging.info("Hint: Maybe there were no books in the specified --language?")
        return

    with track_context:
        for book in (
            track(books_to_download, description="Downloading books…")
            if len(books_to_download) > 1
            else books_to_download
        ):
            logging.info(f"Book: “{book.title}”")
            if not kwargs["no_download"]:
                download_book(
                    book=book,
                    **kwargs
                )


if __name__ == '__main__':
    main()
