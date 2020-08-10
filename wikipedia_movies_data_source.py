import pandas as pd


class WikipediaDataSource:
    def get_data(self):
        return pd.read_csv('./data/wiki_movie_data.csv')
