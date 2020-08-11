from datetime import datetime
from sqlalchemy import create_engine, MetaData, Table, Column, Float, Integer, String, inspect
import pandas as pd

TOP_MOVES_TABLE = "top_movies"
FAKE_YEAR_PLACEHOLDER = 1111


class WikiMovieDBLoader:
    def __init__(self, moviesDataSource):
        self.movieSource = moviesDataSource

    def get_wiki_data_for_movies(self):
        imdb_movies_data = self.movieSource.get_data_with_budget_vs_revenue()
        wiki_movie_data = self.movieSource.get_movie_wikipedia_data()

        full_set = imdb_movies_data.merge(wiki_movie_data, left_on='title', right_on='Title', suffixes=('_imdb', '_wiki'))

        full_set.drop(['Title'], axis=1, inplace=True)

        return full_set

    def get_year(self, date):
        try:
            year = datetime.strptime(date, "%Y-%m-%d").year
            return year
        except:
            return FAKE_YEAR_PLACEHOLDER

    def get_by_highest_to_lowest_ratio_top_1000(self):
        df = self.get_wiki_data_for_movies().sort_values(by=['budget_revenue_ratio'])

        df['year'] = df.apply(lambda row: self.get_year(row.release_date), axis=1)
        df = df.drop(df[df.year == FAKE_YEAR_PLACEHOLDER].index)

        df = df.head(1000)

        df = df[
            ['title', 'budget', 'year', 'revenue', 'vote_average', 'budget_revenue_ratio', 'production_companies',
             'URL',
             'Abstract']]

        df = df.rename(columns={'vote_average': 'rating',
                                'budget_revenue_ratio': 'ratio',
                                'URL': 'wikipedia_page_url',
                                'Abstract': 'wikipedia_abstract'
                                })
        return df

    def drop_existing_table(self, engine):
        inspector = inspect(engine)
        if TOP_MOVES_TABLE in inspector.get_table_names():
            meta = MetaData()
            top_movies = Table(TOP_MOVES_TABLE, meta)
            top_movies.drop(engine)

    def load_top_movies_into_db(self):
        try:
            engine = create_engine('postgresql://postgres:docker@localhost:5432/postgres')
            self.drop_existing_table(engine)

            df = self.get_by_highest_to_lowest_ratio_top_1000()
            df.to_sql(TOP_MOVES_TABLE, engine)

            return True
        except Exception as e:
            print(e)
            return False
