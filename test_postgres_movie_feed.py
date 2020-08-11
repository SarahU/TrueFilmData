import unittest

from movie_data_source import MovieDataSource
from postgres_movie_feed import WikiMovieDBLoader
from wikipedia_movies_data_source import WikipediaDataSource

movieSource = MovieDataSource()
wikiSource = WikipediaDataSource()
loader = WikiMovieDBLoader(movieSource, wikiSource)


class TestPostgresMovieFeed(unittest.TestCase):
    def test_get_wiki_data_for_movies(self):
        result = loader.get_wiki_data_for_movies()
        self.assertEqual((45450, 28), result.shape)

    def test_get_year(self):
        result = loader.get_year('1995-10-30')
        self.assertEqual(1995, result)

    def test_load_top_movies_into_db(self):
        result = loader.get_by_highest_to_lowest_ratio_top_1000()
        self.assertEqual((1000, 9), result.shape)
        self.assertTrue('Title' in result.columns)
        self.assertTrue('budget' in result.columns)
        self.assertTrue('year' in result.columns)
        self.assertTrue('revenue' in result.columns)
        self.assertTrue('rating' in result.columns)
        self.assertTrue('ratio' in result.columns)
        self.assertTrue('production_companies' in result.columns)
        self.assertTrue('wikipedia_page_url' in result.columns)
        self.assertTrue('wikipedia_abstract' in result.columns)

    def test_db_loader_integration(self):
        result = loader.load_top_movies_into_db()
        self.assertTrue(result)


if __name__ == '__main__':
    unittest.main()
