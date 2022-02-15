#!/usr/bin/env python3
# ---------------------------------------------------------------------------------------
# Author: Rolv-Apneseth <rolv.apneseth@gmail.com>
# License: MIT
# ---------------------------------------------------------------------------------------

"""
A command line tool for displaying and opening links to the current best stories from
news.ycombinator.com (Hacker News)
"""

import curses
import webbrowser
from argparse import ArgumentParser

import requests
from bs4 import BeautifulSoup, Tag


# ARGUMENTS -----------------------------------------------------------------------------
parser = ArgumentParser(description=__doc__)

parser.add_argument(
    "-p",
    "--print",
    action="store_true",
    help=("prints the stories to the terminal instead of using the ncurses gui"),
)

args = parser.parse_args()


# STORIES -------------------------------------------------------------------------------
class Stories:
    """Handles the fetching and formatting of stories."""

    base_url: str = "https://news.ycombinator.com/"
    best_stories_url: str = f"{base_url}best"
    score_selector: str = ".score"
    titles_selector: str = ".titlelink"

    @classmethod
    def _get_soup(cls, link: str):
        """Gets soup from a given website."""

        response = requests.get(link)
        return BeautifulSoup(response.text, "html.parser")

    @classmethod
    def _get_titles(cls, soup: BeautifulSoup):
        """Gets story title elements from the given hacker news soup."""

        return soup.select(cls.titles_selector)

    @classmethod
    def _get_scores(cls, soup: BeautifulSoup):
        """Gets subtext elements from the given hacker news soup."""

        return soup.select(cls.score_selector)

    @classmethod
    def _fix_item_link(cls, href: str):
        """
        Fixes links which point to specific items in the hacker news
        website itself, as they just point to specific pages on the site.
        """

        return f"{cls.base_url}{href}"

    @classmethod
    def _get_points(cls, score: Tag):
        """Returns an integer representing the points extracted from a given Tag."""

        return int(score.getText().split()[0])

    @classmethod
    def get_stories(cls):
        """Returns a list of dictionaries representing stories."""

        soup = cls._get_soup(cls.best_stories_url)

        titles = cls._get_titles(soup)
        scores = cls._get_scores(soup)

        return [
            {
                "headline": title.get_text(),
                "link": title["href"]
                if title["href"].startswith("http")
                else cls._fix_item_link((title["href"])),
                "score": cls._get_points(score),
            }
            for title, score in zip(titles, scores)
        ]

    @classmethod
    def print_articles(cls, stories: list[dict] = None):
        """Simple print of articles to the screen."""

        if stories is None:
            stories = cls.get_stories()

        for i, story in enumerate(reversed(stories)):
            print(
                f"\n\n{30-i}. {story.get('headline')}"
                f"\nScore: {story.get('score')}"
                f"\nLink: {story.get('link')}"
            )


# CURSES UI -----------------------------------------------------------------------------
class UI:
    """Handles the drawing and management of the ncurses UI."""

    # 'jk{}' used for navigation, 'q' used for quitting
    story_shortcuts: str = 'abcdefhilmnoprstuvwxyz!"$%^&*.'
    # Base measurements
    stories_starting_row: int = 3
    stories_starting_col: int = 2
    border_width: int = 2
    story_rows: int = 3
    number_spacing: int = 4
    # Other
    program_title: str = "Daily Dose of HN"

    @staticmethod
    def _base_curses_setup():
        """
        Sets some basic curses configuration options, such as using default colours.
        """

        curses.use_default_colors()
        curses.curs_set(0)

    @staticmethod
    def _get_colours():
        """Sets up curses colour pairs for easy use."""

        colours = dict(
            fg_blue=(curses.COLOR_BLUE, -1),
            fg_red=(curses.COLOR_RED, -1),
            fg_green=(curses.COLOR_GREEN, -1),
            fg_cyan=(curses.COLOR_CYAN, -1),
            fg_magenta=(curses.COLOR_MAGENTA, -1),
            fg_yellow=(curses.COLOR_YELLOW, -1),
        )

        for i, name in enumerate(colours.keys(), start=1):
            curses.init_pair(i, *colours[name])
            colours[name] = curses.color_pair(i)

        return colours

    @staticmethod
    def _format_headline(headline: str, max_length: int):
        """Cuts/formats a headline to fit in 1 row of the stories pad."""

        return (
            f"{headline[:max_length - 3].strip()}..."
            if len(headline) > max_length
            else headline
        )

    @classmethod
    def _draw_title(cls, stdscr, colours: dict):
        """Draws the title for the program."""

        stdscr.addstr(
            1,
            2,
            cls.program_title,
            curses.A_UNDERLINE | curses.A_BOLD | colours["fg_green"],
        )

    @classmethod
    def _draw_border(cls, stdscr, colours):
        """Draws a basic border for the program."""

        cls.BORDER_DESIGN = curses.A_BOLD | colours["fg_magenta"]
        stdscr.attron(cls.BORDER_DESIGN)
        stdscr.box()
        stdscr.attroff(cls.BORDER_DESIGN)

    @classmethod
    def _base_ui_setup(cls, stdscr, colours: dict):
        """Base ui setup, draws the title of the program and a basic border."""

        cls._draw_title(stdscr, colours)
        cls._draw_border(stdscr, colours)

    @classmethod
    def _draw_shortcut_key(
        cls, stories_pad, colour: int, story_index: int, shortcut_key: str
    ):
        """
        Draws a given shortcut key to the stories pad based on the given story index.
        """

        stories_pad.addstr(
            story_index * cls.story_rows,
            0,
            f"({shortcut_key})",
            colour | curses.A_BOLD,
        )

    @classmethod
    def _add_stories_to_pad(
        cls, stories_pad, stories: list[dict], colours: dict, max_title_length: int
    ):
        """Draw all the given stories to the stories pad."""

        for i, story in enumerate(stories):
            # labelling (shortcuts)
            cls._draw_shortcut_key(
                stories_pad, colours["fg_magenta"], i, cls.story_shortcuts[i]
            )
            # headline
            stories_pad.addstr(
                i * cls.story_rows,
                cls.number_spacing,
                cls._format_headline(story["headline"], max_title_length),
                curses.A_BOLD,
            )
            # score
            stories_pad.addstr(
                i * cls.story_rows + 1,
                cls.number_spacing,
                f"{story['score']}",
                colours["fg_yellow"] | curses.A_BOLD,
            )

    @classmethod
    def _refresh_stories_pad(cls, stories_pad, pad_starting_row: int, MAX_LINES: int):
        """Convenience function for refreshing story pad."""

        stories_pad.refresh(
            pad_starting_row,
            0,
            cls.stories_starting_row,
            cls.stories_starting_col,
            MAX_LINES,
            curses.COLS - cls.border_width,
        )

    @staticmethod
    def _open_url(url: str):
        """Opens the given url in a new browser window."""

        webbrowser.open(url, new=1)

    @classmethod
    def _draw_ui(cls, stdscr, stories: list[dict]):
        """Main function for drawing the UI for the program."""

        max_title_length = curses.COLS - cls.number_spacing - cls.border_width * 2
        MAX_LINES = curses.LINES - cls.border_width
        STORIES_PAD_HEIGHT = len(stories) * cls.story_rows
        STORIES_PAD_WIDTH = max_title_length + cls.number_spacing
        MAX_SCROLL = STORIES_PAD_HEIGHT - MAX_LINES + 2
        SCROLL_AMOUNT_LARGE = MAX_LINES - cls.story_rows

        pad_starting_row = 0  # Used for scrolling the stories pad

        # BASE SETUP
        cls._base_curses_setup()
        COLOURS = cls._get_colours()
        cls._base_ui_setup(stdscr, COLOURS)
        stdscr.refresh()

        # STORIES PAD SETUP
        stories_pad = curses.newpad(STORIES_PAD_HEIGHT, STORIES_PAD_WIDTH)

        cls._add_stories_to_pad(stories_pad, stories, COLOURS, max_title_length)
        cls._refresh_stories_pad(stories_pad, pad_starting_row, MAX_LINES)

        # MAIN LOOP
        while True:
            # Get user keypress
            keypress = stories_pad.getkey()

            # QUIT
            if keypress == "q":
                break

            # NAVIGATION
            elif keypress == "j" and pad_starting_row < MAX_SCROLL:
                pad_starting_row += 1
            elif keypress == "k" and pad_starting_row > 0:
                pad_starting_row -= 1
            elif keypress == "{":
                if pad_starting_row > SCROLL_AMOUNT_LARGE:
                    pad_starting_row -= SCROLL_AMOUNT_LARGE
                else:
                    pad_starting_row = 0
            elif keypress == "}":
                if pad_starting_row < MAX_SCROLL - SCROLL_AMOUNT_LARGE:
                    pad_starting_row += SCROLL_AMOUNT_LARGE
                else:
                    pad_starting_row = MAX_SCROLL

            # OPEN URLS
            elif keypress in cls.story_shortcuts:
                story_index = cls.story_shortcuts.find(keypress)
                matching_story_link = stories[story_index]["link"]

                cls._open_url(matching_story_link)

                # Apply visual change to shortcut keys next to opened story
                cls._draw_shortcut_key(
                    stories_pad, COLOURS["fg_green"], story_index, keypress
                )

            cls._refresh_stories_pad(stories_pad, pad_starting_row, MAX_LINES)

    @classmethod
    def init_ui(cls, stories: list[dict]):
        """Initialise the curses UI."""

        curses.wrapper(cls._draw_ui, stories)


# MAIN ----------------------------------------------------------------------------------
def main():
    # Print articles if --print arg is passed, otherwise initialise the curses UI
    if args.print:
        Stories.print_articles()
    else:
        UI.init_ui(Stories.get_stories())


if __name__ == "__main__":
    main()
