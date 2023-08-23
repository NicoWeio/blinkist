# About this repository

## Features
### File formats
This program downloads books from Blinkist.
To be precise, it saves…
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

### Book selection
- `--book-slug`: the book slug (e.g. `get-smart-en`)
  - ⚠️ As of writing, no authentication is required to access _any_ book, a benefit which _should_ require a subscription _in theory_. Do consider the legal and moral implications of using this.
- `--freedaily`: Each day, Blinkist offers a free book for each locale.
  - [Website (en)](https://www.blinkist.com/en/content/daily)
- Further options include `--book-slug`, `--latest`, `--latest-collections`, `--search`, and `--trending`. Refer to `main.py --help` for more information.
- 🛈 If you pass multiple of these options, all of them will be used.

## Installation

```bash
# First, clone the repository

# Then, install the dependencies
$ pip install -r requirements.txt
```

Installation via _setuptools_ and _pip_ is currently not supported.
Python ≥3.9 is recommended.

## Usage
Just run the [`main.py`](main.py) executable, stating what to download and providing a path to a “library directory”, where every book will be saved in its own subdirectory.
Here's an example:
```bash
$ ./main.py --freedaily ~/Library/Blinkist
```
For an overview of all CLI options, see `main.py --help`.
For other options, you need to modify [`blinkist/config.py`](blinkist/config.py) to your needs.


## Motivation
While https://github.com/ptrstn/dailyblink is/was broken due to changes to Blinkist's frontend (https://github.com/ptrstn/dailyblink/issues/32),
I wrote my own Blinkist downloader from scratch.
In contrast to the original, this one relies on Blinkist's API, which might be more stable than scraping with *beautifulsoup*.
Now, some aspects are even better than in the original, while others are sill lacking.

## Limitations
- Downloading arbitrary books with Blinkist Premium is not supported out of the box. It might be easy to get it working, but I didn't test it. There's other tools for that anyway.
- ID3 tags are not set.
- The formatting of the markdown export differs a little from @ptrstn's.
- Occasionaly, Cloudflare gets in the way.
[[1]](https://github.com/ptrstn/dailyblink/issues/32#issuecomment-1155508522)
[[2]](https://github.com/NicoWeio/blinkist/issues/1)

## Comparison
- https://github.com/ptrstn/dailyblink
  - 🏅 inspiration for this project
  - (👎) relies on web scraping (using BeautifulSoup4) [¹](https://github.com/ptrstn/dailyblink/blob/master/dailyblink/core.py)
  - 👎 last commit was in 2021
  - 👎 currently (at least partially) [broken](https://github.com/ptrstn/dailyblink/issues/32)
- https://github.com/leoncvlt/blinkist-scraper
  - 👍 more features
    - categories
    - formats: HTML, EPUB, PDF
    - embedding of cover art into concatenated audio file
  - (👎) relies on a mixture of web scraping (using Selenium) and API requests [¹](https://github.com/leoncvlt/blinkist-scraper/blob/master/blinkistscraper/scraper.py)
  - 👎 relies on ChromeDriver (larger resource footprint)
  - 👎 last commit was in 2021
- https://github.com/rajeshbhavikatti/daily_blink_to_notion
  - borrows some of my code 😇
  - 👎 very specific use case
- https://github.com/luckylittle/blinkist-m4a-downloader
  - written in Go
  - (👎) relies on web scraping (using [colly](https://github.com/gocolly/colly)) [¹](https://github.com/luckylittle/blinkist-m4a-downloader/blob/master/download/download.go)
- https://github.com/orgarafatm/blinkist
  - (👎) relies on web scraping (using BeautifulSoup4) [¹](https://github.com/orgarafatm/blinkist/blob/master/blinkist_daily_scraper.py)
  - 👎 contains scraped content

> - https://github.com/karlicoss/blinkist-backup
>   - only downloads highlights and the library booklist

## Example data
🛈 Also check out the auto-generated [Swagger API documentation](https://nicoweio.github.io/blinkist/).

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

<details>
<summary>
    https://api.blinkist.com/contentaccess/free_items
</summary>

```json
{
  "items": [
    {
      "item_type": "curated_list",
      "item_id": "f8a49868-a6f3-40fd-b264-2348770c6815"
    },
    {
      "item_type": "book",
      "item_id": "52bec76a3933330008000000"
    },
    {
      "item_type": "episode",
      "item_id": "1055"
    },
    …
  ]
}
```
</details>


<details>
<summary>
    https://api.blinkist.com/content/curated_lists/f8a49868-a6f3-40fd-b264-2348770c6815
</summary>

```json
{
  "curated_list": {
    "id": "1495",
    "position": -1,
    "uuid": "f8a49868-a6f3-40fd-b264-2348770c6815",
    "slug": "how-to-lead-a-team-you-didn-t-hire",
    "title": "How To Lead A Team You Didn't Hire",
    "description": "The Great Resignation has caused many leaders to pursue new roles, often taking charge of pre-existing departments and teams. Starting a new position can be its own steep learning curve, but the margin for error is even smaller when you are managing a team you didn’t hire. How do you earn this team’s respect and make accurate assessments of its current challenges without the context of someone who built it from the ground up? The following two Blinks and two Shortcasts investigate what it means to be a great leader under these circumstances.",
    "short_description": "Four free Blinks and Shortcasts full of tips on how to be a great leader. ",
    "curator_name": "Sally Page",
    "curator_id": "blinkist",
    "etag": 1658845113,
    "language": "en",
    "discoverable": false,
    "published_at": "2022-07-26T14:18:33.000Z",
    "deleted_at": null,
    "kind": "collection",
    "styling": {
      "main_color": null,
      "accent_color": null,
      "text_color": null,
      "text_on_accent_color": null
    },
    "content_items": [
      {
        "id": "14380",
        "position": 1,
        "content_item_type": "book",
        "content_item_id": "52bec76a3933330008000000",
        "description": ""
      },
      {
        "id": "14381",
        "position": 2,
        "content_item_type": "book",
        "content_item_id": "52f1195c35653600110b0000",
        "description": ""
      },
      {
        "id": "14382",
        "position": 3,
        "content_item_type": "episode",
        "content_item_id": "1055",
        "description": ""
      },
      {
        "id": "14383",
        "position": 4,
        "content_item_type": "episode",
        "content_item_id": "1000",
        "description": ""
      }
    ]
  }
}
```
</details>


<!--
<details>
<summary>
    URL
</summary>

```json
DATA
```
</details>
-->

<!-- `https://www.blinkist.com/api/mickey_mouse/setup?…` -->
