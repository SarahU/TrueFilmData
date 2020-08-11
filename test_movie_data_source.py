import unittest

from movie_data_source import MovieDataSource

movie_source = MovieDataSource()


class TestMovieDataSource(unittest.TestCase):
    def test_read_movies_processed(self):
        result = movie_source.get_imdb_movie_data()
        self.assertEqual((45450, 24), result.shape)

    def test_read_movie_names(self):
        result = movie_source.read_movie_names()
        self.assertEqual(42278, len(result))

    def test_budget_vs_revenue(self):
        result = movie_source.get_data_with_budget_vs_revenue()
        self.assertTrue('budget_revenue_ratio' in result.columns)

    def test_read_wikipedia_data(self):
        result = movie_source.get_movie_wikipedia_data()
        self.assertEqual(29193, len(result))


if __name__ == '__main__':
    unittest.main()
