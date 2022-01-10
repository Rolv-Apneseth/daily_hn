#!/usr/bin/env python3
from argparse import ArgumentParser
from bs4 import BeautifulSoup
import requests
import curses
import webbrowser


# ARGUMENTS -----------------------------------------------------------------------------
parser = ArgumentParser(
    description=(
        "A CLI program written in Python with the curses library, used for keeping up"
        " with the current best stories from news.ycombinator.com (Hacker News)."
    ),
)

parser.add_argument(
    "-p",
    "--print",
    action="store_true",
    help=(
        "Simply outputs the formatted stories to stdout, instead of using the"
        "fancy curses interface."
    ),
)

args = parser.parse_args()


# STORIES -------------------------------------------------------------------------------
class Stories:
    BASE_URL: str = "https://news.ycombinator.com/"
    BEST_STORIES_URL: str = f"{BASE_URL}best"
    SCORE_SELECTOR: str = ".score"
    TITLES_SELECTOR: str = ".titlelink"

    @classmethod
    def _get_soup(cls, link: str):
        """Gets soup from a given website."""

        response = requests.get(link)
        return BeautifulSoup(response.text, "html.parser")

    @classmethod
    def _get_titles(cls, soup: BeautifulSoup):
        """Gets story title elements from the given hacker news soup."""

        return soup.select(cls.TITLES_SELECTOR)

    @classmethod
    def _get_scores(cls, soup: BeautifulSoup):
        """Gets subtext elements from the given hacker news soup."""

        return soup.select(cls.SCORE_SELECTOR)

    @classmethod
    def _fix_item_link(cls, href: str):
        """
        Fixes links which point to specific items in the hacker news
        website itself, as they just point to specific pages on the site.
        """

        return f"{cls.BASE_URL}{href}"

    @classmethod
    def get_stories(cls):
        """Returns a list of dictionaries representing stories."""

        soup = cls._get_soup(cls.BEST_STORIES_URL)

        titles = cls._get_titles(soup)
        scores = cls._get_scores(soup)

        return [
            {
                "headline": title.get_text(),
                "link": title["href"]
                if title["href"].startswith("http")
                else cls._fix_item_link((title["href"])),
                "score": score.getText().replace(" points", ""),
            }
            for title, score in zip(titles, scores)
        ]

    @classmethod
    def print_articles(cls):
        """Simple print of articles to the screen."""

        stories = cls.get_stories()

        for i, story in enumerate(reversed(stories)):
            print(
                f"\n\n{30-i}. {story.get('headline')}"
                f"\nScore: {story.get('score')}"
                f"\nLink: {story.get('link')}"
            )


# CURSES UI -----------------------------------------------------------------------------
class UI:
    # 'jk{}' used for navigation, 'q' used for quitting
    POSSIBLE_STORY_SHORTCUTS: str = 'abcdefhilmnoprstuvwxyz!"$%^&*.'
    # Base measurements
    STORIES_STARTING_ROW: int = 3
    STORIES_STARTING_COL: int = 2
    BORDER_WIDTH: int = 2
    STORY_ROWS: int = 3
    NUMBER_SPACING: int = 4
    # Other
    PROGRAM_TITLE: str = "Daily Dose of HN"

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
            cls.PROGRAM_TITLE,
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
            story_index * cls.STORY_ROWS,
            0,
            f"({shortcut_key})",
            colour | curses.A_BOLD,
        )

    @classmethod
    def _add_stories_to_pad(
        cls, stories_pad, stories: list[dict], colours: dict, MAX_TITLE_LENGTH: int
    ):
        """Draw all the given stories to the stories pad."""

        for i, story in enumerate(stories):
            # labelling (shortcuts)
            cls._draw_shortcut_key(
                stories_pad, colours["fg_magenta"], i, cls.POSSIBLE_STORY_SHORTCUTS[i]
            )
            # headline
            stories_pad.addstr(
                i * cls.STORY_ROWS,
                cls.NUMBER_SPACING,
                cls._format_headline(story["headline"], MAX_TITLE_LENGTH),
                curses.A_BOLD,
            )
            # score
            stories_pad.addstr(
                i * cls.STORY_ROWS + 1,
                cls.NUMBER_SPACING,
                f"{story['score']}",
                colours["fg_yellow"] | curses.A_BOLD,
            )

    @classmethod
    def _refresh_stories_pad(cls, stories_pad, pad_starting_row: int, MAX_LINES: int):
        """Convenience function for refreshing story pad."""

        stories_pad.refresh(
            pad_starting_row,
            0,
            cls.STORIES_STARTING_ROW,
            cls.STORIES_STARTING_COL,
            MAX_LINES,
            curses.COLS - cls.BORDER_WIDTH,
        )

    @staticmethod
    def _open_url(url: str):
        """Opens the given url in a new browser window."""

        webbrowser.open(url, new=1)

    @classmethod
    def _draw_ui(cls, stdscr, stories: list[dict]):
        """Main function for drawing the UI for the program."""

        MAX_TITLE_LENGTH = curses.COLS - cls.NUMBER_SPACING - cls.BORDER_WIDTH * 2
        MAX_LINES = curses.LINES - cls.BORDER_WIDTH
        STORIES_PAD_HEIGHT = len(stories) * cls.STORY_ROWS
        STORIES_PAD_WIDTH = MAX_TITLE_LENGTH + cls.NUMBER_SPACING
        MAX_SCROLL = STORIES_PAD_HEIGHT - MAX_LINES + 2
        SCROLL_AMOUNT_LARGE = MAX_LINES - cls.STORY_ROWS

        pad_starting_row = 0  # Used for scrolling the stories pad

        # BASE SETUP
        cls._base_curses_setup()
        COLOURS = cls._get_colours()
        cls._base_ui_setup(stdscr, COLOURS)
        stdscr.refresh()

        # STORIES PAD SETUP
        stories_pad = curses.newpad(STORIES_PAD_HEIGHT, STORIES_PAD_WIDTH)

        cls._add_stories_to_pad(stories_pad, stories, COLOURS, MAX_TITLE_LENGTH)
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
            elif keypress in cls.POSSIBLE_STORY_SHORTCUTS:
                story_index = cls.POSSIBLE_STORY_SHORTCUTS.find(keypress)
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
