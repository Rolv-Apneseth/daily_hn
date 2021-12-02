from bs4 import BeautifulSoup
import requests


BASE_URL = "https://news.ycombinator.com/"
BEST_STORIES_URL = f"{BASE_URL}best"
SCORE_SELECTOR = ".score"
TITLES_SELECTOR = ".titlelink"


def _get_soup(link):
    """Gets soup from a given website."""

    res = requests.get(link)
    return BeautifulSoup(res.text, "html.parser")


def _get_titles(soup):
    """Gets story title elements from the given hacker news soup."""

    return soup.select(TITLES_SELECTOR)


def _get_scores(soup):
    """Gets subtext elements from the given hacker news soup."""

    return soup.select(SCORE_SELECTOR)


def _fix_item_link(href):
    """
    Fixes links which point to specific items in the hacker news
    website itself, as they just point to specific pages on the site.
    """

    return f"{BASE_URL}{href}"


def get_stories():
    """Returns a list of dictionaries representing stories."""

    soup = _get_soup(BEST_STORIES_URL)

    titles = _get_titles(soup)
    scores = _get_scores(soup)

    return [
        {
            "headline": title.get_text(),
            "link": title["href"]
            if title["href"].startswith("http")
            else _fix_item_link((title["href"])),
            "score": score.getText().replace(" points", ""),
        }
        for title, score in zip(titles, scores)
    ]


def print_articles():
    """Simple print of articles to the screen."""

    stories = get_stories()

    for i, story in enumerate(reversed(stories)):
        print(
            f"\n\n{30-i}. {story.get('headline')}"
            f"\nScore: {story.get('score')}"
            f"\nLink: {story.get('link')}"
        )
