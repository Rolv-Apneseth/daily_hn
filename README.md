# hacker-news-webscraper
 Webscraper with a tkinter ui which displays some of the currently most voted headlines on Hacker News, with clickable links.

## What I learned
* Building GUI's using tkinter
* Web scraping
* Sorting and filtering data scraped off a website so it can be displayed nicely
* Connecting functions to labels and wrapping text to make clickable links to articles
* Use of OOP

## Installation
1. Requires python 3.6+ to run. Python can be installed from [here](https://www.python.org/downloads/).
2. Clone the repository by opening your command line/terminal and run: git clone https://github.com/Rolv-Apneseth/hacker-news-webscraper.git
    * Note: If you don't have git, it can be downloaded from [here](https://git-scm.com/downloads).
3. Install the requirements for the program.
    * In your terminal, navigate to the cloned directory and run: pip install -r requirements.txt
4. To run the actual program, navigate further into the file-sorter folder and run: python3 main.py

## Usage
1. Once loaded, the gui will display the first 10 articles with votes over 100, displayed in order.
2. To visit any of the listed articles, simply click on the article name and your browser will open on that page.
3. If there are another 10 articles available with more than 100 votes, pressing next on the top right will navigate to the next page.

Alternatively, you can execute the parse_script.py to display the articles in the terminal. Note that the links here will not be clickable.

The original Hacker News website can be found [here](https://news.ycombinator.com/) or by clicking the link at the top of the program.
