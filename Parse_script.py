from bs4 import BeautifulSoup
import requests
import pprint
from hyperlink import URL

#page 1 of news
res = requests.get("https://news.ycombinator.com/news")
soup = BeautifulSoup(res.text, "html.parser")
links = soup.select(".storylink")
subtext = soup.select(".subtext")

#page 2 of news
res = requests.get("https://news.ycombinator.com/news?p=2")
soup = BeautifulSoup(res.text, "html.parser")
links += soup.select(".storylink")
subtext += soup.select(".subtext")

#page 3 of news
res = requests.get("https://news.ycombinator.com/news?p=3")
soup = BeautifulSoup(res.text, "html.parser")
links += soup.select(".storylink")
subtext += soup.select(".subtext")


def clean(links, subtext):
    hn = []
    for inx, item in enumerate(links):
        vote = subtext[inx].select(".score")


        title = links[inx].getText()
        href = links[inx].get("href", None)
        if len(vote):
            points = int(vote[0].getText().replace(" points", ""))
            if points > 100:
                hn.append({"title": title, "link": href, "score": points})

    return hn


def sort_by_points(hn_list):
    return sorted(hn_list, key=lambda k: k["score"], reverse=True)


def format_list(sorted_list):
    for idx, dictionary in enumerate(sorted_list):
        score, title, link = dictionary["score"], dictionary["title"], dictionary["link"]
        url = URL.from_text(link)
        print(f'\n\nTitle: {title}\nScore: {score}\nLink: ', end="")
        print(url)



format_list(sort_by_points(clean(links, subtext)))