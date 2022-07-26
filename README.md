# About this repository

## Features
This program downloads Blinkist's “free daily” in all available languages.
It saves…
- the (almost) raw API responses
  - as YAML
  - This includes things like categories or ratings which are not saved elsewhere.
- the text version
  - as Markdown
    - the unmodified HTML-formatted content + custom Markdown-formatted structure
    - 🛈 Consider using [Pandoc](https://pandoc.org/) to convert to other formats like HTML, PDF, EPUB, etc.
- the audio version
  - as one M4A file per chapter (no modifications)
- the cover image
  - as JPEG (no modifications)
  - in the highest resolution available (1080×1080)

## Installation

```bash
# First, clone the repository

# Then, install the dependencies
$ pip install -r requirements.txt
```

Installation via _setuptools_ and _pip_ is currently not supported.

## Usage
Just run the [`main.py`](main.py) executable, providing a path to a “library directory”, where every book will be saved in its own subdirectory:
```bash
$ python main.py ~/Library/Blinkist
```
Some CLI options are available; see `main.py --help`.
For other options, you need to modify [`blinkist/config.py`](blinkist/config.py) to your needs.


## Motivation
While https://github.com/ptrstn/dailyblink is/was broken due to changes to Blinkist's frontend (https://github.com/ptrstn/dailyblink/issues/32),
I wrote my own Blinkist downloader from scratch.
In contrast to the original, this one relies on Blinkist's API, which might be more stable than scraping with *beautifulsoup*.

## Limitations
- Downloading arbitrary books with Blinkist Premium is not supported out of the box. It might be easy to get it working, but I didn't test it. There's other tools for that anyway.
- ID3 tags are not set.
- The formatting of the markdown export differs a little from @ptrstn's.
- Apparently, this doesn't work for everyone. [[1]](https://github.com/ptrstn/dailyblink/issues/32#issuecomment-1155508522)

## Example data
<details>
<summary>
    https://www.blinkist.com/api/free_daily
</summary>

```json
{
    "book": {
        "id": "628223936cee0700089119c9",
        "kind": "book",
        "slug": "the-4-stages-of-psychological-safety-en",
        "title": "The 4 Stages of Psychological Safety",
        "subtitle": "Defining the Path to Inclusion and Innovation",
        "subtitleHtmlSafe": "Defining the Path to Inclusion and Innovation",
        "aboutTheBook": "<p><em>The 4 Stages of Psychological Safety </em>(2020) is a practical handbook for creating and maintaining psychological safety in the workplace. In order for employees to take risks, ask questions, challenge the status quo, and make mistakes –&nbsp;all while learning and growing –&nbsp;they have to feel included and safe. This book shows how leaders can reduce social friction while encouraging collaboration and innovation.</p>",
        "buyOnAmazonUrl": "/en/books/the-4-stages-of-psychological-safety-en/purchase",
        "author": "Timothy R. Clark",
        "truncatedAuthor": "Timothy R. Clark",
        "sourceAuthor": "Timothy R. Clark",
        "url": "/en/books/the-4-stages-of-psychological-safety-en",
        "browseUrl": "/en/nc/browse/books/the-4-stages-of-psychological-safety-en",
        "previewUrl": "/en/books/the-4-stages-of-psychological-safety-en",
        "readingDuration": 9,
        "minutesToRead": 9,
        "isAudio": true,
        "readCount": null,
        "image": {
            "default": {
                "src": "https://images.blinkist.io/images/books/628223936cee0700089119c9/1_1/470.jpg",
                "srcset": {
                    "2x": "https://images.blinkist.io/images/books/628223936cee0700089119c9/1_1/640.jpg"
                }
            },
            "sources": [
                {
                    "media": "xs",
                    "src": "https://images.blinkist.io/images/books/628223936cee0700089119c9/1_1/470.jpg",
                    "srcset": {
                        "2x": "https://images.blinkist.io/images/books/628223936cee0700089119c9/1_1/640.jpg"
                    }
                },
                {
                    "media": "s",
                    "src": "https://images.blinkist.io/images/books/628223936cee0700089119c9/1_1/640.jpg",
                    "srcset": {
                        "2x": "https://images.blinkist.io/images/books/628223936cee0700089119c9/1_1/1080.jpg"
                    }
                },
                {
                    "media": "m",
                    "src": "https://images.blinkist.io/images/books/628223936cee0700089119c9/1_1/250.jpg",
                    "srcset": {
                        "2x": "https://images.blinkist.io/images/books/628223936cee0700089119c9/1_1/470.jpg"
                    }
                }
            ]
        },
        "audioUrl": "https://hls.blinkist.io/bibs/628223936cee0700089119c9/628223936cee0700089119cb-T1652696046.m4a?Expires=1654617121&Signature=VuyioBHQEDE~ExCpKbib9rBYzjtxsls3EQo6ZCLN0fY~GaFiU9Cb1pV5Xzo1-4Xdef8IlRMWHXZdLFtAOpmmWqcnC2z8ySekv8wFrSmZcPxbQGdi-AstNtVMzTRQVKniy6Kx3Xc2lCswJdnwP0j3okC4Z~ijkcEn91EqTHZhtpEwkBjPEg2hX433tKnc1yFHU4DQpcbe6977fuaCyKZZjXRL4jYXRhRXgvMcqLs8ST3cS49lfzuqfG1kSJxBo7PJ~mvT9HsrSH91aEHW2XBtgfoiwrNVdxQBm9gGSHNoVun0kJa8DABagDRMdFHkr0~pF7XPfrNJGGO6DhIUVNdCmw__&Key-Pair-Id=APKAJXJM6BB7FFZXUB4A",
        "chaptersLength": 5,
        "hasAudio": true,
        "language": "en",
        "freeDaily": null,
        "category": {
            "title": "Management & Leadership",
            "sprite": "management-and-leadership",
            "slug": "management-and-leadership-en"
        },
        "averageRating": 4.2,
        "categories": [
            {
                "id": "54788e1066333100094b0000",
                "url": "/en/nc/categories/management-and-leadership-en",
                "sprite": "management-and-leadership",
                "slug": "management-and-leadership-en",
                "title": "Management & Leadership",
                "subtitle": "Every great leader has unique secrets to success, but what’s one they all agree on? Books! Read up, step up, and shine."
            },
            {
                "id": "5b868435b238e1000726ccba",
                "url": "/en/nc/categories/career-and-success-en",
                "sprite": "career-and-success",
                "slug": "career-and-success-en",
                "title": "Career & Success",
                "subtitle": "With these titles, climbing the job ladder will be as easy as 1-2-3."
            }
        ]
    },
    "endTimestamp": 1654639199
}
```
</details>

<details>
<summary>
    https://www.blinkist.com/api/books/{book_slug}/chapters
</summary>

```json
{
   "book":{…},
   "chapters":[
      {
         "id":"628223936cee0700089119ca",
         "order_no":0,
         "action_title":"What’s in it for me? Learn how to encourage innovation through inclusion in your team or organization."
      },
      {
         "id":"628223936cee0700089119cb",
         "order_no":1,
         "action_title":"To create inclusion safety, make sure team members feel unconditionally included from the very beginning."
      },
      {
         "id":"628223936cee0700089119cc",
         "order_no":2,
         "action_title":"To provide learner safety, create an environment where failure isn’t just accepted – it’s rewarded."
      },
      {
         "id":"628223936cee0700089119cd",
         "order_no":3,
         "action_title":"To provide contributor safety, get to know your team, limit your tell-to-ask ratio, and help colleagues think beyond their roles."
      },
      {
         "id":"628223936cee0700089119ce",
         "order_no":4,
         "action_title":"Democratize innovation by fostering challenger safety."
      },
      {
         "id":"628223936cee0700089119cf",
         "order_no":5,
         "action_title":"Final summary"
      }
   ],
   "current_chapter_id":"None"
}
```
</details>

<details>
<summary>
    https://www.blinkist.com/api/books/{book_id}/chapters/{chapter_id}
</summary>

```json
{
   "id":"628223936cee0700089119ca",
   "order_no":0,
   "action_title":"What’s in it for me? Learn how to encourage innovation through inclusion in your team or organization.",
   "text":"<p>Congrats! You’re in the luxurious position of choosing between two teams you could work with. Let’s go ahead and meet them.</p>\\n<p>\\n </p>\\n<p>This is the first team’s office. Notice that? The air is stiff. [shortened as to not violate their copyright]</p>",
   "audio_url":"https://hls.blinkist.io/bibs/628223936cee0700089119c9/628223936cee0700089119ca-T1652696046.m4a",
   "signed_audio_url":"https://hls.blinkist.io/bibs/628223936cee0700089119c9/628223936cee0700089119ca-T1652696046.m4a?Expires=1654621635&Signature=PFcksN0ISh~J6YjzWQKsJYaQUbmW0Cl~ct4qtiIsfDPxrXjyYxorafH~TdCP4bYsjSuuOeDp1BCEkLtO0HWm3EsLc1T5Cv7LRIS7yuuHpR6GK~72DjKDQBPGWx4JZsWv0Au1VegwfYHEU4sFaz9VvahcJg5u3~FufSEhgygTC3SOGpgfsRTIAOfkvXPhet-d~8u0KAHZudHHkBEVl1w804abVfW-30uvxyuSBBViTkI7r74RyJt~ui42mMO8s314vz6wdMNSgLmF-blKDwU0xXTnskIdSOHI~PS6TT4PEQS~pf1KfsUDLrhr8P61TzUHkCZtricCD1udzRLjYLpEzA__&Key-Pair-Id=APKAJXJM6BB7FFZXUB4A"
}
```
</details>

<!-- `https://www.blinkist.com/api/mickey_mouse/setup?…` -->
