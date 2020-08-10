import unittest

from movie_data_source import MovieDataSource
from postgres_movie_feed import WikiMovieDBLoader
from wikipedia_movies_data_source import WikipediaDataSource


class TestPostgresMovieFeed(unittest.TestCase):
    def test_get_wiki_data_for_movies(self):
        movieSource = MovieDataSource()
        wikiSource = WikipediaDataSource()

        loader = WikiMovieDBLoader()
        result = loader.get_wiki_data_for_movies()
        self.assertEqual((45450, 27), result.shape)


if __name__ == '__main__':
    unittest.main()
