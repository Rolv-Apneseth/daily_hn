from daily_hn import UI, Stories


class TestDailyHN:
    # Expensive call as it must scrape the newscombinator best stories page, so
    # it is only made once
    stories: list[dict] = Stories.get_stories()
    assert stories

    def test_Stories(self, capsys):
        Stories.print_articles(stories=self.stories)

        captured = capsys.readouterr()

        assert len(captured.out.split("\n")) // 5 == len(self.stories)  # 5 lines per

        for story in self.stories:
            assert story["headline"] and story["link"] and story["score"]
            assert story["link"].startswith("http")
            assert type(story["score"]) is int

        assert self.stories[0]["score"] >= self.stories[-1]["score"]

    def test_UI_shortcuts(self):
        assert len(UI.story_shortcuts) >= len(self.stories)

    def test_UI_format_headlines(self):
        headline = "headline"
        formatted_headline = UI._format_headline(headline, 6)

        assert formatted_headline == "hea..."
