import unittest
import pandas as pd

from movie_data_source import MovieDataSource
from wikipedia_data_feed import WikipediaDataFeed


class TestWikipediaDataFeed(unittest.TestCase):
    def test_update_wikipedia_data_source(self):
        movieDataSource = MovieDataSource()
        feed = WikipediaDataFeed(movieDataSource)
        result = feed.update_wikipedia_data_source()
        self.assertEqual(29193, len(result))

        data = pd.read_csv('./data/wiki_movie_data.csv')
        self.assertTrue((29193, 3), data.shape)

if __name__ == '__main__':
    unittest.main()