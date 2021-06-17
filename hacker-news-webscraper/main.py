import tkinter as tk
from tkinter import ttk
import webbrowser
import textwrap
import os

import parse_script


# Font and cursor for gui
HEADER_FONT = ("Helvetica", 20, "bold")
TITLE_FONT = ("Helvetica", 15, "bold")
LINK_FONT = ("Helvetica", 11, "underline")
BUTTON_FONT = ("Helvetica", 12)
TITLE_CURSOR = "hand2"

# Minimum votes for article to be included
MIN_SCORE = 150

# UI colours
BG_PRIMARY = "#1F1B24"
BG_SECONDARY = "#373040"
BG_BUTTON = "#b53930"
BG_BUTTON_HOVER = "#c93f36"
TEXT = "#cccccc"

# Variable to keep track of the index of the article in display, for
# displaying different articles as only 10 fit on the gui at one time
headline_tally = [0]


def alternative_hacker_news(links, subtext):
    """
    Returns an organised list of dictionaries which display title, link and votes
    to each article, if the article has at least MIN_SCORE votes.
    """

    hn = []
    for inx, _ in enumerate(links):
        vote = subtext[inx].select(".score")
        title = links[inx].getText()
        href = links[inx].get("href", None)

        # Fix links which point back to the Y Combinator website itself
        if not href.startswith("http"):
            href = parse_script.fix_item_link(href)

        # If statement in case article has not yet received any votes so
        # does not have a vote category
        if len(vote):
            points = int(vote[0].getText().replace(" points", ""))

            if points >= MIN_SCORE:
                hn.append({"title": title, "link": href, "score": points})

    return hn


def sort_by_points(hn_list):
    """
    Returns a sorted list of dictionaries from alternative_hacker_news to
    be ordered by score (highest first).
    """

    sorted_list = sorted(hn_list, key=lambda k: k["score"], reverse=True)

    return sorted_list


def format_titles(sorted_list):
    """
    Returns a list of dictionaries where the titles within the
    dictionaries are formatted so that they have wrapped text
    (to fit inside their given labels).
    """

    wrap_size = 30
    formatted_list = sorted_list
    for dictionary in sorted_list:
        if len(dictionary["title"]) > wrap_size:
            dictionary["title"] = textwrap.fill(dictionary["title"], wrap_size)

    return formatted_list


def bind_label_to_url(label, url):
    """Binds a label with a function which opens a given url (in a new window)."""

    label.bind("<Button-1>", lambda e: webbrowser.open_new(url))


def titles_and_links(count, formatted_list, labels):
    """
    Applies corresponding article text and binds article link to each label.
    """

    for i, label in enumerate(labels):
        no = count + i
        article_no = str(no + 1)
        article_title = formatted_list[no]["title"]
        article_score = str(formatted_list[no]["score"])
        article_link = formatted_list[no]["link"]

        bind_label_to_url(label, article_link)
        label["text"] = f"{article_no}. {article_title}\nScore: {article_score}"


def previous_button_function(headline_tally, formatted_list, labels):
    """Shows previous 10 articles (if possible)."""
    if headline_tally[0] >= 10:
        headline_tally[0] -= 10
        titles_and_links(headline_tally[0], formatted_list, labels)


def next_button_function(formatted_list, headline_tally, labels):
    """Shows next 10 articles (if possible)."""

    if len(formatted_list) >= (headline_tally[0] + 20):
        headline_tally[0] += 10
        titles_and_links(headline_tally[0], formatted_list, labels)


def links_and_subtext():
    """
    Returns a tuple containing a list of links to articles and a list of
    titles and votes, to be sent to the alternative_hacker_news function.
    """

    # Get links and subtext from page 1 of hacker news
    soup = parse_script.get_soup("https://news.ycombinator.com/news")
    links = parse_script.get_links(soup)
    subtext = parse_script.get_subtext(soup)
    # Add links and subtext from pages 2 and 3 of hacker news
    for link in [
        "https://news.ycombinator.com/news?p=2",
        "https://news.ycombinator.com/news?p=3",
    ]:
        soup = parse_script.get_soup(link)
        parse_script.add_links(links, soup)
        parse_script.add_subtext(subtext, soup)

    return (links, subtext)


def get_formatted_list(links_and_subtext):
    """Gets a formatted list of all the articles with over 150 points"""

    formatted_list = format_titles(
        sort_by_points(
            alternative_hacker_news(links_and_subtext[0], links_and_subtext[1])
        )
    )

    return formatted_list


# Get formatted list of articles and links
# Only executed once while the program runs, so a refresh requires the
# program to be restarted
formatted_list = get_formatted_list(links_and_subtext())

# UI --------------------------------------------------------------------------
root = tk.Tk()

# Default window size
default_window = tk.Canvas(root, height=900, width=800)
default_window.pack()

# Background
bg = tk.Label(root, bg=BG_PRIMARY, bd=15)
bg.place(relwidth=1, relheight=1)

# Set icon and title for window
root.tk.call(
    "wm",
    "iconphoto",
    root._w,
    tk.PhotoImage(file=os.path.join(os.path.dirname(__file__), "assets", "icon.ico")),
)
root.title("Hacker News Webscraper")

# Make Title Label with link to hacker news
title_frame = tk.Frame(root)
title_frame.place(relx=0.2, rely=0.01, relwidth=0.6, relheight=0.1)

title_background = tk.Label(title_frame, bg=BG_SECONDARY)
title_background.place(relwidth=1, relheight=1)

title_label = tk.Label(
    title_frame,
    bg=BG_SECONDARY,
    text="Hacker News Webscraper",
    font=HEADER_FONT,
    fg=TEXT,
)
title_label.place(relx=0.025, rely=0.025, relwidth=0.95, relheight=0.7)

hacker_news_link = tk.Label(
    title_frame,
    bg=BG_SECONDARY,
    text="Original website (source)",
    font=LINK_FONT,
    cursor=TITLE_CURSOR,
    fg=TEXT,
)
hacker_news_link.place(relx=0.025, rely=0.75, relheight=0.25, relwidth=0.95)
hacker_news_link.bind(
    "<Button-1>", lambda e: webbrowser.open_new("https://news.ycombinator.com/")
)

# ARTICLES
FRAME_HEIGHT = 0.15
FRAME_WIDTH = 0.45
FRAME_START_X = 0.025
FRAME_END_X = 0.5 + FRAME_START_X
FRAME_Y_VALUES = [0.125, 0.3, 0.475, 0.65, 0.825]
LABEL_LOCATION = 0.1
LABEL_SIZE = 0.8

# Make and place ui elements, saving the finished label elements into lists
# since the text on them needs to be changed
labels = []
for i in range(5):
    # Frames
    left_column_frame = tk.Frame(root)
    right_column_frame = tk.Frame(root)

    left_column_frame.place(
        relx=FRAME_START_X,
        rely=FRAME_Y_VALUES[i],
        relwidth=FRAME_WIDTH,
        relheight=FRAME_HEIGHT,
    )
    right_column_frame.place(
        relx=FRAME_END_X,
        rely=FRAME_Y_VALUES[i],
        relwidth=FRAME_WIDTH,
        relheight=FRAME_HEIGHT,
    )

    # Set frame backgrounds, currently no need to save these as they do not need
    # to be changed
    tk.Label(left_column_frame, bg=BG_SECONDARY).place(relwidth=1, relheight=1)
    tk.Label(right_column_frame, bg=BG_SECONDARY).place(relwidth=1, relheight=1)

    # Create text labels
    left_frame_label = tk.Label(
        left_column_frame,
        bg=BG_SECONDARY,
        font=TITLE_FONT,
        cursor=TITLE_CURSOR,
        fg=TEXT,
    )
    right_frame_label = tk.Label(
        right_column_frame,
        bg=BG_SECONDARY,
        font=TITLE_FONT,
        cursor=TITLE_CURSOR,
        fg=TEXT,
    )

    # Place text labels, and add them to the labels list
    for label in (left_frame_label, right_frame_label):
        label.place(
            relx=LABEL_LOCATION,
            rely=LABEL_LOCATION,
            relwidth=LABEL_SIZE,
            relheight=LABEL_SIZE,
        )
        labels.append(label)

# BUTTONS
# Make 'next' and 'previous' buttons
style = ttk.Style()
style.configure(
    "TButton",
    background=BG_BUTTON,
    foreground=TEXT,
    font=BUTTON_FONT,
)
style.map("TButton", background=[("active", BG_BUTTON_HOVER)])

next_button = ttk.Button(
    root,
    text="Next",
    command=lambda: next_button_function(formatted_list, headline_tally, labels),
    cursor=TITLE_CURSOR,
)
next_button.place(relx=0.875, rely=0.06, relwidth=0.1, relheight=0.05)

previous_button = ttk.Button(
    root,
    text="Previous",
    command=lambda: previous_button_function(headline_tally, formatted_list, labels),
    cursor=TITLE_CURSOR,
)
previous_button.place(relx=0.025, rely=0.06, relwidth=0.1, relheight=0.05)

# Displays first 10 articles straight away
titles_and_links(headline_tally[0], formatted_list, labels)

root.mainloop()
