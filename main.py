#!/usr/bin/env python3
from datetime import datetime

from rich.progress import track

from blinkist.blinkist import get_free_daily
from blinkist.chapter import Chapter
from blinkist.config import DOWNLOAD_DIR, LOCALES
from blinkist.console import console

for locale in LOCALES:
    with console.status(f"Retrieving free daily in {locale}…"):
        book = get_free_daily(locale=locale)
    console.print(f"Today's free daily in {locale} is: “{book.title}”")

    # setup book directory
    book_dir = DOWNLOAD_DIR / f"{datetime.today().strftime('%Y-%m-%d')} – {book.slug}"
    book_dir.mkdir(exist_ok=True)

    # list of chapters without their content
    with console.status("Retrieving list of chapters…"):
        chapter_list = book.get_chapter_list()

    # fetch chapter content
    chapters = [
        Chapter.from_id(book, chapter['id'])
        for chapter in track(chapter_list, description='Fetching chapters…')
    ]

    # download audio
    for chapter in track(chapters, description='Downloading audio…'):
        chapter.download_audio(book_dir)

    # download cover
    with console.status("Downloading cover…"):
        book.download_cover(book_dir)
