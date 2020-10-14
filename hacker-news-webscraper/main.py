import tkinter as tk
from tkinter import ttk
import webbrowser
import textwrap
import os

import parse_script


# Font and cursor for gui
TITLE_FONT = ("Helvetica", 12, "underline", "bold")
TITLE_CURSOR = "hand2"

# Variable to keep track of the index of the article in display, for displaying different articles as only 10 fit on the gui at one time
# A list so that variable changes from within the scope of functions are changed
headline_tally = [0]

def alternative_hacker_news(links, subtext):
    """
    Returns an organised list of dictionaries which display title,
    link and votes to each article, if the article has more than 150 votes.
    """

    hn = []
    for inx, _ in enumerate(links):
        vote = subtext[inx].select(".score")
        title = links[inx].getText()
        href = links[inx].get("href", None)
        # If statement in case article has not yet received any votes so does not have a vote category
        if len(vote):
            points = int(vote[0].getText().replace(" points", ""))
            # Change 150 to a lower number if you want to see more articles
            if points > 150:
                hn.append({"title": title, "link": href, "score": points})

    return hn


def sort_by_points(hn_list):
    """Returns a sorted list of dictionaries from alternative_hacker_news to be ordered by score (highest first)"""

    sorted_list = sorted(hn_list, key=lambda k: k["score"], reverse=True)

    return sorted_list


def format_titles(sorted_list):
    """Returns a list of dictionaries where the titles within the dictionaries are formatted so that they have wrapped text (to fit inside their given labels)"""

    wrap_size = 30
    formatted_list = sorted_list
    for dictionary in sorted_list:
        if len(dictionary["title"]) > wrap_size:
            dictionary["title"] = textwrap.fill(dictionary["title"], wrap_size)

    return formatted_list


def open_url(url):
    """Opens the given url with the default browser, to be activated when a title is clicked"""

    webbrowser.open_new(url)


def bind_links(count, formatted_list):
    """Binds the open_url function onto each title so that they can simply be clicked to open the respective link"""

    title_label1.bind(
        "<Button-1>", lambda e: open_url(formatted_list[count]["link"]))
    title_label2.bind(
        "<Button-1>", lambda e: open_url(formatted_list[count + 1]["link"]))
    title_label3.bind(
        "<Button-1>", lambda e: open_url(formatted_list[count + 2]["link"]))
    title_label4.bind(
        "<Button-1>", lambda e: open_url(formatted_list[count + 3]["link"]))
    title_label5.bind(
        "<Button-1>", lambda e: open_url(formatted_list[count + 4]["link"]))
    title_label6.bind(
        "<Button-1>", lambda e: open_url(formatted_list[count + 5]["link"]))
    title_label7.bind(
        "<Button-1>", lambda e: open_url(formatted_list[count + 6]["link"]))
    title_label8.bind(
        "<Button-1>", lambda e: open_url(formatted_list[count + 7]["link"]))
    title_label9.bind(
        "<Button-1>", lambda e: open_url(formatted_list[count + 8]["link"]))
    title_label10.bind(
        "<Button-1>", lambda e: open_url(formatted_list[count + 9]["link"]))


def set_titles(count, formatted_list):
    """Sets the title for each of the 10 labels on the gui
    Titles are set according to variable headline_tally, so they may be given in order
    """

    title_label1["text"] = f'{str(count+1)}. {formatted_list[count]["title"]}\nScore: {str(formatted_list[count]["score"])}'
    title_label2["text"] = f'{str(count+2)}. {formatted_list[count+1]["title"]}\nScore: {str(formatted_list[count+1]["score"])}'
    title_label3["text"] = f'{str(count+3)}. {formatted_list[count+2]["title"]}\nScore: {str(formatted_list[count+2]["score"])}'
    title_label4["text"] = f'{str(count+4)}. {formatted_list[count+3]["title"]}\nScore: {str(formatted_list[count+3]["score"])}'
    title_label5["text"] = f'{str(count+5)}. {formatted_list[count+4]["title"]}\nScore: {str(formatted_list[count+4]["score"])}'
    title_label6["text"] = f'{str(count+6)}. {formatted_list[count+5]["title"]}\nScore: {str(formatted_list[count+5]["score"])}'
    title_label7["text"] = f'{str(count+7)}. {formatted_list[count+6]["title"]}\nScore: {str(formatted_list[count+6]["score"])}'
    title_label8["text"] = f'{str(count+8)}. {formatted_list[count+7]["title"]}\nScore: {str(formatted_list[count+7]["score"])}'
    title_label9["text"] = f'{str(count+9)}. {formatted_list[count+8]["title"]}\nScore: {str(formatted_list[count+8]["score"])}'
    title_label10["text"] = f'{str(count+10)}. {formatted_list[count+9]["title"]}\nScore: {str(formatted_list[count+9]["score"])}'


def titles_and_links(formatted_list, headline_tally):
    """Helper function to run bind_links and set_titles functions"""

    bind_links(headline_tally[0], formatted_list)
    set_titles(headline_tally[0], formatted_list)


def previous_button_function(formatted_list, headline_tally):
    """Shows previous 10 articles (if possible)"""
    if headline_tally[0] >= 10:
        headline_tally[0] -= 10
        titles_and_links(formatted_list, headline_tally)


def next_button_function(formatted_list, headline_tally):
    """Shows next 10 articles (if possible)"""

    if len(formatted_list) >= (headline_tally[0] + 20):
        headline_tally[0] += 10
        titles_and_links(formatted_list, headline_tally)


def links_and_subtext():
    """
    Returns a tuple containing a list of links to articles and a list of titles and votes,
    to be sent to alternative_hacker_news function
    """

    # Get links and subtext from page 1 of hacker news
    soup = parse_script.get_soup("https://news.ycombinator.com/news")
    links = parse_script.get_links(soup)
    subtext = parse_script.get_subtext(soup)
    # Add links and subtext from pages 2 and 3 of hacker news
    for link in ["https://news.ycombinator.com/news?p=2", "https://news.ycombinator.com/news?p=3"]:
        soup = parse_script.get_soup(link)
        parse_script.add_links(links, soup)
        parse_script.add_subtext(subtext, soup)

    return (links, subtext)


def get_formatted_list(links_and_subtext):
    """Gets a formatted list of all the articles with over 150 points"""

    formatted_list = format_titles(sort_by_points(
        alternative_hacker_news(links_and_subtext[0], links_and_subtext[1])))

    return formatted_list


# Get formatted list of articles and links
# Only executed once while the program runs, so a refesh requires the program to be restarted
formatted_list = get_formatted_list(links_and_subtext())

# UI --------------------------------------------------------------------------
root = tk.Tk()

# default window size
default_window = tk.Canvas(root, height=900, width=800)
default_window.pack()

# background
bg = tk.Label(root, bg="black", bd=15)
bg.place(relwidth=1, relheight=1)

# Set icon and title for window
root.tk.call('wm', 'iconphoto', root._w, tk.PhotoImage(file=os.path.join(os.getcwd(),
                                                                         'assets/icon.ico'
                                                                         )))
root.title("Hacker News Webscraper")

# Make Title Label with link to hacker news
title_frame = tk.Frame(root)
title_frame.place(relx=0.2, rely=0.01, relwidth=0.6, relheight=0.1)

title_background = tk.Label(title_frame, bg="gray")
title_background.place(relwidth=1, relheight=1)

title_label = tk.Label(title_frame, bg="gray",
                       text="Hacker News Parser Display", font=("Helvetica", 18, "bold"))
title_label.place(relx=0.025, rely=0.025, relwidth=0.95, relheight=0.7)

hacker_news_link = tk.Label(title_frame, bg="gray", text="Click here to go to the original Hacker News website (source)", font=(
    "Helvetica", 10, "underline"), cursor=TITLE_CURSOR)
hacker_news_link.place(relx=0.025, rely=0.75, relheight=0.25, relwidth=0.95)
hacker_news_link.bind(
    "<Button-1>", lambda e: open_url("https://news.ycombinator.com/"))

# FRAMES
# make frames
frame1 = tk.Frame(root)
frame2 = tk.Frame(root)
frame3 = tk.Frame(root)
frame4 = tk.Frame(root)
frame5 = tk.Frame(root)
frame6 = tk.Frame(root)
frame7 = tk.Frame(root)
frame8 = tk.Frame(root)
frame9 = tk.Frame(root)
frame10 = tk.Frame(root)
# place the frames
frame1.place(relx=0.025, rely=0.125, relwidth=0.45, relheight=0.15)
frame2.place(relx=0.025, rely=0.3, relwidth=0.45, relheight=0.15)
frame3.place(relx=0.025, rely=0.475, relwidth=0.45, relheight=0.15)
frame4.place(relx=0.025, rely=0.65, relwidth=0.45, relheight=0.15)
frame5.place(relx=0.025, rely=0.825, relwidth=0.45, relheight=0.15)
frame6.place(relx=0.525, rely=0.125, relwidth=0.45, relheight=0.15)
frame7.place(relx=0.525, rely=0.3, relwidth=0.45, relheight=0.15)
frame8.place(relx=0.525, rely=0.475, relwidth=0.45, relheight=0.15)
frame9.place(relx=0.525, rely=0.65, relwidth=0.45, relheight=0.15)
frame10.place(relx=0.525, rely=0.825, relwidth=0.45, relheight=0.15)
# frame backgrounds
bg1 = tk.Label(frame1, bg="gray")
bg1.place(relwidth=1, relheight=1)
bg2 = tk.Label(frame2, bg="gray")
bg2.place(relwidth=1, relheight=1)
bg3 = tk.Label(frame3, bg="gray")
bg3.place(relwidth=1, relheight=1)
bg4 = tk.Label(frame4, bg="gray")
bg4.place(relwidth=1, relheight=1)
bg5 = tk.Label(frame5, bg="gray")
bg5.place(relwidth=1, relheight=1)
bg6 = tk.Label(frame6, bg="gray")
bg6.place(relwidth=1, relheight=1)
bg7 = tk.Label(frame7, bg="gray")
bg7.place(relwidth=1, relheight=1)
bg8 = tk.Label(frame8, bg="gray")
bg8.place(relwidth=1, relheight=1)
bg9 = tk.Label(frame9, bg="gray")
bg9.place(relwidth=1, relheight=1)
bg10 = tk.Label(frame10, bg="gray")
bg10.place(relwidth=1, relheight=1)

# LABELS
# make title labels
title_label1 = tk.Label(
    frame1, bg="gray", font=TITLE_FONT, cursor=TITLE_CURSOR)
title_label1.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.8)
title_label2 = tk.Label(
    frame2, bg="gray", font=TITLE_FONT, cursor=TITLE_CURSOR)
title_label2.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.8)
title_label3 = tk.Label(
    frame3, bg="gray", font=TITLE_FONT, cursor=TITLE_CURSOR)
title_label3.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.8)
title_label4 = tk.Label(
    frame4, bg="gray", font=TITLE_FONT, cursor=TITLE_CURSOR)
title_label4.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.8)
title_label5 = tk.Label(
    frame5, bg="gray", font=TITLE_FONT, cursor=TITLE_CURSOR)
title_label5.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.8)
title_label6 = tk.Label(
    frame6, bg="gray", font=TITLE_FONT, cursor=TITLE_CURSOR)
title_label6.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.8)
title_label7 = tk.Label(
    frame7, bg="gray", font=TITLE_FONT, cursor=TITLE_CURSOR)
title_label7.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.8)
title_label8 = tk.Label(
    frame8, bg="gray", font=TITLE_FONT, cursor=TITLE_CURSOR)
title_label8.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.8)
title_label9 = tk.Label(
    frame9, bg="gray", font=TITLE_FONT, cursor=TITLE_CURSOR)
title_label9.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.8)
title_label10 = tk.Label(
    frame10, bg="gray", font=TITLE_FONT, cursor=TITLE_CURSOR)
title_label10.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.8)

# BUTTONS
# make next and previous buttons
next_button = ttk.Button(root, text="Next", command=lambda: next_button_function(
    formatted_list, headline_tally), cursor=TITLE_CURSOR)
next_button.place(relx=0.875, rely=0.06, relwidth=0.1, relheight=0.05)

previous_button = ttk.Button(root, text="Previous", command=lambda: previous_button_function(
    formatted_list, headline_tally), cursor=TITLE_CURSOR)
previous_button.place(relx=0.025, rely=0.06, relwidth=0.1, relheight=0.05)

# Displays first 10 articles straight away
titles_and_links(formatted_list, headline_tally)

root.mainloop()
