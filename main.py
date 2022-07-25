#!/usr/bin/env python3
from datetime import datetime

from rich.progress import track

from blinkist.blinkist import get_free_daily
from blinkist.config import DOWNLOAD_DIR, LOCALES
from blinkist.console import console

for locale in LOCALES:
    with console.status(f"Retrieving free daily in {locale}…"):
        book = get_free_daily(locale=locale)
    console.print(f"Today's free daily in {locale} is: “{book.title}”")

    # setup book directory
    # This comes first so we can fail early if the path doesn't exist.
    book_dir = DOWNLOAD_DIR / f"{datetime.today().strftime('%Y-%m-%d')} – {book.slug}"
    book_dir.mkdir(exist_ok=True)

    # prefetch chapter_list and chapters for nicer progress info
    with console.status("Retrieving list of chapters…"):
        _ = book.chapter_list
    # this displays a progress bar itself ↓
    _ = book.chapters

    # download text (Markdown)
    with console.status("Downloading text…"):
        book.download_text_md(book_dir)

    # download raw (YAML)
    with console.status("Downloading raw YAML…"):
        book.download_raw_yaml(book_dir)

    # download audio
    for chapter in track(book.chapters, description='Downloading audio…'):
        chapter.download_audio(book_dir)

    # download cover
    with console.status("Downloading cover…"):
        book.download_cover(book_dir)
