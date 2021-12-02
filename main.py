#!/usr/bin/env python3
from argparse import ArgumentParser
from curses_ui import init_ui
from stories import print_articles


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


# MAIN ----------------------------------------------------------------------------------
def main():
    if args.print:
        print_articles()
    else:
        init_ui()


if __name__ == "__main__":
    main()
