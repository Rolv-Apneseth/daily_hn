from bs4 import BeautifulSoup
import requests


def get_soup(link):
    """Gets soup from a given website."""

    res = requests.get(link)
    soup = BeautifulSoup(res.text, "html.parser")
    return soup


def get_links(soup):
    """Gets the story links from the given hacker news soup."""

    links = soup.select(".storylink")
    return links


def add_links(links, soup):
    """Adds links to the existing links variable, used for scraping pages 2 and 3 of hacker news"""

    links += soup.select(".storylink")
    return links


def get_subtext(soup):
    """Gets the subtext links from the given hacker news soup."""

    subtext = soup.select(".subtext")
    return subtext


def add_subtext(subtext, soup):
    """Adds subtext to the existing subtext variable, used for scraping pages 2 and 3 of hacker news"""

    subtext += soup.select(".subtext")
    return subtext


def fix_item_link(href):
    """
    Fixes links which point to specific items in the hacker news
    website itself, as they just point to specific pages on the site.
    """

    return "https://news.ycombinator.com/" + href


def clean(links, subtext):
    """
    Organises the links and subtext lists given from the soup into a list of dictionaries which display title,
    link and votes to each article, if the article has more than 150 votes, then returns this list.
    """

    hn = []
    for inx, _ in enumerate(links):
        vote = subtext[inx].select(".score")
        title = links[inx].getText()
        href = links[inx].get("href", None)

        # Fix link if it needs fixing
        if not href.startswith("http"):
            href = fix_item_link(href)

        # If statement in case article has not yet received any votes so does not have a vote category
        if len(vote):
            points = int(vote[0].getText().replace(" points", ""))
            # Change 100 to a lower number if you want to see more articles
            if points > 100:
                hn.append({"title": title, "link": href, "score": points})

    return hn


def sort_by_points(hn_list):
    """Sorts the given list of dictionaries by the score category."""

    # reversed so that the list is in descending order
    return sorted(hn_list, key=lambda x: x["score"], reverse=True)


def print_articles(sorted_list):
    """Prints the sorted list of dictionaries neatly to the console"""

    for dictionary in sorted_list:
        title, link, score = dictionary.values()

        print(f"\n\nTitle: {title}\nScore: {score}\nLink: {link}")


def main():
    # Get links and subtext from page 1 of hacker news
    soup = get_soup("https://news.ycombinator.com/news")
    links = get_links(soup)
    subtext = get_subtext(soup)
    # Add links and subtext from pages 2 and 3 of hacker news
    for link in [
        "https://news.ycombinator.com/news?p=2",
        "https://news.ycombinator.com/news?p=3",
    ]:
        soup = get_soup(link)
        add_links(links, soup)
        add_subtext(subtext, soup)

    print_articles(sort_by_points(clean(links, subtext)))


if __name__ == "__main__":
    main()
