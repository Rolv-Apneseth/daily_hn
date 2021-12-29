# daily-hn

A quick command line tool for displaying the current best stories from [news.ycombinator.com](news.ycombinator.com) (Hacker News).

## Installation

Note that for any of the below commands, if you are running Windows, replace `python3` with just `python`

1. Requires python 3.6+ to run. Python can be installed from [here](https://www.python.org/downloads/).
2. To download, click on 'Code' to the top right, then download as a zip file. You can unzip using your preferred program.
   - You can also clone the repository using: `git clone https://github.com/Rolv-Apneseth/daily-hn.git`
3. Install the requirements for the program.
   - In your terminal, navigate to the cloned directory and run: `python3 -m pip install -r requirements.txt`

## Usage

To launch the program, navigate to this project's directory and run the command `python3 main.py`, and add the `-p` flag if you want use the program without the curses UI.

With the curses UI, you can open up stories (uses the default browser) by pressing the shortcut key to the left of that story. Navigate up and down using either `j` and `k` for fine movements or `{` and `}` for bigger jumps. To quit, press `q`.

The original Hacker News website can be found [here](https://news.ycombinator.com/) or check out the best stories page this program parses [here](https://news.ycombinator.com/best)
