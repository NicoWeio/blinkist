#!/usr/bin/env python3
from pathlib import Path

import click
from rich.progress import track

from blinkist.blinkist import get_free_curated_lists, get_free_daily
from blinkist.book import Book  # typing only
from blinkist.config import LANGUAGES
from blinkist.console import console


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
):
    # check library directory
    # This comes first so we can fail early if the path doesn't exist.
    assert library_dir.exists()

    # setup book directory
    # book_dir = library_dir / f"{datetime.today().strftime('%Y-%m-%d')} – {book.slug}"
    book_dir = library_dir / book.slug
    if book_dir.exists() and not redownload:
        console.print(f"Skipping „{book.title}“ – already downloaded.")
        # TODO: this doss not check if the download was complete! Can we do something about that
        return
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
    if audio and book.is_audio:
        for chapter in track(book.chapters, description='Downloading audio…'):
            chapter.download_audio(book_dir)

    # download cover
    if cover:
        with console.status("Downloading cover…"):
            book.download_cover(book_dir)


@click.command()
# ▒ arguments ↓
@click.argument('library_dir', type=click.Path(exists=True, dir_okay=True, writable=True, path_type=Path))
# ▒ general options ↓
@click.option('--language', '-l', help="Language to download content in. Other languages will be skipped. Defaults to all languages.", type=click.Choice(LANGUAGES), default=None)
@click.option('--redownload', '-r', help="Redownload all files, even if they already exist. Otherwise, skip all downloads if the book directory exists. Incomplete downloads won't be completed!", is_flag=True, default=False)
# ▒ what books to download ↓
@click.option('--book-slug', help="Download a book by its slug.", type=str, default=None)
@click.option('--freedaily', help="Download the free daily.", is_flag=True, default=False)
@click.option('--freecurated', help="Download the free curated list.", is_flag=True, default=False)
# ▒ file format switches ↓
@click.option('--yaml/--no-yaml', help="Save content as YAML", default=True)
@click.option('--markdown/--no-markdown', help="Save content as Markdown", default=True)
@click.option('--audio/--no-audio', help="Download audio", default=True)
@click.option('--cover/--no-cover', help="Download cover", default=True)
def main(book_slug, freedaily, freecurated, language, **kwargs):
    languages_to_download = [language] if language else LANGUAGES  # default to all languages
    books_to_download = set()

    if book_slug:
        books_to_download.add(Book.from_slug(book_slug))

    if freedaily:
        for language_ in languages_to_download:
            with console.status(f"Retrieving free daily in {language_}…"):
                book = get_free_daily(locale=language_)
            books_to_download.add(book)

    if freecurated:
        with console.status("Retrieving free curated lists…"):
            # TODO: Don't just look at curated lists, also look directly at free book items.
            curated_lists = get_free_curated_lists()
        print(f"Found {len(curated_lists)} curated lists.")

        for i, curated_list in enumerate(curated_lists, 1):
            print(f"Curated list ({i}/{len(curated_lists)}): “{curated_list.title}”")
            books_to_download |= set(curated_list.books)

    # filter out books in non-selected languages
    books_to_download = [book for book in books_to_download if book.language in languages_to_download]

    if not books_to_download:
        console.print("No books to download.", "Hint: Try --freedaily or --freecurated.", sep="\n")
        return

    for j, book in enumerate(books_to_download, 1):
        print(f"Book ({j}/{len(books_to_download)}): “{book.title}”")
        download_book(
            book=book,
            language=language,
            **kwargs
        )


if __name__ == '__main__':
    main()
