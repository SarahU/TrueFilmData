import unittest

from wikipedia_movies_data_source import WikipediaDataSource


class TestWikipediaDataSource(unittest.TestCase):
    def test_read_wikipedia_data(self):
        source = WikipediaDataSource()
        result = source.get_data()
        self.assertEqual(29193, len(result))


if __name__ == '__main__':
    unittest.main()
