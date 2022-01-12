# daily-hn

![Demo aPNG](https://github.com/Rolv-Apneseth/Rolv-Apneseth.github.io/blob/4f0024e25168a57757d4631a6346275cb3f9cee7/assets/images/animated_images/daily-hn.png)

## Description

A minimalistic command line tool for displaying and opening links to the current best stories from [news.ycombinator.com](news.ycombinator.com) (Hacker News).

## Dependencies

- [Python3](https://www.python.org/downloads/) (v3.6 or later)
- [Beautiful Soup 4](https://pypi.org/project/beautifulsoup4/) (Python)
- [Requests](https://pypi.org/project/requests/) (Python)
- If you are on Windows: [Windows curses module](https://pypi.org/project/windows-curses/) (Python)

## Installation

To download, click on 'Code' to the top right, then download as a zip file. You can unzip using your preferred program.

> You can also clone the repository using:

```bash
git clone https://github.com/Rolv-Apneseth/daily-hn.git
```

### Linux

First, install the requirements for the program.

> In your terminal, navigate to the cloned directory and run:

```bash
python3 -m pip install -r requirements.txt
```

Then, to place the daily-hn script at `/usr/local/daily-hn`:

```bash
sudo make install
```

Now, to launch the program in your terminal simply run `daily-hn`

### Windows

Install the requirements for the program.

> In your terminal, navigate to the cloned directory and run:

```bash
pip install beautifulsoup4 requests windows-curses
```

To launch the program, navigate to the project directory and run:

```bash
python daily-hn.py
```

## Usage

With the curses UI (default), you can open up stories (uses the default browser) by pressing the shortcut key to the left of that story. Navigate up and down using either `j` and `k` for fine movements or `{` and `}` for bigger jumps. To quit, press `q`.

To simply get a list of stories printed to the terminal, provide the `-p` flag

The original Hacker News website can be found [here](https://news.ycombinator.com/) or check out the best stories page this program parses [here](https://news.ycombinator.com/best)

## License

[MIT](https://github.com/Rolv-Apneseth/daily-hn/blob/2d40839e6e625c55075430bde5fef337a08e89ba/LICENSE)
