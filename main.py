from bs4 import BeautifulSoup
import requests


BASE_URL = "https://news.ycombinator.com/"
BEST_STORIES_URL = f"{BASE_URL}best"
SCORE_SELECTOR = ".score"
TITLES_SELECTOR = ".titlelink"

# STYLLING
RESET = "\033[0m"
BOLD = "\033[1m"


def get_soup(link):
    """Gets soup from a given website."""

    res = requests.get(link)
    return BeautifulSoup(res.text, "html.parser")


def get_titles(soup):
    """Gets story title elements from the given hacker news soup."""

    return soup.select(TITLES_SELECTOR)


def get_scores(soup):
    """Gets subtext elements from the given hacker news soup."""

    return soup.select(SCORE_SELECTOR)


def fix_item_link(href):
    """
    Fixes links which point to specific items in the hacker news
    website itself, as they just point to specific pages on the site.
    """

    return f"{BASE_URL}href"


def get_stories(soup):
    """Returns a list of dictionaries representing stories."""

    titles = get_titles(soup)
    scores = get_scores(soup)

    return [
        {
            "headline": title.get_text(),
            "link": title["href"],
            "score": score.getText().replace(" points", ""),
        }
        for title, score in zip(titles, scores)
    ]


def _print_articles(stories: dict):
    """Prints the reversed list of dictionaries neatly to the console"""

    for i, story in enumerate(reversed(stories)):
        print(
            f"\n\n{BOLD}{30 - i}.{story.get('headline')}"
            f"\nScore:{RESET} {story.get('score')}"
            f"\n{BOLD}Link:{RESET} {story.get('link')}"
        )


def main():
    soup = get_soup(BEST_STORIES_URL)
    stories = get_stories(soup)

    _print_articles(stories)


if __name__ == "__main__":
    main()
