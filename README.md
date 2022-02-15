# daily_hn

![Tests](https://github.com/Rolv-Apneseth/daily_hn/actions/workflows/tests.yml/badge.svg)
![Linux](https://img.shields.io/badge/-Linux-grey?logo=linux)
![OSX](https://img.shields.io/badge/-OSX-black?logo=apple)
![Python](https://img.shields.io/badge/Python-v3.9%5E-green?logo=python)

![Demo aPNG](https://github.com/Rolv-Apneseth/Rolv-Apneseth.github.io/blob/4f0024e25168a57757d4631a6346275cb3f9cee7/assets/images/animated_images/daily-hn.png)

## Description

A command line tool for displaying and opening links to the current best stories from [news.ycombinator.com](https://news.ycombinator.com) (Hacker News).

You can find the best stories page this program parses [here](https://news.ycombinator.com/best)!

## Dependencies

- [Python](https://www.python.org/downloads/) v3.9+
- [Beautiful Soup 4](https://pypi.org/project/beautifulsoup4/)
- [Requests](https://pypi.org/project/requests/)
- If you are on Windows: [Windows curses module](https://pypi.org/project/windows-curses/) (Python)

## Installation

To download, click on 'Code' to the top right, then download as a zip file. You can unzip using your preferred program.

> You can also clone the repository using:

```bash
git clone https://github.com/Rolv-Apneseth/daily_hn.git
```

Next, install the requirements for the program.

> In your terminal, navigate to the cloned directory and run:

```bash
python3 -m pip install requests beautifulsoup4
```

Then, to place the `daily_hn` script at `/usr/local/daily_hn`:

```bash
sudo make install
```

Now, to launch the program in your terminal simply run `daily_hn`

### Windows

Install the requirements for the program.

> In your terminal, navigate to the cloned directory and run:

```bash
pip install beautifulsoup4 requests windows-curses
```

To launch the program, navigate to the project directory and run:

```bash
python daily_hn.py
```

## Usage

With the curses UI (default), you can open up stories (uses the default browser) by pressing the shortcut key to the left of that story. Navigate up and down using either `j` and `k` for fine movements or `{` and `}` for bigger jumps. To quit, press `q`.

To simply print out a list of stories (links being clickable depends on your terminal emulator), provide the `-p` flag

## License

[MIT](https://github.com/Rolv-Apneseth/daily_hn/blob/2d40839e6e625c55075430bde5fef337a08e89ba/LICENSE)
