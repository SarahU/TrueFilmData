import unittest

from queries import Report

report = Report()


class TestQueries(unittest.TestCase):

    def test_read_movies_processed(self):
        result = report.read_cleaned_movies_data()
        self.assertEqual((45450, 24), result.shape)

    def test_budget_vs_revenue(self):
        result = report.budget_vs_revenue()
        self.assertTrue('budget_revenue_ratio' in result.columns)

    def test_read_movie_names(self):
        result = report.read_movie_names()
        self.assertEqual(42278, len(result))


if __name__ == '__main__':
    unittest.main()
