# <img alt="daily_hn" src="https://github.com/Rolv-Apneseth/daily_hn/blob/1f191fe1cb9f81892794d2d0b7d0173923df7da9/assets/daily_hn.png" width="400px"/>

![Tests](https://github.com/Rolv-Apneseth/daily_hn/actions/workflows/tests.yml/badge.svg)
![Linux](https://img.shields.io/badge/-Linux-grey?logo=linux)
![OSX](https://img.shields.io/badge/-OSX-black?logo=apple)
![Python](https://img.shields.io/badge/Python-v3.9%5E-green?logo=python)
![Version](https://img.shields.io/github/v/tag/rolv-apneseth/daily_hn?label=version)
[![PyPi](https://img.shields.io/pypi/v/daily_hn?label=pypi)](https://pypi.org/project/daily-hn/)
![Black](https://img.shields.io/badge/code%20style-black-000000.svg)

![daily_hn demo](https://user-images.githubusercontent.com/69486699/161394178-a6030503-f481-481e-999b-b027ea4bba96.png)


## Description

A command line tool for displaying and opening links to the current best stories from [news.ycombinator.com](https://news.ycombinator.com) (Hacker News).

You can find the best stories page this program parses [here!](https://news.ycombinator.com/best)

## Dependencies

- [Python](https://www.python.org/downloads/) v3.9+
- [Beautiful Soup 4](https://pypi.org/project/beautifulsoup4/)
- [Requests](https://pypi.org/project/requests/)
- If you are on Windows: [windows-curses](https://pypi.org/project/windows-curses/) (Python)

## Installation

### Pypi

> Install or update to latest version

```bash
python3 -m pip install daily-hn --upgrade
```

> If you are on Windows, also install `windows-curses`

```bash
pip install windows-curses daily-hn --upgrade
```

## Manual Installation

> Make sure you have `python3` and `git` installed

> Install Python requirements

```bash
python3 -m pip install requests beautifulsoup4
```

> Install

```bash
git clone https://github.com/Rolv-Apneseth/daily_hn.git
cd daily_hn
sudo make install
```

> Uninstall

```bash
sudo make uninstall
```

## Usage

After installation, the program can be launched from your terminal by running `daily_hn` (on Windows, use `python -m daily_hn` unless you added the `site-packages` folder to your `Path`).

With the `curses` UI (default), you can open up stories (uses the default browser) by pressing the shortcut key to the left of that story. Navigate up and down using either `j` and `k` for fine movements or `{` and `}` for bigger jumps. To quit, press `q`.

To simply print out a list of stories (links being clickable depends on your terminal emulator), provide the `-p` flag i.e. `daily_hn -p`.

## License

[MIT](https://github.com/Rolv-Apneseth/daily_hn/blob/2d40839e6e625c55075430bde5fef337a08e89ba/LICENSE)
