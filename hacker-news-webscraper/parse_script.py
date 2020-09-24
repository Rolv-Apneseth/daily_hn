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


def clean(links, subtext):
    """
    Organises the links and subtext lists given from the soup into a list of dictionaries which display title,
    link and votes to each article, if the article has more than 150 votes, then returns this list.
    """

    hn = []
    for inx, item in enumerate(links):
        vote = subtext[inx].select(".score")
        title = links[inx].getText()
        href = links[inx].get("href", None)
        #If statement in case article has not yet received any votes so does not have a vote category
        if len(vote):
            points = int(vote[0].getText().replace(" points", ""))
            #Change 150 to a lower number if you want to see more articles
            if points > 150:
                hn.append({"title": title, "link": href, "score": points})

    return hn


def sort_by_points(hn_list):
    """Sorts the given list of dictionaries by the score category."""

    #reversed so that the list is in descending order
    return sorted(hn_list, key=lambda x: x["score"], reverse=True)


def format_list(sorted_list):
    """Formats the dictionaries in the sorted list so they can be printed neatly on the console"""

    for idx, dictionary in enumerate(sorted_list):
        score, title, link = dictionary["score"], dictionary["title"], dictionary["link"]

        print(f'\n\nTitle: {title}\nScore: {score}\nLink: {link}')


def main():
    #Get links and subtext from page 1 of hacker news
    soup = get_soup("https://news.ycombinator.com/news")
    links = get_links(soup)
    subtext = get_subtext(soup)
    #Add links and subtext from pages 2 and 3 of hacker news
    for link in ["https://news.ycombinator.com/news?p=2", "https://news.ycombinator.com/news?p=3"]:
        soup = get_soup(link)
        add_links(links, soup)
        add_subtext(subtext, soup)

    format_list(sort_by_points(clean(links, subtext)))


if __name__ == "__main__":
    main()
