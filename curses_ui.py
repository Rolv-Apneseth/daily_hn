import curses
import webbrowser
from stories import get_stories

# 'jk{}' used for navigation, 'q' used for quitting
POSSIBLE_STORY_SHORTCUTS = 'abcdefhilmnoprstuvwxyz!"$%^&*.'
# Base measurements
STORIES_STARTING_ROW = 3
STORIES_STARTING_COL = 2
BORDER_WIDTH = 2
STORY_ROWS = 3
NUMBER_SPACING = 4
# Other
PROGRAM_TITLE = "Daily Dose of HN"


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


def _draw_title(stdscr, colours):
    """Draws the title for the program."""

    stdscr.addstr(
        1,
        2,
        PROGRAM_TITLE,
        curses.A_UNDERLINE | curses.A_BOLD | colours["fg_green"],
    )


def _draw_border(stdscr, colours):
    """Draws a basic border for the program."""

    BORDER_DESIGN = curses.A_BOLD | colours["fg_magenta"]
    stdscr.attron(BORDER_DESIGN)
    stdscr.box()
    stdscr.attroff(BORDER_DESIGN)


def _base_curses_setup(curses):
    """Sets some basic curses configuration options, such as using default colours."""

    curses.use_default_colors()
    curses.curs_set(0)


def _base_ui_setup(stdscr, colours):
    """Base ui setup, draws the title of the program and a basic border."""

    _draw_title(stdscr, colours)
    _draw_border(stdscr, colours)


def _format_headline(headline: str, max_length: int):
    """Cuts/formats a headline to fit in 1 row of the stories pad."""

    return (
        f"{headline[:max_length - 3].strip()}..."
        if len(headline) > max_length
        else headline
    )


def _draw_shortcut_key(stories_pad, colour: int, story_index: int, shortcut_key: str):
    """Draws a given shortcut key to the stories pad based on the given story index."""

    stories_pad.addstr(
        story_index * STORY_ROWS,
        0,
        f"({shortcut_key})",
        colour | curses.A_BOLD,
    )


def _add_stories_to_pad(stories_pad, stories: list[dict], colours, MAX_TITLE_LENGTH):
    """Draw all the given stories to the stories pad."""

    for i, story in enumerate(stories):
        # labelling (shortcuts)
        _draw_shortcut_key(
            stories_pad, colours["fg_magenta"], i, POSSIBLE_STORY_SHORTCUTS[i]
        )
        # headline
        stories_pad.addstr(
            i * STORY_ROWS,
            NUMBER_SPACING,
            _format_headline(story["headline"], MAX_TITLE_LENGTH),
            curses.A_BOLD,
        )
        # score
        stories_pad.addstr(
            i * STORY_ROWS + 1,
            NUMBER_SPACING,
            f"{story['score']}",
            colours["fg_yellow"] | curses.A_BOLD,
        )


def _refresh_stories_pad(stories_pad, pad_starting_row: int, MAX_LINES: int):
    """Convenience function for refreshing story pad."""

    stories_pad.refresh(
        pad_starting_row,
        0,
        STORIES_STARTING_ROW,
        STORIES_STARTING_COL,
        MAX_LINES,
        curses.COLS - BORDER_WIDTH,
    )


def _open_url(url: str):
    """Opens the given url in a new browser window."""

    webbrowser.open(url, new=1)


def _draw_ui(stdscr, stories: list[dict]):
    """Main function for drawing the UI for the program."""

    MAX_TITLE_LENGTH = curses.COLS - NUMBER_SPACING - BORDER_WIDTH * 2
    MAX_LINES = curses.LINES - BORDER_WIDTH
    STORIES_PAD_HEIGHT = len(stories) * STORY_ROWS
    STORIES_PAD_WIDTH = MAX_TITLE_LENGTH + NUMBER_SPACING
    MAX_SCROLL = STORIES_PAD_HEIGHT - MAX_LINES + 2
    SCROLL_AMOUNT_LARGE = MAX_LINES - STORY_ROWS
    pad_starting_row = 0  # Used for scrolling the stories pad

    # BASE SETUP
    _base_curses_setup(curses)
    COLOURS = _get_colours()
    _base_ui_setup(stdscr, COLOURS)
    stdscr.refresh()

    # STORIES PAD SETUP
    stories_pad = curses.newpad(STORIES_PAD_HEIGHT, STORIES_PAD_WIDTH)

    _add_stories_to_pad(stories_pad, stories, COLOURS, MAX_TITLE_LENGTH)
    _refresh_stories_pad(stories_pad, pad_starting_row, MAX_LINES)

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
        elif keypress in POSSIBLE_STORY_SHORTCUTS:
            story_index = POSSIBLE_STORY_SHORTCUTS.find(keypress)
            matching_story_link = stories[story_index]["link"]

            _open_url(matching_story_link)

            # Apply visual change to shortcut keys next to opened story
            _draw_shortcut_key(stories_pad, COLOURS["fg_green"], story_index, keypress)

        _refresh_stories_pad(stories_pad, pad_starting_row, MAX_LINES)


def init_ui():
    """Initialise the curses UI."""

    stories = get_stories()

    curses.wrapper(_draw_ui, stories)
